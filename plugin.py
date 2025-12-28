"""
# AI 语音 (AI Voice)

提供文本转语音（TTS）功能，让 AI 可以"开口说话"。

## 主要功能

- **文本转语音**: AI 可以将指定的文本，通过预设的 AI 语音角色（声源）合成为语音消息，并发送到私聊或群聊中。
- **角色查询**: 用户可以通过 `/ai_voices` 命令，查询当前协议端支持的所有可用语音角色。
- **私聊/群聊支持**: 支持在私聊和群聊中使用 AI 语音功能。

## 使用方法

- **AI 自动调用**: 在某些场景下，AI 可能会决定使用语音来回复，此时它会自动调用此插件。
- **命令查询**: 用户可以使用 `/ai_voices` 命令查看可用的声音列表，然后在插件配置中修改 `AI_VOICE_CHARACTER` 来切换 AI 的声音。
- **目标群配置**: 在插件配置中设置 `AI_VOICE_TARGET_GROUP`，指定用于生成 AI 语音的群号。留空则使用当前群（仅群聊时有效）。

## 工作原理

1. AI 语音生成：将文本发送到配置的目标群，调用 `send_group_ai_record` API 生成语音
2. 获取语音 URL：从 API 响应中提取语音文件的 URL
3. 发送语音消息：使用普通语音消息格式将语音发送到实际目标（私聊或群聊）

## 配置说明

- **AI_VOICE_CHARACTER**: AI 语音角色 ID，使用 `/ai_voices` 命令查看可用角色
- **AI_VOICE_TARGET_GROUP**: 用于生成 AI 语音的群号，留空则使用当前群

## 特别说明

此插件的功能**高度依赖**于您所使用的 OneBot v11 协议端。它需要协议端实现了 `send_group_ai_record` 和 `get_ai_characters` 这两个自定义 API。如果您的协议端不支持这些 API，此插件将无法正常工作。

## 注意事项

- 如果在私聊中使用 AI 语音，**必须**配置 `AI_VOICE_TARGET_GROUP`，因为私聊无法直接调用 `send_group_ai_record`
- 目标群需要是 bot 所在的群，否则无法生成语音
- 生成的语音会先发送到目标群，然后获取 URL 再发送到实际目标
"""

import asyncio
import json
import re
from typing import Optional

from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from pydantic import Field

from nekro_agent.adapters.onebot_v11.core.bot import get_bot
from nekro_agent.adapters.onebot_v11.matchers.command import (
    command_guard,
    finish_with,
    on_command,
)
from nekro_agent.api import core
from nekro_agent.api.plugin import (
    ConfigBase,
    ExtraField,
    NekroPlugin,
    SandboxMethodType,
)
from nekro_agent.api.schemas import AgentCtx
from nekro_agent.models.db_chat_channel import DBChatChannel
from nekro_agent.schemas.chat_message import ChatType

plugin = NekroPlugin(
    name="AI 语音插件 Plus",
    module_name="ai_voice_plus",
    description="提供AI语音生成功能，支持将文本转为AI合成语音",
    version="0.1.0",
    author="xiaojiu",
    url="https://github.com/miuzhaii/ai_voice_plus/",
    support_adapter=["onebot_v11"],
)


@plugin.mount_config()
class AIVoiceConfig(ConfigBase):
    """AI语音配置"""

    AI_VOICE_TARGET_GROUP: str = Field(
        default="",
        title="AI 语音目标群",
        description="用于生成 AI 语音的群号，留空则使用当前群",
        json_schema_extra={"placeholder": "留空则使用当前群"},
    )

    AI_VOICE_CHARACTER: str = Field(
        default="lucy-voice-xueling",
        title="AI 语音角色",
        description="从下拉列表选择 AI 语音角色，或手动输入角色 ID",
        json_schema_extra={"placeholder": "使用 /ai_voices_plus 命令查看可用角色"},
    )


# 获取配置
config = plugin.get_config(AIVoiceConfig)

# 全局变量存储角色列表
_ai_voice_characters_cache: dict = {}


