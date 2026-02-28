# LinkBridge GitHub 发布指南

## 方法一：使用 GitHub 网页界面创建仓库（推荐）

### 步骤 1：登录 GitHub
1. 访问 https://github.com
2. 登录你的 GitHub 账号

### 步骤 2：创建新仓库
1. 点击右上角的 "+" 按钮
2. 选择 "New repository"
3. 填写仓库信息：
   - **Repository name**: `linkbridge`
   - **Description**: `LinkBridge - 跨 NAS 软链接管理工具，支持群晖、威联通、飞牛、极空间等主流 NAS 系统`
   - **Public**: ✅ 公开（推荐）或 ❌ 私有
   - **Initialize this repository**:
     - ❌ Add a README file（我们已有 README.md）
     - ❌ Add .gitignore（我们已有 .gitignore）
     - ❌ Choose a license（后续可添加）
4. 点击 "Create repository"

### 步骤 3：推送代码到 GitHub

创建仓库后，GitHub 会显示推送代码的命令。执行以下命令：

```bash
# 添加远程仓库（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/linkbridge.git

# 推送代码到 GitHub
git push -u origin main
```

如果提示输入用户名和密码：
- **用户名**: 你的 GitHub 用户名
- **密码**: 你的 GitHub Personal Access Token（不是登录密码）

### 步骤 4：创建 Personal Access Token（如果需要）

如果使用 HTTPS 推送时遇到认证问题，需要创建 Personal Access Token：

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token" -> "Generate new token (classic)"
3. 填写信息：
   - **Note**: `LinkBridge Development`
   - **Expiration**: 选择有效期（推荐 90 天）
   - **Scopes**: 勾选 `repo`（完整仓库访问权限）
4. 点击 "Generate token"
5. **重要**: 复制生成的 token（只显示一次）

使用 token 推送：
```bash
# 推送时会提示输入密码，粘贴 token 即可
git push -u origin main
```

## 方法二：使用 GitHub CLI（需要先安装）

### 安装 GitHub CLI

**Windows:**
```powershell
winget install --id GitHub.cli
```

**macOS:**
```bash
brew install gh
```

**Linux:**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 登录 GitHub
```bash
gh auth login
```

按照提示选择：
- What account do you want to log into? -> `GitHub.com`
- What is your preferred protocol for Git operations? -> `HTTPS`
- Authenticate Git with your GitHub credentials? -> `Yes`
- How would you like to authenticate GitHub CLI? -> `Login with a web browser`

### 创建仓库并推送
```bash
# 创建仓库
gh repo create linkbridge --public --description "LinkBridge - 跨 NAS 软链接管理工具，支持群晖、威联通、飞牛、极空间等主流 NAS 系统"

# 推送代码
git push -u origin main
```

## 方法三：使用 SSH 密钥（推荐长期使用）

### 生成 SSH 密钥
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

### 添加 SSH 密钥到 GitHub
1. 复制公钥：
```bash
cat ~/.ssh/id_ed25519.pub
```

2. 添加到 GitHub：
   - 访问 https://github.com/settings/ssh
   - 点击 "New SSH key"
   - 粘贴公钥
   - 点击 "Add SSH key"

### 使用 SSH 推送
```bash
# 修改远程仓库地址为 SSH
git remote set-url origin git@github.com:YOUR_USERNAME/linkbridge.git

# 推送代码
git push -u origin main
```

## 推送后的后续操作

### 1. 添加 License
1. 访问仓库页面
2. 点击 "Add file" -> "Create new file"
3. 文件名：`LICENSE`
4. 选择模板：`MIT License`
5. 提交文件

### 2. 配置 GitHub Actions Secrets
如果需要自动构建 Docker 镜像，需要配置 Secrets：

1. 访问 https://github.com/YOUR_USERNAME/linkbridge/settings/secrets/actions
2. 点击 "New repository secret"
3. 添加以下 secrets：
   - `DOCKER_USERNAME`: Docker Hub 用户名
   - `DOCKER_PASSWORD`: Docker Hub 密码或 Access Token

### 3. 创建 Releases
1. 访问 https://github.com/YOUR_USERNAME/linkbridge/releases
2. 点击 "Create a new release"
3. 填写信息：
   - **Tag version**: `v1.0.0`
   - **Release title**: `LinkBridge v1.0.0`
   - **Description**: 复制 `CHANGELOG.md` 内容
4. 点击 "Publish release"

### 4. 启用 GitHub Pages（可选）
如果需要部署文档网站：

1. 访问 https://github.com/YOUR_USERNAME/linkbridge/settings/pages
2. Source 选择 `Deploy from a branch`
3. Branch 选择 `main` -> `/ (root)`
4. 点击 Save

## 常见问题

### Q1: 推送时提示 "Permission denied"
**A**: 检查以下几点：
- 确认仓库地址正确
- 确认有仓库的写入权限
- 如果使用 HTTPS，确认使用的是 Personal Access Token 而不是密码
- 如果使用 SSH，确认 SSH 密钥已添加到 GitHub

### Q2: 推送时提示 "remote contains work"
**A**: 远程仓库有本地没有的提交，需要先拉取：
```bash
git pull --rebase origin main
git push origin main
```

### Q3: 忘记 Personal Access Token
**A**: 需要重新生成：
1. 访问 https://github.com/settings/tokens
2. 找到旧 token，点击 "Delete"
3. 按照上面的步骤创建新 token

### Q4: 如何删除仓库
**A**:
1. 访问仓库页面
2. 点击 "Settings"
3. 滚动到页面底部 "Danger Zone"
4. 点击 "Delete this repository"

## 推荐的仓库设置

### 1. 启用 Issues
- Settings -> General -> Features -> Issues ✅

### 2. 启用 Discussions
- Settings -> General -> Features -> Discussions ✅

### 3. 启用 Projects
- Settings -> General -> Features -> Projects ✅

### 4. 设置主题
- Settings -> Appearance -> Theme color

### 5. 添加 Topics
- Settings -> Topics
- 添加：`nas`, `docker`, `flutter`, `symlink`, `file-management`

### 6. 配置 Branch Protection
- Settings -> Branches
- Add rule: `main`
- 勾选：
  - Require a pull request before merging
  - Require status checks to pass before merging
  - Require branches to be up to date before merging

## 推送成功后的验证

### 检查仓库内容
访问 https://github.com/YOUR_USERNAME/linkbridge，确认：
- ✅ 所有文件已上传
- ✅ README.md 正常显示
- ✅ .gitignore 已生效
- ✅ 提交历史正确

### 检查 CI/CD
1. 访问 "Actions" 标签页
2. 确认工作流正常运行

### 测试克隆
```bash
# 在其他目录测试克隆
git clone https://github.com/YOUR_USERNAME/linkbridge.git
cd linkbridge
ls -la
```

## 下一步

推送成功后，你可以：
1. 📝 完善 README.md
2. 🏷️ 添加更多 Topics
3. 📢 分享到社交媒体
4. 🤝 邀请协作者
5. 🐛 处理 Issues
6. 🔀 管理 Pull Requests

---

**祝你发布顺利！** 🎉
