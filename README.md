# 圣经提词器（Bible Teleprompter）

一个**完全离线、双击即用**的中英双语圣经投影提词器。键盘翻节、目录定位、墨色金边视觉，经文与图标全部内嵌，断网也能运行。

- 作者：HongBing（© HongBing）
- 版本：1.0.0
- 协议：MIT（详见 LICENSE）
- 平台：Windows 10/11（自带 WebView2 即可）；Mac 用户直接打开 `圣经提词器.html` 即可使用

---

## 目录结构

```
Bible\
├── 圣经提词器.html              ← 【唯一源码】单文件、离线、含更新提醒 + 署名扫光（也是 Mac 版，直接发这个）
├── 圣经提词器-使用说明书.html   ← 说明书可编辑源（改文字后用 make_manual_pdf.py 重出 PDF）
├── 圣经提词器-使用说明书.pdf    ← 说明书成品（发给客户）
├── make_manual_pdf.py          ← 说明书 PDF 生成脚本（reportlab，内嵌中文字体）
├── version.json                ← 更新检测的版本文件（发新版时上传到 GitHub 仓库根目录）
├── README.md                   ← 本文件
└── build_exe\                  ← 【纯打包工程，不发给客户】
    ├── app_main.py             ← pywebview 壳（把 HTML 写到临时文件用 file:// 加载，已修黑屏）
    ├── 圣经提词器.spec         ← PyInstaller 配置（直接读上级的源码 HTML，不在 build_exe 留重复拷贝）
    ├── app.ico                 ← 图标（由 logo.png 生成）
    ├── logo.png                ← 图标源文件（已 base64 内联进 HTML，运行不再引用，仅留作将来改图标）
    ├── version_info.txt        ← exe 版本信息（HongBing / © HongBing / 1.0.0.0）
    ├── 重新打包.bat            ← 改完 HTML 后双击即重出 exe（Windows 双击运行）
    └── dist\
        └── 圣经提词器_v1.0.exe ← 【软件成品，发给客户】
```

> 关键约定：**根目录 = 源码与交付物（给人看/发给客户）；`build_exe/` = 仅用于重建 exe 的打包工程，不必发给客户。**
> 提交到 Git 仓库时：`build_exe/build/`（构建缓存）与 `build_exe/dist/`（exe 产物）已被 `.gitignore` 忽略；源码与 README 正常提交；exe 成品通过 **GitHub Releases** 分发，不进仓库。

---

## 发给客户的物料

1. `build_exe/dist/圣经提词器_v1.0.exe` — 软件本体，双击即用、无需安装、无需联网。
2. `圣经提词器-使用说明书.pdf` - 使用说明（白底黑字、中文字体内嵌，任意 PDF 阅读器可开）。

> 极少数精简版 / 老系统若双击报错，是缺 WebView2 运行时，让客户装一下「Microsoft WebView2 Runtime（Evergreen）」即可。Win10/11 绝大多数自带。

---

## 操作快捷键

| 按键 | 功能 |
|------|------|
| ← → | 上一节 / 下一节 |
| ↑ ↓ | 上一章 / 下一章 |
| L | 中文 / 英文 切换 |
| T 或点左上 logo | 打开目录（旧约/新约 → 分类 → 书卷 → 章 → 节） |
| Esc | 关闭目录 |

---

## 如何重建 exe（改了源码以后）

1. 编辑根目录的 `圣经提词器.html`（界面、文案、版本号等）。
2. 双击 `build_exe/重新打包.bat`。
3. 新 exe 生成在 `build_exe/dist/圣经提词器_v1.0.exe`，会自动弹出资源管理器定位。

> 注意：打包时 `圣经提词器.spec` 会直接读取**上级根目录**的 `圣经提词器.html`，`build_exe/` 下**不再保留重复拷贝**，请始终改根目录那份。

---

## 如何发布更新（让用户自行下载）

1. 把 `version.json` 里的 `version` 改成新版本号（需大于用户手里的版本），`url` 填你的下载页，提交到 GitHub 仓库根目录。
2. 把新 exe 上传到 GitHub **Releases**（标记为 latest）。
3. 把 `圣经提词器.html` 里的 `APP_VERSION` 也改成同一新号，重新打包（否则「已看过」标记不会轮换，会重复提醒）。

用户侧：软件里签名「© Design by HongBing」检测到有新版时会轻轻闪烁，点一下即用浏览器打开下载页；看过一次后该版本不再闪。断网 / 取不到版本信息时完全静默，不影响离线使用。

> 待替换的地址（目前是占位）：`圣经提词器.html` 中的 `UPDATE_INFO_URL`（读 version.json）与 `UPDATE_FALLBACK_URL`（下载页）。

---

## 已知坑（开发备忘）

- **pywebview 打包大体积 HTML 必须用 file:// 加载**：直接把 ~7MB 的 HTML 当字符串传给 WebView2（`NavigateToString`）在部分环境会静默失败、只露深色背景（黑屏）。`app_main.py` 已改为先写临时文件再 `file://` 加载。
- **打包别留重复 HTML**：源码只在根目录一份，`build_exe/` 下不复制，靠 `spec` 的 `datas=[('../圣经提词器.html','.')]` 读取。