async def fetch_ai_characters(group_id: int) -> dict:
    """从目标群获取 AI 语音角色列表
    
    Args:
        group_id: 群号
        
    Returns:
        dict: 角色列表字典 {role_id: role_name}
    """
    global _ai_voice_characters_cache
    
    try:
        tags = await get_bot().call_api("get_ai_characters", group_id=group_id)
        characters = {}
        
        for tag in tags:
            for char in tag["characters"]:
                char_id = char["character_id"]
                char_name = char["character_name"]
                characters[char_id] = char_name
        
        _ai_voice_characters_cache = characters
        core.logger.info(f"成功获取 {len(characters)} 个 AI 语音角色")
        
        # 保存到插件存储
        await plugin.store.set(store_key="ai_voice_characters", value=json.dumps(characters))
        
        return characters
    except Exception as e:
        core.logger.error(f"获取 AI 语音角色列表失败: {e}")
        return {}


async def get_ai_characters() -> dict:
    """获取缓存的 AI 语音角色列表
    
    Returns:
        dict: 角色列表字典 {role_id: role_name}
    """
    global _ai_voice_characters_cache
    
    # 如果缓存为空，尝试从存储加载
    if not _ai_voice_characters_cache:
        try:
            cached_data = await plugin.store.get(store_key="ai_voice_characters")
            if cached_data:
                _ai_voice_characters_cache = json.loads(cached_data)
        except Exception as e:
            core.logger.warning(f"加载角色列表缓存失败: {e}")
    
    return _ai_voice_characters_cache


@on_command("ai_voices_plus", aliases={"ai-voices-plus"}, priority=5, block=True).handle()
async def _(matcher: Matcher, event: MessageEvent, bot: Bot, arg: Message = CommandArg()):
    """查看 AI 语音角色列表"""
    username, cmd_content, chat_key, chat_type = await command_guard(event, bot, arg, matcher)

    if chat_type is ChatType.GROUP:
        group_id = int(chat_key.split("_")[2])
        tags = await bot.call_api("get_ai_characters", group_id=group_id)
        formatted_characters = []
        for tag in tags:
            char_list = []
            for char in tag["characters"]:
                char_list.append(f"ID: {char['character_id']} - {char['character_name']}")
            formatted_characters.append(f"=== {tag['type']} ===\n" + "\n".join(char_list))

        await finish_with(matcher, message="当前可用的 AI 声聊角色: \n\n" + "\n\n".join(formatted_characters))
    else:
        await finish_with(matcher, message="AI 声聊功能仅支持群组")


@on_command("refresh_ai_voices_plus", aliases={"刷新ai语音角色plus", "refresh-ai-voices-plus"}, priority=5, block=True).handle()
async def _(matcher: Matcher, event: MessageEvent, bot: Bot, arg: Message = CommandArg()):
    """刷新 AI 语音角色列表"""
    username, cmd_content, chat_key, chat_type = await command_guard(event, bot, arg, matcher)
    
    if chat_type is ChatType.GROUP:
        group_id = int(chat_key.split("_")[2])
        characters = await fetch_ai_characters(group_id)
        
        if characters:
            formatted_chars = []
            for char_id, char_name in characters.items():
                formatted_chars.append(f"ID: {char_id} - {char_name}")
            
            await finish_with(matcher, message=f"已刷新 AI 语音角色列表（共 {len(characters)} 个）：\n\n" + "\n".join(formatted_chars))
        else:
            await finish_with(matcher, message="刷新失败，请检查 bot 权限")
    else:
        await finish_with(matcher, message="刷新角色列表功能仅支持群组")


@on_command("reload_ai_voice_config_plus", aliases={"重载ai语音配置plus", "reload-ai-voice-config-plus"}, priority=5, block=True).handle()
async def _(matcher: Matcher, event: MessageEvent, bot: Bot, arg: Message = CommandArg()):
    """重新加载 AI 语音配置"""
    username, cmd_content, chat_key, chat_type = await command_guard(event, bot, arg, matcher)
    
    # 重新加载配置
    global config
    config = plugin.get_config(AIVoiceConfig)
    
    config_info = f"""
AI 语音配置已重新加载：

- 目标群: {config.AI_VOICE_TARGET_GROUP or '当前群'}
- 语音角色: {config.AI_VOICE_CHARACTER}
"""
    
    await finish_with(matcher, message=config_info.strip())


