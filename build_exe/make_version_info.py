# -*- coding: utf-8 -*-
"""
从项目根 version.json 读取版本号，自动刷新 build_exe/version_info.txt。

目的：让「版本号」只有一个真源（version.json），避免手写时漏改——
之前就出现过 exe 属性里还写着 1.1.0.0 而实际已是 1.2.0 的情况。

version_info.txt 只影响 Windows exe 的「文件属性 → 详细信息」，
不影响更新提醒（更新提醒读的是 HTML 里的 APP_VERSION），
但保持它一致更专业。

用法：
    本地：python build_exe/make_version_info.py
    CI  ：release.yml 里打包前自动调用
"""
import json
import os
import re
import sys

# Windows 控制台是 cp1252，中文 print 会 UnicodeEncodeError 中断构建
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VJSON = os.path.join(ROOT, "version.json")
VINFO = os.path.join(HERE, "version_info.txt")


def main():
    with open(VJSON, encoding="utf-8") as f:
        ver = json.load(f)["version"]          # 如 "1.2.0"

    parts = [int(x) for x in ver.split(".")[:3]]
    while len(parts) < 3:
        parts.append(0)
    tup = "(%d, %d, %d, 0)" % tuple(parts)     # (1, 2, 0, 0)
    quad = ".".join(str(p) for p in parts) + ".0"   # 1.2.0.0

    src = open(VINFO, encoding="utf-8").read()
    src = re.sub(r"filevers=\([^)]*\)", "filevers=" + tup, src)
    src = re.sub(r"prodvers=\([^)]*\)", "prodvers=" + tup, src)
    src = re.sub(
        r"StringStruct\(u'FileVersion', u'[^']*'\)",
        "StringStruct(u'FileVersion', u'%s')" % quad, src)
    src = re.sub(
        r"StringStruct\(u'ProductVersion', u'[^']*'\)",
        "StringStruct(u'ProductVersion', u'%s')" % quad, src)
    src = re.sub(
        r"StringStruct\(u'OriginalFilename', u'[^']*'\)",
        "StringStruct(u'OriginalFilename', u'bible-teleprompter_v%s.exe')" % ver, src)

    with open(VINFO, "w", encoding="utf-8") as f:
        f.write(src)

    # 纯 ASCII 输出：Windows 控制台是 GBK(936)，中文会变乱码
    print("[version_info] synced to %s (filevers=%s, FileVersion=%s)" % (ver, tup, quad))


if __name__ == "__main__":
    main()
