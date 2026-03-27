#!/usr/bin/env python3
"""
Inpainting: Replace Japanese text with Traditional Chinese in landing page images.
Modifies ONLY text regions, keeping all other image content intact.
"""

from PIL import Image, ImageDraw, ImageFont
import os

BASE = '/Users/jiae/Documents/taiwan landing page/assets/img/'
TW   = '/Users/jiae/Documents/taiwan landing page/assets/img/tw/'
FONT = '/System/Library/Fonts/STHeiti Medium.ttc'

# Verified background/text colors
BLUE  = (141, 171, 216, 255)   # LINE notification header blue
WHITE = (255, 255, 255, 255)
DARK  = (55,  44,  119, 255)   # #372C77 dark navy (original text color)

def load(path):
    return Image.open(path).convert('RGBA')

def fnt(size):
    return ImageFont.truetype(FONT, size)

def paint(draw, img, box, bg, text, fs, color, align='left', px=8, py=0):
    """Fill box with bg color and draw text."""
    x0, y0, x1, y1 = box
    x0, y0 = max(0, x0-2), max(0, y0-2)
    x1, y1 = min(img.width-1, x1+2), min(img.height-1, y1+2)
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


# ─── 1. experience_headline.png (598×180) ────────────────────────────────────
# "無料体験でできること" → "免費體驗能做什麼" (white text on yellow ribbon)
def do_experience_headline():
    print('Processing: experience_headline.png')
    img  = load(BASE + 'experience_headline.png')
    draw = ImageDraw.Draw(img)
    YELLOW = (255, 206, 51, 255)   # sampled from image
    # Cover the full text area in the center of the ribbon
    paint(draw, img, (30, 28, 568, 152), YELLOW, '免費體驗能做什麼', 52, WHITE, 'center')
    save(img, TW + 'experience_headline.png')


# ─── 2. experience03.png (600×387) ───────────────────────────────────────────
# "最大30%割引" → "最多30%折扣"  (white text on pink ticket)
# "ウェルカムクーポン" → "歡迎優惠券"  (white text on teal band)
def do_experience03():
    print('Processing: experience03.png')
    img  = load(BASE + 'experience03.png')
    draw = ImageDraw.Draw(img)

    # Sample pink from ticket area, teal from bottom band
    PINK = img.getpixel((280, 160))   # hot pink ticket
    TEAL = img.getpixel((300, 340))   # teal = (65, 168, 174, 255)

    # Pink ticket text: two lines centered in ticket area
    paint(draw, img, (90, 98, 420, 175),  PINK, '最多',    44, WHITE, 'center')
    paint(draw, img, (90, 175, 420, 255), PINK, '30%折扣', 44, WHITE, 'center')

    # Teal bottom band
    paint(draw, img, (22, 308, 578, 382), TEAL, '歡迎優惠券', 34, WHITE, 'center')

    save(img, TW + 'experience03.png')


# ─── 3. about_slide03-01.png (800×1366) ──────────────────────────────────────
# Full LINE notification mockup with Japanese text
# Pixel-exact coordinates verified by scanning
def do_slide03_01():
    print('Processing: about_slide03-01.png')
    img  = load(BASE + 'about_slide03-01.png')
    draw = ImageDraw.Draw(img)

    # ① "トド英語" header  (blue bg, y=168-202, x=337-483)
    paint(draw, img, (335, 165, 495, 206), BLUE, '都都英語', 26, DARK, 'left')

    # ② "学習お知らせが到着しました！" speech bubble  (white bg, y=479-508)
    paint(draw, img, (140, 475, 610, 512), WHITE, '學習通知已送達！', 22, DARK, 'left')

    # ③─⑦ First white card – Jenny's study data  (white bg)
    paint(draw, img, (130, 609, 300, 643), WHITE, 'Jenny',              22, DARK, 'left')
    paint(draw, img, (130, 661, 585, 697), WHITE, '學習等級：等級G Unit21', 20, DARK, 'left')
    paint(draw, img, (130, 714, 415, 751), WHITE, '學習日：9月13日',      20, DARK, 'left')
    paint(draw, img, (130, 767, 450, 804), WHITE, '開始時間：20:05',      20, DARK, 'left')
    paint(draw, img, (130, 821, 385, 857), WHITE, '學習時間：35分鐘',     20, DARK, 'left')

    # ⑧ Second white card  (white bg)
    paint(draw, img, (133, 958, 530, 995), WHITE, '學習了以下內容。',      20, DARK, 'left')
    # Lines 9-13 use English + CJK counters valid in both JP/TW → keep as-is
    # (Daily Courses 2個、Free Choice 1個、Videos 1本、Books 5冊、Pet Quiz)

    save(img, TW + 'about_slide03-01.png')


