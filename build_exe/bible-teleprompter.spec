# -*- mode: python ; coding: utf-8 -*-
import json
import os

from PyInstaller.utils.hooks import collect_all

# 版本号唯一真源 = 项目根 version.json。
# 这样升版本只需改 version.json，exe 文件名自动跟上，不会漏改。
# （SPECPATH 由 PyInstaller 注入；不同版本可能给的是目录或文件路径，这里兼容两种）
_SPEC_PATH = os.path.abspath(SPECPATH)
_SPEC_DIR = _SPEC_PATH if os.path.isdir(_SPEC_PATH) else os.path.dirname(_SPEC_PATH)
_ROOT = os.path.dirname(_SPEC_DIR)          # build_exe/ 的上级 = 项目根
with open(os.path.join(_ROOT, "version.json"), encoding="utf-8") as _f:
    VERSION = json.load(_f)["version"]

# 直接读上级目录（项目根）的源 HTML，避免 build_exe 里再留一份重复拷贝
datas = [('../圣经提词器.html', '.')]
binaries = []
hiddenimports = []
tmp_ret = collect_all('webview')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['app_main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='bible-teleprompter_v%s' % VERSION,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app.ico'],
    version='version_info.txt',
)

