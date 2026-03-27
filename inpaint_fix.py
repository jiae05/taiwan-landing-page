#!/usr/bin/env python3
"""Fix pass: re-inpaint images where coordinates were off in first pass."""

from PIL import Image, ImageDraw, ImageFont
import os

BASE = '/Users/jiae/Documents/taiwan landing page/assets/img/'
TW   = '/Users/jiae/Documents/taiwan landing page/assets/img/tw/'
FONT = '/System/Library/Fonts/STHeiti Medium.ttc'

WHITE = (255, 255, 255, 255)
DARK  = (48,  43,  80,  255)   # sampled dark text color from slide03-02

def load(path):
    return Image.open(path).convert('RGBA')

def fnt(size):
    return ImageFont.truetype(FONT, size)

def paint(draw, img, box, bg, text, fs, color, align='left', px=8, py=0):
    x0, y0, x1, y1 = box
    x0, y0 = max(0, x0-1), max(0, y0-1)
    x1, y1 = min(img.width-1, x1+1), min(img.height-1, y1+1)
    draw.rectangle([x0, y0, x1, y1], fill=bg)
    f = fnt(fs)
    tb = draw.textbbox((0, 0), text, font=f)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    bw, bh = x1-x0, y1-y0
    ty = y0 + max(0, (bh-th)//2) + py
    tx = x0 + max(0, (bw-tw)//2) if align == 'center' else x0 + px
    draw.text((tx, ty), text, fill=color, font=f)

def save(img, path):
    img.convert('RGB').save(path, 'PNG')
    print(f'  ✓ {os.path.basename(path)}')


# ─── experience03.png ─────────────────────────────────────────────────────────
# Fix: use correct hot-pink color & correct ticket y range
def fix_experience03():
    print('Fixing: experience03.png')
    img  = load(BASE + 'experience03.png')
    draw = ImageDraw.Draw(img)

    PINK = (247, 65, 156, 255)   # verified hot pink at (270,70)
    TEAL = (65, 168, 174, 255)   # verified teal at (300,340)

    # Pink ticket: covers y=40-145, full ticket width x=88-432
    # Two text lines:  "最多" (top) and "30%折扣" (bottom)
    paint(draw, img, (88, 40, 432, 95),  PINK, '最多',    44, WHITE, 'center')
    paint(draw, img, (88, 95, 432, 148), PINK, '30%折扣', 44, WHITE, 'center')

    # Teal band: cover from y=262 to bottom (text can be anywhere in band)
    paint(draw, img, (20, 262, 580, 387), TEAL, '歡迎優惠券', 34, WHITE, 'center')

    save(img, TW + 'experience03.png')


# ─── about_slide03-02.png ─────────────────────────────────────────────────────
# Fix: correct button x range, day header cell positions
def fix_slide03_02():
    print('Fixing: about_slide03-02.png')
    img  = load(BASE + 'about_slide03-02.png')
    draw = ImageDraw.Draw(img)

    BG_NEAR_WHITE = (246, 246, 248, 255)  # sampled background under days

    # ① "料金プラン" button text  (text at x=608-720, y=120-156, dark on white)
    # Cover slightly wider to catch full text including anti-aliasing
    paint(draw, img, (406, 116, 724, 160), WHITE, '付費方案', 22, DARK, 'center')

    # ② "週間学習内容"  (y=467-500, x=81-350, dark on white)
    BG_TXT = img.getpixel((200, 483))
    TXT_CLR = img.getpixel((140, 484))
    paint(draw, img, (79, 463, 380, 505), BG_TXT, '週間學習內容', 24, TXT_CLR, 'left')

    # ③ "学習進度をみる" link  (y=467-500, x=450-700)
    LINK_BG  = img.getpixel((560, 483))
    LINK_COL = img.getpixel((520, 484))
    paint(draw, img, (440, 463, 705, 505), LINK_BG, '查看學習進度', 20, LINK_COL, 'right', px=6)

    # ④ Calendar title  (y=608-637, x=149-650)
    CAL_BG  = img.getpixel((400, 622))
    CAL_CLR = img.getpixel((310, 622))
    paint(draw, img, (148, 604, 660, 641), CAL_BG, '2022年4月第3週', 22, CAL_CLR, 'center')

    # ⑤ Day-of-week headers  (y=730-755, text x=138-662)
    # 7 cells, total width = 662-138 = 524px → ~74.9px/cell
    days_tw  = ['一', '二', '三', '四', '五', '六', '日']
    day_clrs = [DARK]*5 + [(180, 0, 0, 255)]*2   # Sat/Sun in red
    cell_w   = (662 - 138) // 7
    DAY_BG   = img.getpixel((200, 742))
    for i, (day, col) in enumerate(zip(days_tw, day_clrs)):
        cx0 = 138 + i * cell_w
        cx1 = cx0 + cell_w
        paint(draw, img, (cx0, 727, cx1, 758), DAY_BG, day, 18, col, 'center')

    # ⑥ "詳しくはこちら" button  (y=1248-1315)
    BTN_BG  = img.getpixel((500, 1282))
    BTN_CLR = img.getpixel((400, 1282))
    paint(draw, img, (292, 1244, 718, 1319), BTN_BG, '點此查看詳情', 32, BTN_CLR, 'center')

    save(img, TW + 'about_slide03-02.png')


# ─── about_slide01-03.png ─────────────────────────────────────────────────────
# Fix: correct positions for Japanese text in game screenshot
def fix_slide01_03():
    print('Fixing: about_slide01-03.png')
    img  = load(BASE + 'about_slide01-03.png')
    draw = ImageDraw.Draw(img)

    # ① Language selector "日本語" → "繁體中文"
    # At x=610-690, y=8-35; background orange (255,177,51)
    LANG_BG  = img.getpixel((555, 22))   # orange
    LANG_TXT = img.getpixel((640, 22))   # teal text
    paint(draw, img, (535, 5, 697, 38), LANG_BG, '繁體中文', 13, LANG_TXT, 'center')

    # ② "きょうのどうが" – the label is in the pink video section
    # Pink section: x≈95-190, y≈280-330 region
    # The label text (white) sits at bottom of the section around y=310-335
    PINK_BG = img.getpixel((130, 313))   # solid pink at the text row
    # Cover the text label area and redraw
    paint(draw, img, (93, 308, 190, 333), PINK_BG, '今日影片', 13, WHITE, 'left', px=4)

    # ③ "じゃないおばけ" video subtitle
    # Below the pink section, lighter background, approximate y=333-358
    DARK_BG = img.getpixel((130, 345))
    paint(draw, img, (93, 332, 190, 360), DARK_BG, '不是幽靈', 12, WHITE, 'left', px=4)

    save(img, TW + 'about_slide01-03.png')


# ─── update index_tw.html to reference tw/about_slide01-03.png ────────────────
def update_html():
    html_path = '/Users/jiae/Documents/taiwan landing page/index_tw.html'
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    old = 'src="assets/img/about_slide01-03.png"'
    new = 'src="assets/img/tw/about_slide01-03.png"'
    if old in content:
        content = content.replace(old, new)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('  ✓ index_tw.html updated: about_slide01-03 → tw/ version')
    else:
        print('  (index_tw.html already up-to-date)')


if __name__ == '__main__':
    print('Fix pass...\n')
    fix_experience03()
    fix_slide03_02()
    fix_slide01_03()
    update_html()
    print('\nDone.')
