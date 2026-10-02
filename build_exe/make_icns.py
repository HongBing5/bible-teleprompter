# -*- coding: utf-8 -*-
"""
从 logo.png 生成 macOS 应用图标 app.icns。

Windows 用 .ico，macOS 用 .icns，两者都由同一个 logo.png 派生，
保证两个平台的图标完全一致。

用法：
    本地：python build_exe/make_icns.py
    CI  ：build_mac.sh 第一步自动调用
"""
import os
import sys

from PIL import Image

# Windows 控制台是 cp1252，中文 print 会 UnicodeEncodeError 中断构建
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "logo.png")
OUT = os.path.join(HERE, "app.icns")


def main():
    im = Image.open(SRC).convert("RGBA")

    # 补成正方形（图标必须是方的，否则 macOS 会拉伸变形）
    w, h = im.size
    side = max(w, h)
    if (w, h) != (side, side):
        canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        canvas.paste(im, ((side - w) // 2, (side - h) // 2))
        im = canvas

    # Pillow 写 .icns 支持的尺寸有限，512 是清晰度与兼容性的最佳平衡
    if side > 512:
        im = im.resize((512, 512), Image.LANCZOS)

    # 纯 ASCII 输出：Windows 控制台是 GBK(936)，中文会变乱码
    im.save(OUT)
    print("[icns] %s generated %s" % (OUT, im.size))


if __name__ == "__main__":
    main()
