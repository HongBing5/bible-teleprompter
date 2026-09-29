# -*- coding: utf-8 -*-
"""Generate a plain, standard PDF manual for 圣经提词器 from scratch.
No external assets, Chinese via reportlab built-in CID font (STSong-Light)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, ListFlowable, ListItem)
from reportlab.lib.styles import ParagraphStyle

# Embed a real CJK font so the PDF is fully self-contained (renders on any reader).
pdfmetrics.registerFont(TTFont('CN', 'C:/Windows/Fonts/simsun.ttc', subfontIndex=0))
FONT = 'CN'

GOLD = colors.HexColor('#8a6f1e')
INK = colors.HexColor('#2b2b2b')
SOFT = colors.HexColor('#555555')
BOXBG = colors.HexColor('#f5efe2')
LINE = colors.HexColor('#d8cdb4')

P = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(P, '圣经提词器-使用说明书.pdf')

doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=20*mm, rightMargin=20*mm,
                        topMargin=18*mm, bottomMargin=18*mm,
                        title='圣经提词器 使用说明书', author='HongBing')

def style(size, color=INK, align=TA_LEFT, leading=None, space=4):
    return ParagraphStyle('s', fontName=FONT, fontSize=size, textColor=color,
                          alignment=align, leading=leading or size*1.7, spaceAfter=space)

def para(t, s): return Paragraph(t, s)
def h1(t): return para(t, style(20, GOLD, TA_CENTER, space=2))
def h2(t): return para(t, style(13.5, GOLD, space=8))
def body(t): return para(t, style(11, INK, space=6))
def soft(t): return para(t, style(10.5, SOFT, space=6))

st = []
st.append(h1('圣经提词器'))
st.append(para('使用说明书 · 版本 1.0', style(11, SOFT, TA_CENTER, space=10)))
st.append(Spacer(1, 4))

def rule():
    t = Table([['']], colWidths=[doc.width], rowHeights=[1])
    t.setStyle(TableStyle([('LINEABOVE', (0,0), (-1,-1), 0.6, GOLD)]))
    return t
st.append(rule()); st.append(Spacer(1, 10))

# 一
st.append(h2('一、软件简介'))
st.append(body('这是一款为讲道、聚会、教学等场景设计的中英双语圣经投影提词器。界面简洁、字号大，'
               '便于在投影或大屏上清晰展示经文，支持中文（和合本）与英文（KJV）一键切换。'))

# 二
st.append(h2('二、运行环境'))
env = ListFlowable([
    ListItem(soft('操作系统：Windows 10 / Windows 11'), leftIndent=6),
    ListItem(soft('运行库：需系统自带 Microsoft WebView2 运行时（Win10/11 绝大多数已自带）'), leftIndent=6),
    ListItem(soft('网络：完全离线，无需联网，断网也可正常使用'), leftIndent=6),
    ListItem(soft('安装：无需安装，双击即可打开'), leftIndent=6),
], bulletType='bullet', start='square', bulletColor=GOLD)
st.append(env)
tip1 = Table([[para('若双击后提示缺少 WebView2 运行时，请到微软官网下载安装 '
                    'Microsoft WebView2 Runtime（Evergreen 版）即可，过程约一分钟。',
                    style(10, INK))]], colWidths=[doc.width])
tip1.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BOXBG),
                          ('BOX',(0,0),(-1,-1),0.5,LINE),
                          ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
                          ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
st.append(Spacer(1, 2)); st.append(tip1)

# 三
st.append(h2('三、开始使用'))
use = ListFlowable([
    ListItem(soft('将 圣经提词器_v1.0.exe 复制到任意位置（桌面、U 盘均可）。'), leftIndent=6),
    ListItem(soft('双击该文件，稍候片刻即进入主界面，默认定位在《创世记》开头。'), leftIndent=6),
    ListItem(soft('如需快速跳到某卷某章某节，点击屏幕左上角的十字架图标打开目录。'), leftIndent=6),
], bulletType='bullet', start='square', bulletColor=GOLD)
st.append(use)

# 四
st.append(h2('四、操作快捷键'))
rows = [
    [para('操作', style(10.5, GOLD)), para('按键 / 方式', style(10.5, GOLD))],
    [para('翻节（上一节 / 下一节）', style(10.5, INK)), para('←   →', style(10.5, INK))],
    [para('翻章（上一章 / 下一章）', style(10.5, INK)), para('↑   ↓', style(10.5, INK))],
    [para('中文 / 英文 切换', style(10.5, INK)), para('L（或在目录面板右上角点击语言胶囊）', style(10.5, INK))],
    [para('打开目录', style(10.5, INK)), para('T（或点击左上角十字架图标）', style(10.5, INK))],
    [para('关闭目录', style(10.5, INK)), para('Esc', style(10.5, INK))],
]
kt = Table(rows, colWidths=[doc.width*0.42, doc.width*0.58])
kt.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(-1,0),BOXBG),
    ('LINEBELOW',(0,0),(-1,0),0.6,GOLD),
    ('GRID',(0,0),(-1,-1),0.4,LINE),
    ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
    ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
    ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white, colors.HexColor('#faf6ee')]),
]))
st.append(kt)
tip2 = Table([[para('切换经文时画面会有约 0.5 秒的柔和渐变过渡，方便投影时自然换节、不突兀。',
                    style(10, INK))]], colWidths=[doc.width])
tip2.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),BOXBG),('BOX',(0,0),(-1,-1),0.5,LINE),
                          ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
                          ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
st.append(Spacer(1, 6)); st.append(tip2)

# 五
st.append(h2('五、目录结构'))
st.append(body('目录按 旧约 / 新约 → 分类 → 书卷 → 章 → 节 三级分组，逐级展开即可精确定位到任意一节，'
               '适合快速跳转长途经文。'))

# 六
st.append(h2('六、常见问题'))
faq = ListFlowable([
    ListItem(soft('需要联网吗？ 不需要。所有经文已内置，断网也能用。'), leftIndent=6),
    ListItem(soft('可以拷给别的电脑用吗？ 可以。直接把 .exe 文件复制过去即可，不依赖任何额外文件。'), leftIndent=6),
    ListItem(soft('打开后是黑屏 / 没反应？ 多半是缺少 WebView2 运行时，按第二节安装即可。'), leftIndent=6),
    ListItem(soft('支持 Mac 或手机吗？ 本版本仅支持 Windows，暂不支持其他平台。'), leftIndent=6),
], bulletType='bullet', start='square', bulletColor=GOLD)
st.append(faq)

st.append(Spacer(1, 14))
st.append(para('© HongBing  ·  完全离线  ·  双击即用', style(10.5, GOLD, TA_CENTER, space=0)))

doc.build(st)
print('PDF written:', OUT, os.path.getsize(OUT), 'bytes')
