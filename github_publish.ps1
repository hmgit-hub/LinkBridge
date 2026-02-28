# LinkBridge GitHub 发布脚本 (PowerShell)
# 使用方法: .\github_publish.ps1 -Username YOUR_GITHUB_USERNAME

param(
    [Parameter(Mandatory=$true)]
    [string]$Username
)

$REPO_NAME = "linkbridge"
$REMOTE_URL = "https://github.com/${Username}/${REPO_NAME}.git"

Write-Host "🚀 开始发布 LinkBridge 到 GitHub..." -ForegroundColor Green
Write-Host "📦 仓库地址: ${REMOTE_URL}" -ForegroundColor Cyan
Write-Host ""

# 检查是否已添加远程仓库
$remoteUrl = git remote get-url origin 2>$null
if ($remoteUrl) {
    Write-Host "📝 检测到已存在的远程仓库" -ForegroundColor Yellow
    Write-Host "   当前地址: ${remoteUrl}" -ForegroundColor Gray
    $update = Read-Host "   是否要更新远程仓库地址? (y/n)"
    if ($update -eq 'y' -or $update -eq 'Y') {
        git remote set-url origin $REMOTE_URL
        Write-Host "✅ 远程仓库地址已更新" -ForegroundColor Green
    }
} else {
    Write-Host "📝 添加远程仓库..." -ForegroundColor Yellow
    git remote add origin $REMOTE_URL
    Write-Host "✅ 远程仓库已添加" -ForegroundColor Green
}

Write-Host ""
Write-Host "📋 下一步操作:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. 在浏览器中打开 GitHub 并创建新仓库:" -ForegroundColor White
Write-Host "   https://github.com/new" -ForegroundColor Blue
Write-Host ""
Write-Host "2. 仓库设置:" -ForegroundColor White
Write-Host "   - Repository name: ${REPO_NAME}" -ForegroundColor Gray
Write-Host "   - Description: LinkBridge - 跨 NAS 软链接管理工具" -ForegroundColor Gray
Write-Host "   - Public: ✅" -ForegroundColor Gray
Write-Host "   - 不要勾选: Add README, .gitignore, license" -ForegroundColor Red
Write-Host ""
Write-Host "3. 创建仓库后，运行以下命令推送代码:" -ForegroundColor White
Write-Host ""
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. 如果使用 HTTPS 推送时需要认证，请创建 Personal Access Token:" -ForegroundColor White
Write-Host "   https://github.com/settings/tokens" -ForegroundColor Blue
Write-Host ""
Write-Host "   Token 权限: 勾选 'repo' (完整仓库访问权限)" -ForegroundColor Gray
Write-Host ""
Write-Host "5. 推送时会提示输入密码，粘贴 Token 即可" -ForegroundColor Yellow
Write-Host ""
Write-Host "📚 详细指南请查看: GITHUB_PUBLISH_GUIDE.md" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 提示: 首次推送可能需要输入 GitHub 用户名和 Personal Access Token" -ForegroundColor Yellow
Write-Host ""

# 询问是否立即推送
$pushNow = Read-Host "是否现在推送代码到 GitHub? (y/n)"
if ($pushNow -eq 'y' -or $pushNow -eq 'Y') {
    Write-Host ""
    Write-Host "📤 正在推送代码..." -ForegroundColor Yellow
    git push -u origin main
    Write-Host ""
    Write-Host "✅ 代码推送成功!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 访问你的仓库: https://github.com/${Username}/${REPO_NAME}" -ForegroundColor Cyan
} else {
    Write-Host ""
    Write-Host "⏸️  已跳过推送，稍后可手动运行: git push -u origin main" -ForegroundColor Yellow
}
