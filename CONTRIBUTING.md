# 贡献指南

感谢您对 AI 语音插件 Plus 的关注！我们欢迎任何形式的贡献。

## 🤝 如何贡献

### 报告 Bug

如果您发现了 Bug，请在 [Issues](../../issues) 中提交，并包含以下信息：

- Bug 的详细描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（Python 版本、Nekro Agent 版本等）
- 相关日志（如果适用）

### 提出新功能

如果您有新功能的想法，请在 [Issues](../../issues) 中提交 Feature Request，并详细描述：

- 功能的用途和价值
- 实现思路
- 可能的 API 设计

### 提交代码

1. **Fork 本仓库**
   ```bash
   # 在 GitHub 上点击 Fork 按钮
   ```

2. **克隆您的 Fork**
   ```bash
   git clone https://github.com/您的用户名/ai_voice_plus.git
   cd ai_voice_plus
   ```

3. **创建特性分支**
   ```bash
   git checkout -b feature/您的功能名称
   ```

4. **进行更改**
   - 编写代码
   - 添加必要的测试
   - 更新文档

5. **提交更改**
   ```bash
   git add .
   git commit -m "描述您的更改"
   ```

6. **推送到您的 Fork**
   ```bash
   git push origin feature/您的功能名称
   ```

7. **创建 Pull Request**
   - 在 GitHub 上创建 Pull Request
   - 详细描述您的更改
   - 等待代码审查

## 📋 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 规范
- 使用有意义的变量和函数名
- 添加必要的注释和文档字符串
- 保持代码简洁清晰

### 提交信息规范

使用清晰的提交信息：

```
<type>: <subject>

<body>

<footer>
```

类型可以是：
- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

示例：
```
feat: 添加语音角色缓存功能

- 实现角色列表缓存机制
- 减少不必要的 API 调用
- 添加缓存刷新命令
```

## 🧪 测试

在提交代码前，请确保：

- 代码能够正常运行
- 新功能经过测试
- 没有引入新的 Bug
- 遵循项目现有的代码风格

## 📝 文档

如果您的更改影响了用户使用，请更新：

- README.md
- 相关的代码注释
- 函数和类的文档字符串

## 💬 交流

- 在 Issue 中讨论问题和想法
- 在 Pull Request 中讨论代码更改
- 保持友好和尊重的交流态度

## 📄 许可

通过贡献代码，您同意您的贡献将在 [MIT License](LICENSE) 下发布。

---

再次感谢您的贡献！🎉
