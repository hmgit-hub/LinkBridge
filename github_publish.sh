#!/bin/bash

# LinkBridge GitHub 发布脚本
# 使用方法: ./github_publish.sh YOUR_GITHUB_USERNAME

set -e

# 检查参数
if [ -z "$1" ]; then
    echo "❌ 错误: 请提供 GitHub 用户名"
    echo "使用方法: ./github_publish.sh YOUR_GITHUB_USERNAME"
    exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="linkbridge"
REMOTE_URL="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "🚀 开始发布 LinkBridge 到 GitHub..."
echo "📦 仓库地址: ${REMOTE_URL}"
echo ""

# 检查是否已添加远程仓库
if git remote get-url origin &>/dev/null; then
    echo "📝 检测到已存在的远程仓库"
    CURRENT_REMOTE=$(git remote get-url origin)
    echo "   当前地址: ${CURRENT_REMOTE}"
    read -p "   是否要更新远程仓库地址? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git remote set-url origin "${REMOTE_URL}"
        echo "✅ 远程仓库地址已更新"
    fi
else
    echo "📝 添加远程仓库..."
    git remote add origin "${REMOTE_URL}"
    echo "✅ 远程仓库已添加"
fi

echo ""
echo "📋 下一步操作:"
echo ""
echo "1. 在浏览器中打开 GitHub 并创建新仓库:"
echo "   https://github.com/new"
echo ""
echo "2. 仓库设置:"
echo "   - Repository name: ${REPO_NAME}"
echo "   - Description: LinkBridge - 跨 NAS 软链接管理工具"
echo "   - Public: ✅"
echo "   - 不要勾选: Add README, .gitignore, license"
echo ""
echo "3. 创建仓库后，运行以下命令推送代码:"
echo ""
echo "   git push -u origin main"
echo ""
echo "4. 如果使用 HTTPS 推送时需要认证，请创建 Personal Access Token:"
echo "   https://github.com/settings/tokens"
echo ""
echo "   Token 权限: 勾选 'repo' (完整仓库访问权限)"
echo ""
echo "5. 推送时会提示输入密码，粘贴 Token 即可"
echo ""
echo "📚 详细指南请查看: GITHUB_PUBLISH_GUIDE.md"
echo ""
echo "💡 提示: 首次推送可能需要输入 GitHub 用户名和 Personal Access Token"
echo ""