@plugin.mount_sandbox_method(SandboxMethodType.TOOL, "发送消息语音 Plus")
async def ai_voice_plus(_ctx: AgentCtx, chat_key: str, text: str) -> bool:
    """发送消息语音 Plus

    支持在私聊和群聊中发送 AI 生成的语音消息。
    - 私聊语音：将语音发送到私聊对话中
    - 群聊语音：将语音发送到群聊中

    Args:
        chat_key (str): 聊天的唯一标识符（支持私聊和群聊）
        text (str): 语音文本 (必须是自然语句，不包含任何特殊符号)

    Returns:
        bool: 操作是否成功
    """
    db_chat_channel: DBChatChannel = await DBChatChannel.get_channel(chat_key=chat_key)
    chat_type = db_chat_channel.chat_type
    chat_id = db_chat_channel.channel_id

    # 1. 确定目标群（用于生成 AI 语音）
    target_group_id = None
    
    if config.AI_VOICE_TARGET_GROUP:
        # 使用配置的目标群
        try:
            target_group_id = int(config.AI_VOICE_TARGET_GROUP)
        except ValueError:
            core.logger.error(f"[{chat_key}] 配置的目标群 ID 无效: {config.AI_VOICE_TARGET_GROUP}")
            return False
    else:
        # 使用当前群（仅当当前是群聊时）
        if chat_type != ChatType.GROUP:
            core.logger.error(f"[{chat_key}] 当前不是群聊且未配置目标群")
            return False
        target_group_id = int(chat_id.split("_")[1])

    # 2. 使用 get_ai_record API 生成语音并获取 URL
    voice_url = None
    
    try:
        core.logger.info(f"[{chat_key}] 调用 get_ai_record: target_group={target_group_id}, character={config.AI_VOICE_CHARACTER}, text={text[:50]}...")
        ai_record_result = await get_bot().call_api(
            "get_ai_record",
            group_id=target_group_id,
            character=config.AI_VOICE_CHARACTER,
            text=text,
        )
        core.logger.info(f"[{chat_key}] get_ai_record 响应: {ai_record_result}")
        core.logger.info(f"[{chat_key}] 响应类型: {type(ai_record_result)}")
        
        # 从响应中提取 URL
        if isinstance(ai_record_result, str):
            # 响应直接是 URL 字符串
            voice_url = ai_record_result
            core.logger.info(f"[{chat_key}] 从字符串响应获取到 URL: {voice_url}")
        elif isinstance(ai_record_result, dict):
            if "data" in ai_record_result and isinstance(ai_record_result["data"], str):
                voice_url = ai_record_result["data"]
                core.logger.info(f"[{chat_key}] 从 data 字段获取到 URL: {voice_url}")
            elif "url" in ai_record_result:
                voice_url = ai_record_result["url"]
                core.logger.info(f"[{chat_key}] 从 url 字段获取到 URL: {voice_url}")
    except Exception as e:
        core.logger.error(f"[{chat_key}] 生成 AI 语音失败: {e}")
        return False

    if not voice_url:
        core.logger.error(f"[{chat_key}] 无法获取语音 URL，响应: {ai_record_result}")
        return False

    core.logger.info(f"[{chat_key}] 获取到语音 URL: {voice_url}")

    # 4. 构造语音消息 CQ 码
    voice_message = f"[CQ:record,file={voice_url}]"

    # 5. 发送语音到实际目标
    try:
        if chat_type == ChatType.GROUP:
            # 群聊
            group_id = int(chat_id.split("_")[1])
            await get_bot().call_api(
                "send_msg",
                message_type="group",
                group_id=group_id,
                message=voice_message,
            )
            core.logger.info(f"[{chat_key}] 语音已发送到群 {group_id}")
        elif chat_type == ChatType.PRIVATE:
            # 私聊
            user_id = int(chat_id.split("_")[1])
            await get_bot().call_api(
                "send_msg",
                message_type="private",
                user_id=user_id,
                message=voice_message,
            )
            core.logger.info(f"[{chat_key}] 语音已发送到私聊用户 {user_id}")
        else:
            core.logger.error(f"[{chat_key}] 不支持的聊天类型: {chat_type}")
            return False
        
        return True
    except Exception as e:
        core.logger.error(f"[{chat_key}] 发送语音失败: {e}")
        return False


@plugin.mount_init_method()
async def init():
    """插件初始化"""
    core.logger.info("AI 语音插件 Plus 已加载，使用 /ai_voices_plus 命令查看可用角色")


@plugin.mount_cleanup_method()
async def clean_up():
    """清理插件"""
    pass