# ─── 4. experience01.png (600×441) ───────────────────────────────────────────
# Same LINE notification content as slide03-01 but at smaller scale
# Notification panel: x≈270-580, occupies right portion alongside game screenshot
def do_experience01():
    print('Processing: experience01.png')
    img  = load(BASE + 'experience01.png')
    draw = ImageDraw.Draw(img)
    W, H = img.size  # 600×441

    # Scale ratio vs about_slide03-01 (800×1366)
    # Notification height in slide03-01: ~y=93 to ~y=1100  → 1007px
    # Notification height in experience01: ~y=35 to ~y=430 → 395px
    # scale ≈ 395/1007 ≈ 0.392; notification x offset ≈ 270px

    # Verified reference points (from pixel scan):
    # Blue header: y=35-103;  speech bubble: y=105-140;
    # Card1: y=155-270;  Card2: y=285-405;  Blue footer: y=405-440

    # ① "トド英語" in header
    # header blue zone: y=35-103; 'トド英語' would be ~y=50-78
    NOTIF_X0 = 270
    paint(draw, img, (NOTIF_X0+45, 48, NOTIF_X0+200, 82), BLUE, '都都英語', 18, DARK, 'left')

    # ② Bubble "学習お知らせが到着しました！"  (white, y=107-138)
    paint(draw, img, (NOTIF_X0+5, 107, W-15, 141), WHITE, '學習通知已送達！', 15, DARK, 'left')

    # ③ Card 1 text lines  (white bg, y=155-270, ~23px/line)
    paint(draw, img, (NOTIF_X0+5, 158, NOTIF_X0+130, 180), WHITE, 'Jenny',                 14, DARK, 'left')
    paint(draw, img, (NOTIF_X0+5, 180, W-15,          202), WHITE, '學習等級：等級G Unit21', 13, DARK, 'left')
    paint(draw, img, (NOTIF_X0+5, 202, W-15,          222), WHITE, '學習日：9月13日',        13, DARK, 'left')
    paint(draw, img, (NOTIF_X0+5, 222, W-15,          243), WHITE, '開始時間：20:05',        13, DARK, 'left')
    paint(draw, img, (NOTIF_X0+5, 243, W-15,          265), WHITE, '學習時間：35分鐘',       13, DARK, 'left')

    # ④ Card 2 text lines  (white bg, y=285-405, ~23px/line)
    paint(draw, img, (NOTIF_X0+5, 288, W-15, 310), WHITE, '學習了以下內容。', 13, DARK, 'left')
    # Remaining lines use mixed EN/CJK OK for TW – keep as-is

    save(img, TW + 'experience01.png')


