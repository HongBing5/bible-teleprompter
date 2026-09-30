# 📕圣经提词器（Bible Teleprompter）

一个**完全离线、双击即用**的中英双语圣经投影提词器。键盘翻节、目录定位、墨色金边视觉，经文与图标全部内嵌，断网也能运行。

- 作者：HongBing（© HongBing）
- 版本：1.2.0
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
    ├── bible-teleprompter.spec ← PyInstaller 配置（直接读上级的源码 HTML，不在 build_exe 留重复拷贝）
    ├── app.ico                 ← 图标（由 logo.png 生成）
    ├── logo.png                ← 图标源文件（已 base64 内联进 HTML，运行不再引用，仅留作将来改图标）
    ├── version_info.txt        ← exe 版本信息（HongBing / © HongBing / 1.2.0.0）
    ├── 重新打包.bat            ← 改完 HTML 后双击即重出 exe（Windows 双击运行）
    └── dist\
        └── bible-teleprompter_v1.2.0.exe ← 【软件成品，发给客户】（ASCII 名，避免 GitHub 附件中文被吞）
```

> 关键约定：**根目录 = 源码与交付物（给人看/发给客户）；`build_exe/` = 仅用于重建 exe 的打包工程，不必发给客户。**
> 提交到 Git 仓库时：`build_exe/build/`（构建缓存）与 `build_exe/dist/`（exe 产物）已被 `.gitignore` 忽略；源码与 README 正常提交；exe 成品通过 **GitHub Releases** 分发，不进仓库。

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
3. 新 exe 生成在 `build_exe/dist/bible-teleprompter_v1.2.0.exe`，会自动弹出资源管理器定位。

> 注意：打包时 `bible-teleprompter.spec` 会直接读取**上级根目录**的 `圣经提词器.html`，`build_exe/` 下**不再保留重复拷贝**，请始终改根目录那份。

---

## 如何发布更新（发版检查清单）

每次发版，先把 **6 处版本号** 统一改成新版（如 `1.2.0`），再走 **3 步**。

| # | 文件 | 变量 / 字段 | 改什么 |
|---|------|------------|--------|
| 1 | `圣经提词器.html`（约第 1009 行） | `const APP_VERSION` | `'旧号'` → `'新号'` |
| 2 | `version.json`（第 2 行） | `"version"` | `"旧号"` → `"新号"` |
| 3 | `build_exe/bible-teleprompter.spec`（第 33 行） | `name=` | `bible-teleprompter_旧号` → `bible-teleprompter_新号` |
| 4 | `build_exe/version_info.txt`（第 4/5/20/23/25 行） | `filevers`/`prodvers`、`FileVersion`、`OriginalFilename`、`ProductVersion` | `旧号.0` → `新号.0` |
| 5 | `build_exe/重新打包.bat`（第 4/7 行） | `taskkill` / `if exist` 路径 | 旧 exe 名 → `bible-teleprompter_新号.exe` |
| 6 | `README.md` | 版本号与 exe 文件名 | 全文 `旧号` / `v旧号.exe` → `新号` / `v新号.exe` |

发版 3 步：

1. **打包**：双击 `build_exe/重新打包.bat`，产物在 `build_exe/dist/bible-teleprompter_v1.2.0.exe`。
2. **提交**：`git add` 相关文件 → `git commit` → `git push origin main`。
   - 密码/令牌填 **PAT**，不是 GitHub 登录密码。
   - 凭据助手用 `manager-core`，别写成 `credential-manager-core`。
   - 直连 GitHub 超时，可在 VSCode 终端重试，或临时开 Clash 走代理（`git config --global http.proxy http://127.0.0.1:7897`，用完 `--unset` 清掉）。
3. **发 Release**：Releases → Draft a new release → Tag 填 `v1.2.0`、Title 填 `圣经提词器 v1.2.0`、✅ 勾 **Set as the latest release**、拖入新 exe（**ASCII 名**，中文名会被吞）、Publish。

验证：用旧版 exe 打开，看到署名红点呼吸闪烁，点它跳转到最新 Release 下载页，即更新链路打通。

> 更新检测已固定指向本仓库：`UPDATE_INFO_URL` 读 `version.json`，`UPDATE_FALLBACK_URL` 跳 `releases/latest`，无需再改。

---

## 已知坑（开发备忘）

- **pywebview 打包大体积 HTML 必须用 file:// 加载**：直接把 ~7MB 的 HTML 当字符串传给 WebView2（`NavigateToString`）在部分环境会静默失败、只露深色背景（黑屏）。`app_main.py` 已改为先写临时文件再 `file://` 加载。
- **打包别留重复 HTML**：源码只在根目录一份，`build_exe/` 下不复制，靠 `spec` 的 `datas=[('../圣经提词器.html','.')]` 读取。
- **Release 附件必须 ASCII 名**：中文名 exe 上传后会被 GitHub 截断/吞掉，始终用 `bible-teleprompter_vX.Y.Z.exe` 形式。
- **git 直连 GitHub 不稳**：见上方「提交」小节的 PAT / 凭据助手 / 代理绕行说明。

---

## 支持作者

如果这个项目对你有帮助，欢迎请我喝杯咖啡☕，让我有动力继续打磨 👇

<p align="center">
  <img src="assets/wechat-donate.png" alt="微信支付赞赏码" width="240">
  <br>
  <sub>微信扫码，随喜支持</sub>
</p>
