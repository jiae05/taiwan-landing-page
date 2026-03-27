#!/usr/bin/env python3
"""
Inpainting v3: pixel-precise approach.
- Only touches exact text pixels / tight bounding boxes
- Preserves all background, characters, layout
"""

from PIL import Image, ImageDraw, ImageFont
import os

BASE = '/Users/jiae/Documents/taiwan landing page/assets/img/'
TW   = '/Users/jiae/Documents/taiwan landing page/assets/img/tw/'
FONT = '/System/Library/Fonts/STHeiti Medium.ttc'

WHITE = (255, 255, 255, 255)
DARK  = (48,  43,  80,  255)

def load(path):
    return Image.open(path).convert('RGBA')

def fnt(size):
    return ImageFont.truetype(FONT, size)

def save(img, path):
    img.convert('RGB').save(path, 'PNG')
    print(f'  ✓ {os.path.basename(path)}')

def paint(draw, img, box, bg, text, fs, color, align='center', px=8, py_off=0):
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=bg)
    f = fnt(fs)
    tb = draw.textbbox((0, 0), text, font=f)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    bw, bh = x1-x0, y1-y0
    ty = y0 + max(0, (bh-th)//2) + py_off
    if align == 'center':
        tx = x0 + max(0, (bw-tw)//2)
    elif align == 'right':
        tx = x1 - tw - px
    else:
        tx = x0 + px
    draw.text((tx, ty), text, fill=color, font=f)


# ─── 1. experience_headline.png ───────────────────────────────────────────────
def do_experience_headline():
    print('Processing: experience_headline.png')
    img  = load(BASE + 'experience_headline.png')
    draw = ImageDraw.Draw(img)

    # Find tight white-text bbox (text spans y=39-101, x=97-516 from scan)
    # Sample yellow from top-center of ribbon (above text, solid yellow)
    YELLOW = img.getpixel((298, 32))[:3] + (255,)   # yellow at ribbon center, no text

    # Tight fill: just the text region, not extending to ribbon fold decorations
    paint(draw, img, (92, 35, 522, 105), YELLOW, '免費體驗能做什麼', 52, WHITE, 'center')
    save(img, TW + 'experience_headline.png')


# ─── 2. experience03.png ──────────────────────────────────────────────────────
def do_experience03():
    print('Processing: experience03.png')
    img  = load(BASE + 'experience03.png')
    draw = ImageDraw.Draw(img)

    PINK = (247, 65, 156, 255)
    TEAL = (65,  168, 174, 255)

    # --- Pink ticket: fill row-by-row only within the pink shape ---
    # For each row, find leftmost/rightmost pink pixel, fill only that span.
    # This preserves the gray circle background and dog illustration.
    for py in range(25, 165):
        left = right = None
        for px in range(80, 480):
            r, g, b, a = img.getpixel((px, py))
            if a < 100:
                continue
            # Pink: high red, low green, mid blue
            if r > 200 and g < 170 and b > 90:
                if left is None:
                    left = px
                right = px
        if left is not None and right > left:
            # Fill the pink span (covers old white text + pink bg)
            draw.line([(left, py), (right, py)], fill=PINK, width=1)

    # Draw two-line Chinese text centered in the ticket
    # Ticket full extent: x=211-434, y=47-158 (from pixel scan)
    # Line 1: "最多"
    f44 = fnt(44)
    TICKET_X0, TICKET_X1 = 211, 434
    TICKET_Y0, TICKET_Y1 = 47, 100
    tb = draw.textbbox((0,0), '最多', font=f44)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    tx = TICKET_X0 + (TICKET_X1 - TICKET_X0 - tw) // 2
    ty = TICKET_Y0 + (TICKET_Y1 - TICKET_Y0 - th) // 2
    draw.text((tx, ty), '最多', fill=WHITE, font=f44)

    # Line 2: "30%折扣"
    TICKET_Y0b, TICKET_Y1b = 100, 158
    tb = draw.textbbox((0,0), '30%折扣', font=f44)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    tx = TICKET_X0 + (TICKET_X1 - TICKET_X0 - tw) // 2
    ty = TICKET_Y0b + (TICKET_Y1b - TICKET_Y0b - th) // 2
    draw.text((tx, ty), '30%折扣', fill=WHITE, font=f44)

    # --- Teal band: tight fill around just the text ---
    # Text bbox from scan: y=250-310, x=170-428
    # Pad by 6px; teal band bg is solid
    paint(draw, img, (165, 246, 432, 315), TEAL, '歡迎優惠券', 34, WHITE, 'center')

    save(img, TW + 'experience03.png')


# ─── 3. about_slide03-01.png ─────────────────────────────────────────────────
def do_slide03_01():
    print('Processing: about_slide03-01.png')
    img  = load(BASE + 'about_slide03-01.png')
    draw = ImageDraw.Draw(img)
    BLUE = (141, 171, 216, 255)

    # ① "トド英語" header (blue bg)
    paint(draw, img, (335, 165, 510, 208), BLUE, '都都英語', 26, DARK, 'left')

    # ② Speech bubble
    paint(draw, img, (140, 475, 610, 512), WHITE, '學習通知已送達！', 22, DARK, 'left')

    # ③–⑦ Card 1
    paint(draw, img, (130, 609, 300, 643), WHITE, 'Jenny',               22, DARK, 'left')
    paint(draw, img, (130, 661, 590, 697), WHITE, '學習等級：等級G Unit21', 20, DARK, 'left')
    paint(draw, img, (130, 714, 420, 751), WHITE, '學習日：9月13日',        20, DARK, 'left')
    paint(draw, img, (130, 767, 455, 804), WHITE, '開始時間：20:05',        20, DARK, 'left')
    paint(draw, img, (130, 821, 390, 857), WHITE, '學習時間：35分鐘',        20, DARK, 'left')

    # ⑧ Card 2
    paint(draw, img, (133, 958, 535, 995), WHITE, '學習了以下內容。',        20, DARK, 'left')

    save(img, TW + 'about_slide03-01.png')


# ─── 4. experience01.png ─────────────────────────────────────────────────────
def do_experience01():
    print('Processing: experience01.png')
    img  = load(BASE + 'experience01.png')
    draw = ImageDraw.Draw(img)
    BLUE = (141, 171, 216, 255)
    W    = img.width   # 600

    NX = 270  # notification panel left edge

    # ① Header
    paint(draw, img, (NX+45, 48, NX+200, 82), BLUE, '都都英語', 18, DARK, 'left')

    # ② Speech bubble
    paint(draw, img, (NX+5, 107, W-15, 141), WHITE, '學習通知已送達！', 15, DARK, 'left')

    # ③ Card 1
    paint(draw, img, (NX+5, 158, NX+130, 180), WHITE, 'Jenny',                  14, DARK, 'left')
    paint(draw, img, (NX+5, 180, W-15,   202), WHITE, '學習等級：等級G Unit21',   13, DARK, 'left')
    paint(draw, img, (NX+5, 202, W-15,   222), WHITE, '學習日：9月13日',          13, DARK, 'left')
    paint(draw, img, (NX+5, 222, W-15,   243), WHITE, '開始時間：20:05',          13, DARK, 'left')
    paint(draw, img, (NX+5, 243, W-15,   265), WHITE, '學習時間：35分鐘',         13, DARK, 'left')

    # ④ Card 2
    paint(draw, img, (NX+5, 288, W-15, 310), WHITE, '學習了以下內容。', 13, DARK, 'left')

    save(img, TW + 'experience01.png')


# ─── 5. about_slide03-02.png ─────────────────────────────────────────────────
def do_slide03_02():
    print('Processing: about_slide03-02.png')
    img  = load(BASE + 'about_slide03-02.png')
    draw = ImageDraw.Draw(img)

    APP_BG  = (246, 246, 248, 255)   # verified app background color
    WHITE4  = (255, 255, 255, 255)
    RED     = (180,   0,   0, 255)
    LINK_CLR = (100, 100, 220, 255)  # purple link color

    # ① "料金プラン" button → "付費方案"
    # Sample button bg/text from original
    BTN_BG  = img.getpixel((640, 140))[:3] + (255,)
    BTN_TXT = img.getpixel((620, 140))[:3] + (255,)
    # Cover wider than needed to catch all anti-aliased text
    paint(draw, img, (406, 116, 724, 162), BTN_BG, '付費方案', 22, BTN_TXT, 'center')

    # ② "週間学習内容" → "週間學習內容"
    # Section text is at y=467-501. Background is WHITE in this area (from scan y=455-465)
    # Cover ONLY the left text (x=88-290) with white, redraw
    paint(draw, img, (85, 462, 298, 506), WHITE4, '週間學習內容', 24, DARK, 'left')

    # ③ "学習進度をみる" → "查看學習進度"
    # Right side of section row (x=520-695)
    paint(draw, img, (518, 462, 698, 506), WHITE4, '查看學習進度', 20, LINK_CLR, 'right', px=6)

    # ④ Calendar title
    CAL_BG  = img.getpixel((400, 622))[:3] + (255,)
    CAL_TXT = img.getpixel((310, 622))[:3] + (255,)
    paint(draw, img, (148, 604, 660, 641), CAL_BG, '2022年4月第3週', 22, CAL_TXT, 'center')

    # ⑤ Day-of-week headers
    # Pixel scan confirmed: day names are at y=691-714, x≈68-728
    # Character x-centers (from scan at y=710): 150,233,315,399,482,565,647
    day_centers = [150, 233, 315, 399, 482, 565, 647]
    days_tw     = ['一', '二', '三', '四', '五', '六', '日']
    day_colors  = [DARK]*5 + [RED]*2

    # Cover the full day-header row
    draw.rectangle([68, 685, 728, 720], fill=APP_BG)

    # Draw each day centered at original character's x position
    f_day = fnt(18)
    for i, (day, col) in enumerate(zip(days_tw, day_colors)):
        cx = day_centers[i]
        cx0 = 68  if i == 0 else (day_centers[i-1] + cx) // 2
        cx1 = 728 if i == 6 else (cx + day_centers[i+1]) // 2
        tb = draw.textbbox((0,0), day, font=f_day)
        tw = tb[2]-tb[0]; th = tb[3]-tb[1]
        tx = cx0 + (cx1 - cx0 - tw) // 2
        ty = 685 + (35 - th) // 2
        draw.text((tx, ty), day, fill=col, font=f_day)

    # ⑥ "詳しくはこちら" → "點此查看詳情"
    # Background is white at (500,1280) and (400,1282)
    BTN2_BG  = img.getpixel((500, 1280))[:3] + (255,)
    BTN2_TXT = img.getpixel((600, 1282))[:3] + (255,)
    paint(draw, img, (292, 1244, 718, 1319), BTN2_BG, '點此查看詳情', 32, BTN2_TXT, 'center')

    save(img, TW + 'about_slide03-02.png')


# ─── 6. about_slide01-03.png ─────────────────────────────────────────────────
def do_slide01_03():
    print('Processing: about_slide01-03.png')
    img  = load(BASE + 'about_slide01-03.png')
    draw = ImageDraw.Draw(img)

    # ① Language selector "日本語" → "繁體中文"  (orange bg, top-right)
    LANG_BG  = img.getpixel((555, 22))[:3] + (255,)
    LANG_TXT = img.getpixel((640, 22))[:3] + (255,)
    paint(draw, img, (535, 5, 697, 38), LANG_BG, '繁體中文', 13, LANG_TXT, 'center')

    # Pink bar: uniform solid pink (210,53,119), x=96-207, y=265-320.
    # Play button (▶) x=105-141 — leave it intact.
    # Text region (label + time + subtitle): x=141-207.
    # Erase entire text region with solid pink, then draw Chinese two lines.
    PINK_BG = (210, 53, 119, 255)   # exact sampled pink

    # Pink bar extends x=96-292 (wider than expected).
    # Erase entire text region (right of play button) with solid pink
    draw.rectangle([141, 265, 292, 320], fill=PINK_BG)

    # Draw line 1 "今日影片" in upper portion
    f1 = fnt(11)
    tb = draw.textbbox((0,0), '今日影片', font=f1)
    th1 = tb[3]-tb[1]
    draw.text((143, 265 + (26 - th1)//2), '今日影片', fill=WHITE, font=f1)

    # Draw line 2 "不是幽靈" in lower portion
    f2 = fnt(10)
    tb = draw.textbbox((0,0), '不是幽靈', font=f2)
    th2 = tb[3]-tb[1]
    draw.text((143, 291 + (29 - th2)//2), '不是幽靈', fill=WHITE, font=f2)

    save(img, TW + 'about_slide01-03.png')


# ─── HTML update ─────────────────────────────────────────────────────────────
def update_html():
    path = '/Users/jiae/Documents/taiwan landing page/index_tw.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    old = 'src="assets/img/about_slide01-03.png"'
    new = 'src="assets/img/tw/about_slide01-03.png"'
    if old in content:
        content = content.replace(old, new)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('  ✓ index_tw.html → tw/about_slide01-03.png')
    else:
        print('  (index_tw.html already up-to-date)')


if __name__ == '__main__':
    print('Inpainting v3...\n')
    do_experience_headline()
    do_experience03()
    do_slide03_01()
    do_experience01()
    do_slide03_02()
    do_slide01_03()
    update_html()
    print('\nDone.')
