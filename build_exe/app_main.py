import os
import sys
import webbrowser
import tempfile
import atexit

import webview


def resource_path(rel):
    """定位打包后的资源文件。

    - Windows onefile：资源在 sys._MEIPASS（临时解压目录），直接拼即可。
    - macOS .app：PyInstaller 把资源放 Contents/Frameworks，但不同版本布局有差异，
      因此逐个候选目录探测，找不到再退回 sys._MEIPASS 本身（让报错信息更明确）。
    - 开发模式：先找脚本同目录，再回退到上级（项目根）。
    """
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        candidates = [
            os.path.join(meipass, rel),                          # Windows / macOS 常规
            os.path.join(meipass, "Resources", rel),             # macOS bundle 资源目录
            os.path.join(meipass, os.pardir, "Resources", rel),  # macOS Contents/Resources
            os.path.join(meipass, os.pardir, rel),
        ]
        for cand in candidates:
            if os.path.exists(cand):
                return cand
        return candidates[0]

    here = os.path.dirname(os.path.abspath(__file__))
    cand = os.path.join(here, rel)
    if os.path.exists(cand):
        return cand
    return os.path.join(os.path.dirname(here), rel)  # build_exe/../ = 项目根


class Api:
    """暴露给网页的桥接：点击签名「下载最新版」时用系统默认浏览器打开链接。"""
    def open_url(self, url):
        try:
            webbrowser.open(str(url))
        except Exception:
            pass


def main():
    html_path = resource_path("圣经提词器.html")

    # 把 HTML 写到临时文件，用 file:// 加载。
    # 直接把 ~7MB 的 HTML 当作字符串传给 WebView2(NavigateToString) 在部分环境会静默失败、
    # 只露出深色背景（看起来像黑屏）。改走 file:// 与 Edge 渲染同一套路径，最稳妥。
    tmp = tempfile.NamedTemporaryFile(
        mode="w", suffix=".html", encoding="utf-8",
        delete=False, dir=tempfile.gettempdir()
    )
    with open(html_path, encoding="utf-8") as f:
        tmp.write(f.read())
    tmp.close()
    atexit.register(lambda: os.path.exists(tmp.name) and os.remove(tmp.name))

    webview.create_window(
        "圣经提词器",
        url="file://" + tmp.name,
        width=1200,
        height=780,
        resizable=True,
        background_color="#1a1611",
        js_api=Api(),
    )
    webview.start()


if __name__ == "__main__":
    main()