# ─── 5. about_slide03-02.png (800×1366) ──────────────────────────────────────
# Weekly calendar app UI with Japanese text elements
def do_slide03_02():
    print('Processing: about_slide03-02.png')
    img  = load(BASE + 'about_slide03-02.png')
    draw = ImageDraw.Draw(img)
    W    = img.width  # 800

    # Sample background colors
    BG_HEADER = img.getpixel((400, 50))    # light gray top area
    BTN_BG    = img.getpixel((600, 143))   # button background (white)
    BTN_TXT   = (100, 100, 220, 255)       # purple button text color (approx)
    LINK_CLR  = (100, 100, 220, 255)       # link text color
    CAL_BG    = WHITE
    CAL_TXT   = DARK

    # ① "料金プラン" button (top-right) → "付費方案"
    # y=120-158, button roughly x=530-740
    # Sample button bg and text color
    BTN_BG2 = img.getpixel((560, 140))
    BTN_TXT2 = img.getpixel((590, 140))
    paint(draw, img, (525, 118, 742, 162), BTN_BG2, '付費方案', 22, BTN_TXT2, 'center')

    # ② "週間学習内容" → "週間學習內容"  (y=467-500, x=81-300)
    # ③ "学習進度をみる" link → "查看學習進度"  (y=467-500, x=450-695)
    TXT_BG = img.getpixel((200, 483))
    TXT_CLR = img.getpixel((150, 483))
    LINK_BG = img.getpixel((560, 483))
    LINK_COL = img.getpixel((520, 483))
    paint(draw, img, (79, 463, 420, 504), TXT_BG,  '週間學習內容', 24, TXT_CLR,  'left')
    paint(draw, img, (435, 463, 700, 504), LINK_BG, '查看學習進度', 20, LINK_COL, 'right', px=8)

    # ④ Calendar title "2022年4月3週目" → "2022年4月第3週"  (y=608-637, x=149-650)
    CAL_HDR_BG  = img.getpixel((400, 622))
    CAL_HDR_TXT = img.getpixel((380, 622))
    paint(draw, img, (148, 604, 660, 641), CAL_HDR_BG, '2022年4月第3週', 22, CAL_HDR_TXT, 'center')

    # ⑤ Day-of-week headers "月火水木金土日" → "一二三四五六日"  (y=734-754)
    # 7 cells from x≈75 to x≈725, each ~93px wide
    days_tw = ['一', '二', '三', '四', '五', '六', '日']
    # Sat=red, Sun=red; others dark
    day_colors = [CAL_TXT]*5 + [(180, 0, 0, 255)]*2
    cell_w = (725 - 75) // 7
    DAY_BG = img.getpixel((200, 744))
    for i, (day, col) in enumerate(zip(days_tw, day_colors)):
        cx0 = 75 + i * cell_w
        cx1 = cx0 + cell_w
        paint(draw, img, (cx0, 730, cx1, 758), DAY_BG, day, 18, col, 'center')

    # ⑥ "詳しくはこちら" button → "點此查看詳情"  (y=1248-1315, x=296-712)
    BTN_BG3  = img.getpixel((500, 1280))
    BTN_TXT3 = img.getpixel((400, 1280))
    paint(draw, img, (293, 1244, 718, 1319), BTN_BG3, '點此查看詳情', 32, BTN_TXT3, 'center')

    save(img, TW + 'about_slide03-02.png')


# ─── 6. about_slide01-03.png (700×370) ───────────────────────────────────────
# Game screenshot with Japanese UI labels
# Creates tw/ version
def do_slide01_03():
    print('Processing: about_slide01-03.png')
    img  = load(BASE + 'about_slide01-03.png')
    draw = ImageDraw.Draw(img)

    # ① "日本語" language selector (top-right, x≈608-690, y≈8-35)
    # Background: orange/yellow (255, 177, 51); text: teal
    LANG_BG  = img.getpixel((555, 22))   # orange bg
    LANG_TXT = img.getpixel((640, 22))   # teal text
    paint(draw, img, (533, 6, 695, 37), LANG_BG, '繁體中文', 14, LANG_TXT, 'center')

    # ② "きょうのどうが" (Today's video label) – white text on pink/dark bg
    # Approx region: x=6-185, y=297-322
    VID_BG  = img.getpixel((15, 310))    # dark purple bg
    paint(draw, img, (4, 296, 190, 323), VID_BG, '今日影片', 14, WHITE, 'left')

    # ③ "じゃないおばけ" (video title) – white text on dark bg
    # Approx region: x=6-185, y=323-350
    paint(draw, img, (4, 323, 190, 352), VID_BG, '不是幽靈', 13, WHITE, 'left')

    save(img, TW + 'about_slide01-03.png')


# ─── Run all ──────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print('Starting inpainting...\n')
    do_experience_headline()
    do_experience03()
    do_slide03_01()
    do_experience01()
    do_slide03_02()
    do_slide01_03()
    print('\nAll done.')
