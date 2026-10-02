# 📕圣经提词器（Bible Teleprompter）

一个**完全离线、双击即用**的中英双语圣经投影提词器。键盘翻节、目录定位、墨色金边视觉，经文与图标全部内嵌，断网也能运行。

- 作者：HongBing（© HongBing）
- 版本：1.2.0
- 协议：MIT（详见 LICENSE）
- 平台：
  - **Windows 10/11** → `bible-teleprompter_v1.2.0.exe`（自带 WebView2 即可）
  - **macOS** → `bible-teleprompter_v1.2.0-macOS.zip`（解压出 `圣经提词器.app`，走系统自带 WebKit）
  - 二者都不需要用户装 Python；Mac 若不想装软件，直接双击 `圣经提词器.html` 也能用

---

## 目录结构

```
Bible\
├── 圣经提词器.html              ← 【唯一源码】单文件、离线、含更新提醒 + 署名扫光（也是 Mac 版，直接发这个）
├── 圣经提词器-使用说明书.html   ← 说明书可编辑源（改文字后用 make_manual_pdf.py 重出 PDF）
├── 圣经提词器-使用说明书.pdf    ← 说明书成品（发给客户）
├── make_manual_pdf.py          ← 说明书 PDF 生成脚本（reportlab，内嵌中文字体）
├── version.json                ← 【版本号唯一真源】更新检测 + 打包命名都读它
├── .gitattributes              ← 强制 *.sh 用 LF 换行（CRLF 会让 Mac 的 bash 报错）
├── .github\workflows\release.yml ← 云端打包（Windows exe + macOS app，打 tag 自动发版）
└── build_exe\                  ← 【纯打包工程，不发给用户】
    ├── app_main.py             ← pywebview 壳（把 HTML 写到临时文件用 file:// 加载，已修黑屏）
    ├── bible-teleprompter.spec ← Windows 打包配置（版本号自动读 version.json）
    ├── build_mac.sh            ← macOS 打包脚本（云 Mac / 本地 Mac 都能跑）
    ├── make_version_info.py    ← 从 version.json 生成 version_info.txt（免手改）
    ├── make_icns.py            ← 从 logo.png 生成 macOS 图标 app.icns
    ├── app.ico / logo.png      ← 图标（Windows 用 ico，macOS 用 icns，同源派生）
    ├── version_info.txt        ← exe 版本信息（由 make_version_info.py 自动生成）
    ├── 重新打包.bat            ← 改完 HTML 后双击即重出 exe（Windows 双击运行）
    └── dist\
        └── bible-teleprompter_v1.2.0.exe ← 【软件成品，发给用户】（ASCII 名，避免 GitHub 附件中文被吞）
```

> 关键约定：**根目录 = 源码与交付物（给人看/发给用户）；`build_exe/` = 仅用于重建 exe 的打包工程，不必发给用户。**
> 提交到 Git 仓库时：`build_exe/build/`（构建缓存）、`build_exe/dist/`（exe 产物）、`build_exe/app.icns`（派生图标）已被 `.gitignore` 忽略；源码与 README 正常提交；exe / zip 成品通过 **GitHub Releases** 分发，不进仓库。

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

## 如何打包（本地 / 云端）

**Windows 本地打包**（改了源码后想立刻出 exe）：

1. 编辑根目录的 `圣经提词器.html`（界面、文案、版本号等）。
2. 双击 `build_exe/重新打包.bat` —— 它会自动同步版本号、清理旧产物、打包并弹出资源管理器定位。
3. 产物：`build_exe/dist/bible-teleprompter_v1.2.0.exe`。

> 注意：打包时 `bible-teleprompter.spec` 会直接读取**上级根目录**的 `圣经提词器.html`，`build_exe/` 下**不再保留重复拷贝**，请始终改根目录那份。

**macOS 打包**：Windows 上**无法**交叉编译出 `.app`，必须在 Mac 上或借云端 Mac 编译 → 见下一节。

---

## 如何打包 Mac 版（云端 CI，推荐）

Windows 电脑打不出 macOS 的 `.app`，所以 Mac 版走 **GitHub Actions 的云 Mac 机器**（免费、无需你有 Mac）。

两台机器分工：

| 平台 | 谁构建 | 产物 |
|------|--------|------|
| Windows | `windows-latest` 云机器 | `bible-teleprompter_v1.2.0.exe` |
| macOS | `macos-latest` 云 Mac | `bible-teleprompter_v1.2.0-macOS.zip`（内含 `圣经提词器.app`） |

**发布方式（打 tag 即全自动）**：

```bash
git tag v1.2.0      # 版本号与 version.json 保持一致
git push --tags
```

推上去后 Actions 自动：装依赖 → 生成图标 → 打 Windows exe → 打 macOS app → 压 zip → **自动创建 Release 并上传两个附件**（`generate_release_notes: true` 会自动生成更新说明）。

**只想自测、不发版**：去仓库 **Actions** 页选「发布新版本（打包 exe + app）」→ **Run workflow** → 构建完在页面底部 `Artifacts` 下载两份产物。

