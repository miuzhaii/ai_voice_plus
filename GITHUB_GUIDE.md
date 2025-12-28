# GitHub 上传指南

本指南将帮助您将 ai_voice_plus 项目上传到 GitHub。

## 📋 准备工作

1. **安装 Git**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install git
   
   # CentOS/RHEL
   sudo yum install git
   
   # macOS (使用 Homebrew)
   brew install git
   ```

2. **创建 GitHub 账号**
   - 访问 [GitHub](https://github.com/) 并注册账号

3. **配置 Git**
   ```bash
   git config --global user.name "您的用户名"
   git config --global user.email "您的邮箱"
   ```

## 🚀 上传步骤

### 方法一：使用 GitHub CLI (推荐)

1. **安装 GitHub CLI**
   ```bash
   # Ubuntu/Debian
   sudo apt install gh
   
   # macOS
   brew install gh
   ```

2. **登录 GitHub**
   ```bash
   gh auth login
   ```

3. **初始化仓库并上传**
   ```bash
   cd srv/nekro_agent/plugins/packages/ai_voice_plus
   gh repo create ai_voice_plus --public --source=. --remote=origin --push
   ```

### 方法二：手动创建仓库

1. **在 GitHub 上创建新仓库**
   - 访问 https://github.com/new
   - 仓库名称：`ai_voice_plus`
   - 描述：`AI 语音插件 Plus - 为 Nekro Agent 提供文本转语音功能`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"
   - 点击 "Create repository"

2. **初始化本地仓库**
   ```bash
   cd srv/nekro_agent/plugins/packages/ai_voice_plus
   git init
   ```

3. **添加所有文件**
   ```bash
   git add .
   ```

4. **提交更改**
   ```bash
   git commit -m "Initial commit: AI 语音插件 Plus v0.1.0"
   ```

5. **关联远程仓库**
   ```bash
   git remote add origin https://github.com/您的用户名/ai_voice_plus.git
   ```

6. **推送到 GitHub**
   ```bash
   git branch -M main
   git push -u origin main
   ```

## 📝 更新 package_data.json

上传成功后，更新 [`package_data.json`](../package_data.json) 中的 git_url：

```json
{
  "module_name": "ai_voice_plus",
  "git_url": "https://github.com/您的用户名/ai_voice_plus.git",
  "remote_id": "332b1dbc-668d-4cae-b909-2bae9c439055",
  "author": "KroMiose",
  "description": "AI 语音插件 Plus - 提供文本转语音功能，支持私聊和群聊"
}
```

## 🔄 后续更新

### 添加新功能或修复 Bug

```bash
# 1. 修改代码
# 2. 查看更改
git status

# 3. 添加修改的文件
git add .

# 4. 提交更改
git commit -m "描述您的更改"

# 5. 推送到 GitHub
git push
```

### 创建新分支（用于开发新功能）

```bash
# 创建并切换到新分支
git checkout -b feature/新功能名称

# 进行开发...

# 提交更改
git add .
git commit -m "添加新功能"

# 推送分支
git push -u origin feature/新功能名称
```

## 🎯 常用 Git 命令

```bash
# 查看状态
git status

# 查看提交历史
git log

# 查看分支
git branch

# 切换分支
git checkout 分支名

# 合并分支
git merge 分支名

# 拉取最新更改
git pull

# 查看远程仓库
git remote -v
```

## ⚠️ 注意事项

1. **敏感信息**：确保不要上传包含密码、密钥等敏感信息的文件
2. **.gitignore**：已配置好 `.gitignore` 文件，会自动忽略不必要的文件
3. **提交信息**：使用清晰的提交信息，便于追踪更改历史
4. **分支管理**：建议使用分支进行开发，保持主分支稳定

## 📚 参考资源

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub 官方文档](https://docs.github.com/)
- [Pro Git 中文版](https://git-scm.com/book/zh/v2)

---

祝您上传顺利！如有问题，请参考 GitHub 官方文档或寻求社区帮助。
