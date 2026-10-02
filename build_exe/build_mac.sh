#!/usr/bin/env bash
# ============================================================
#  圣经提词器 · macOS 打包脚本
#  在 Mac 上（或 GitHub Actions 云 Mac）跑一次，生成 dist/圣经提词器.app
#  macOS 走系统自带的 WebKit，不需要 Windows 的 WebView2 Runtime。
#
#  用法：
#    本地 Mac：bash build_exe/build_mac.sh
#              （先 pip3 install pywebview pyobjc pyinstaller pillow）
#    CI      ：由 .github/workflows/release.yml 调用，依赖已在 workflow 装好
#
#  注意：本文件必须保持 LF 换行（CRLF 会让 bash 报 "\r: command not found"），
#        仓库根目录的 .gitattributes 已强制 *.sh 用 LF。
# ============================================================
set -e
cd "$(dirname "$0")"

PYBIN=$(command -v python3 || command -v python)

echo "== 1/3 生成 macOS 图标 app.icns =="
"$PYBIN" make_icns.py

echo "== 2/3 PyInstaller 打包 .app =="
# --windowed → 生成 .app bundle（不加 --onefile，否则出来是裸可执行文件而非 .app）
# --add-data 在 macOS 的分隔符是 ":"（Windows 是 ";"）
# 只 hidden-import cocoa 后端：pywebview 按平台动态选后端，静态分析找不到；
# 加 --collect-all webview 反而会把 Windows 专有依赖一起收进来，macOS 上易失败。
pyinstaller --noconfirm --windowed --clean \
  --name "圣经提词器" \
  --icon "app.icns" \
  --add-data "../圣经提词器.html:." \
  --hidden-import webview.platforms.cocoa \
  --osx-bundle-identifier "com.hongbing.bible-teleprompter" \
  app_main.py

echo "== 3/3 完成 =="
echo "产物：dist/圣经提词器.app"
echo "分发：把 .app 压成 zip 再发给用户（CI 里自动做）；用户解压后拖进「应用程序」。"
echo "      首次打开若被「无法验证开发者」拦住：右键 .app → 打开，即可正常运行。"