> 关键说明：
> - `build_exe/build_mac.sh` 必须保持 **LF 换行**，仓库根 `.gitattributes` 已强制；否则 bash 会报 `\r: command not found`。
> - macOS 的 `--add-data` 分隔符是 `:`，Windows 是 `;`，两个脚本已分别处理。
> - 未签名的 app 首次打开会被 Gatekeeper 拦（「无法验证开发者」），属正常现象，让用户**右键 `.app` → 打开**即可；想彻底消除需 Apple 开发者账号（99 美元/年）签名。
> - 当前 `macos-latest` 构建的是 **Apple Silicon（M 系列）**版；Intel 老 Mac 需要额外加一个 `macos-13` 的 job 才能覆盖。

---

## 如何发布更新（发版检查清单）

### 第 1 步：改版本号（现在只需 3 处，比之前少）

`version.json` 是**唯一真源**，`spec` 的 exe 名、`version_info.txt`、bat 的产物定位都已改为自动派生，不用再手改：

| # | 文件 | 变量 / 字段 | 改什么 |
|---|------|------------|--------|
| 1 | `version.json`（第 2 行） | `"version"` | `"旧号"` → `"新号"` ← **改这里，下面两项自动跟上** |
| 2 | `圣经提词器.html`（约第 1009 行） | `const APP_VERSION` | `'旧号'` → `'新号'`（决定用户端是否弹更新红点，必须改） |
| 3 | `README.md` | 版本号与文件名 | 全文 `旧号` / `v旧号.exe` → `新号` / `v新号.exe` |

自动派生、无需手改：`bible-teleprompter.spec` 的 `name=`（读 version.json）、`version_info.txt`（由 `make_version_info.py` 生成）、`重新打包.bat`（用通配符匹配产物）。

### 第 2 步：发版（推荐云端一键，也可手动）

**方式 A · 云端自动（推荐）**：打 tag 推送，Actions 自动构建 **Windows exe + macOS app** 并直接建好 Release：

```bash
git add . && git commit -m "feat(1.2.1): 说明这次改了什么"
git tag v1.2.1        # 必须与 version.json 的 version 一致
git push origin main --tags
```

**方式 B · 手动**：本地双击 `重新打包.bat` 出 exe，再去 Releases → Draft a new release → Tag `v1.2.1`、Title `圣经提词器 v1.2.1`、✅ Set as the latest release、拖入 exe（**ASCII 名**，中文名会被吞）、Publish。

> push 注意事项：
> - 密码/令牌填 **PAT**，不是 GitHub 登录密码。
> - 凭据助手用 `manager-core`，别写成 `credential-manager-core`。
> - 直连 GitHub 超时，可在 VSCode 终端重试，或临时开 Clash 走代理（`git config --global http.proxy http://127.0.0.1:7897`，用完 `--unset` 清掉）。

### 第 3 步：验证更新链路

用旧版软件打开 → 署名右上角出现红点呼吸闪烁 → 点它跳转到 `releases/latest` 下载页，即更新提醒生效。

> 更新检测已固定指向本仓库：`UPDATE_INFO_URL` 读 `version.json`，`UPDATE_FALLBACK_URL` 跳 `releases/latest`，无需再改。

---

## 已知坑（开发备忘）

- **pywebview 打包大体积 HTML 必须用 file:// 加载**：直接把 ~7MB 的 HTML 当字符串传给 WebView2（`NavigateToString`）在部分环境会静默失败、只露深色背景（黑屏）。`app_main.py` 已改为先写临时文件再 `file://` 加载。
- **打包别留重复 HTML**：源码只在根目录一份，`build_exe/` 下不复制，靠 `spec` 的 `datas=[('../圣经提词器.html','.')]` 读取。
- **Release 附件必须 ASCII 名**：中文名 exe 上传后会被 GitHub 截断/吞掉，始终用 `bible-teleprompter_vX.Y.Z.exe` 形式。
- **git 直连 GitHub 不稳**：见上方「第 2 步」的 PAT / 凭据助手 / 代理绕行说明。
- **`.sh` 脚本必须 LF 换行**：Windows 默认会把检出文件转成 CRLF，导致云 Mac 执行 `build_mac.sh` 报 `\r: command not found`。已用根目录 `.gitattributes` 强制 `*.sh text eol=lf`。
- **macOS 不要加 `--collect-all webview`**：pywebview 按平台动态选后端，`--collect-all` 会把 Windows 专有依赖（pythonnet 等）一起收进来，在 Mac 上容易失败。只加 `--hidden-import webview.platforms.cocoa` 即可。
- **Windows runner 控制台是 cp1252**：任何 Python `print` 中文都会 `UnicodeEncodeError` 直接让构建失败。workflow 里已设 `PYTHONUTF8=1`，且两个 make_*.py 的日志输出刻意用纯 ASCII。
- **spec 里 `SPECPATH` 是目录不是文件路径**：不同 PyInstaller 版本行为有差异，`bible-teleprompter.spec` 里做了两种兼容（见过 `FileNotFoundError: version.json` 就是这坑）。

---

## 支持作者

如果这个项目对你有帮助，欢迎请我喝杯咖啡☕，让我有动力继续打磨 👇

<p align="center">
  <img src="assets/wechat-donate.png" alt="微信支付赞赏码" width="240">
  <br>
  <sub>微信扫码，随喜支持</sub>
</p>
