# AI 语音插件 Plus (AI Voice Plus)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.1.0-green.svg)](plugin.py)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📖 项目简介

AI 语音插件 Plus 是一个为 Nekro Agent 设计的文本转语音（TTS）插件，让 AI 可以"开口说话"。通过此插件，AI 可以将文本转换为自然流畅的语音消息，并支持在私聊和群聊中发送。

## ✨ 主要功能

- **文本转语音**: AI 可以将指定的文本，通过预设的 AI 语音角色（声源）合成为语音消息，并发送到私聊或群聊中
- **角色查询**: 用户可以通过 `/ai_voices_plus` 命令，查询当前协议端支持的所有可用语音角色
- **私聊/群聊支持**: 支持在私聊和群聊中使用 AI 语音功能
- **智能缓存**: 自动缓存角色列表，减少 API 调用次数
- **配置热重载**: 支持动态重新加载配置，无需重启服务

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Nekro Agent
- OneBot v11 协议端（需支持 `get_ai_record` 和 `get_ai_characters` API）

### 安装步骤

1. 将插件放置到 Nekro Agent 的插件目录：
   ```
   srv/nekro_agent/plugins/packages/ai_voice_plus/
   ```

2. 在 Nekro Agent 配置中启用插件

3. 重启 Nekro Agent 服务

### 配置说明

在插件配置中设置以下参数：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `AI_VOICE_TARGET_GROUP` | 用于生成 AI 语音的群号，留空则使用当前群 | `""` |
| `AI_VOICE_CHARACTER` | AI 语音角色 ID | `"lucy-voice-xueling"` |

## 📝 使用方法

### 命令列表

- `/ai_voices_plus` - 查看当前可用的 AI 语音角色列表
- `/refresh_ai_voices_plus` - 刷新 AI 语音角色列表
- `/reload_ai_voice_config_plus` - 重新加载 AI 语音配置

### AI 自动调用

在某些场景下，AI 可能会决定使用语音来回复，此时它会自动调用此插件。

### 工作原理

1. **AI 语音生成**: 将文本发送到配置的目标群，调用 `get_ai_record` API 生成语音
2. **获取语音 URL**: 从 API 响应中提取语音文件的 URL
3. **发送语音消息**: 使用普通语音消息格式将语音发送到实际目标（私聊或群聊）

## ⚠️ 注意事项

- 此插件的功能**高度依赖**于您所使用的 OneBot v11 协议端
- 协议端必须实现了 `get_ai_record` 和 `get_ai_characters` 这两个自定义 API
- 如果在私聊中使用 AI 语音，**必须**配置 `AI_VOICE_TARGET_GROUP`，因为私聊无法直接调用 API
- 目标群需要是 bot 所在的群，否则无法生成语音
- 生成的语音会先发送到目标群，然后获取 URL 再发送到实际目标

## 🔧 技术栈

- Python 3.8+
- NoneBot2 (OneBot v11 适配器)
- Nekro Agent 框架
- Pydantic (数据验证)

## 📦 项目结构

```
ai_voice_plus/
├── __init__.py          # 插件初始化
├── plugin.py            # 插件主逻辑
└── README.md            # 项目文档
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

## 👨‍💻 作者

**xiaojiu**

## 🔗 相关链接

- [Nekro Agent](https://github.com/KroMiose/nekro-agent)
- [OneBot v11](https://github.com/botuniverse/onebot-11)

## 📜 更新日志

### v0.1.0 (2025-12-28)

- 初始版本发布
- 支持文本转语音功能
- 支持私聊和群聊
- 支持角色查询和配置热重载

## 🙏 致谢

感谢所有为本项目做出贡献的开发者！

---

**注意**: 本插件仅供学习和交流使用，请遵守相关法律法规和平台使用条款。
