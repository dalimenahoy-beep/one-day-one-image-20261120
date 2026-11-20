#!/usr/bin/env python3
"""Draw the 20 November 2026 front-page poster (entry.png), 1024x1024.

Build-time tool only: the submitted program (main.ts) just copies the
finished entry.png into /output. Run: python3 make_poster.py
All layout is measured from the wrapped text so blocks never overlap.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (18, 18, 18)
BODY = (40, 38, 34)
GREY = (84, 80, 72)
FAINT = (190, 184, 170)
ACCENT = (138, 26, 26)

NOTO = "/usr/share/fonts/truetype/noto/"
SERIF_BLACK = NOTO + "NotoSerif-Black.ttf"
SERIF_BOLD = NOTO + "NotoSerif-Bold.ttf"
SERIF = NOTO + "NotoSerif-Regular.ttf"
SANS = NOTO + "NotoSans-Regular.ttf"
SANS_BOLD = NOTO + "NotoSans-Bold.ttf"
SANS_SEMI = NOTO + "NotoSans-SemiBold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def centered(draw, cx, y, text, fnt, fill=INK):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def hline(draw, x0, x1, y, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 46
R = W - M

# ---------------------------------------------------------------- masthead
hline(d, M, R, 32, 2)
name = "THE WORLD GAZETTE"
size = 96
while d.textlength(name, font=font(SERIF_BLACK, size)) > R - M - 8:
    size -= 2
centered(d, W // 2, 40, name, font(SERIF_BLACK, size))
hline(d, M, R, 148, 2)
d.text((M, 157), "ONE DAY · ONE PAGE", font=font(SANS_BOLD, 19), fill=GREY)
centered(d, W // 2, 154, "FRIDAY, 20 NOVEMBER 2026", font(SANS_BOLD, 27))
tag = "WORLD EDITION"
d.text((R - d.textlength(tag, font=font(SANS_BOLD, 19)), 157), tag,
       font=font(SANS_BOLD, 19), fill=GREY)
hline(d, M, R, 184, 5)
hline(d, M, R, 191, 1)

# ---------------------------------------------------------------- lead story
y = 202
d.text((M, y), "THE HAGUE  ·  INTERNATIONAL COURT OF JUSTICE",
       font=font(SANS_BOLD, 21), fill=ACCENT)
y += 30
for line in ("WORLD COURT: MYANMAR", "GUILTY OF GENOCIDE"):
    d.text((M, y), line, font=font(SERIF_BLACK, 64), fill=INK)
    y += 63
y += 8

text_w = 560
lead_body = (
    "In a landmark 9–6 verdict, the UN's top court ruled that Myanmar "
    "committed genocide against the Rohingya in the 2017 clearance "
    "operations that killed some 10,000 people — the first time a state "
    "has been held responsible for genocide at the court."
)
body_end = para(d, M, y, lead_body, font(SERIF, 23), text_w, 30)

# courthouse motif, right of the lead text
bx0, bx1 = M + text_w + 34, R
by0, by1 = y, y + 128
d.rectangle([bx0, by0, bx1, by1], outline=INK, width=2)
cx = (bx0 + bx1) // 2
d.polygon([(cx - 110, by0 + 40), (cx + 110, by0 + 40), (cx, by0 + 10)], outline=INK, width=3)
d.line([(bx0 + 16, by0 + 48), (bx1 - 16, by0 + 48)], fill=INK, width=3)
for i in range(5):
    px = bx0 + 32 + i * 50
    d.rectangle([px, by0 + 55, px + 13, by0 + 100], outline=INK, width=3)
d.line([(bx0 + 16, by0 + 107), (bx1 - 16, by0 + 107)], fill=INK, width=3)
d.line([(bx0 + 10, by0 + 116), (bx1 - 10, by0 + 116)], fill=INK, width=3)
cap_y = by1 + 8
centered(d, cx, cap_y, "The Peace Palace, The Hague", font(SANS, 17), fill=GREY)
centered(d, cx, cap_y + 22, "Verdict 9–6 · Case brought by The Gambia",
         font(SANS_BOLD, 17))

lead_end = max(body_end, cap_y + 46) + 10
hline(d, M, R, lead_end, 3)

# ---------------------------------------------------------------- story grid
stories = [
    ("INDIA · WEATHER",
     "Cyclone Akvan: 300,000 evacuated",
     "423 rescue teams deploy across Odisha as the storm closes in on "
     "India's east coast."),
    ("MIDDLE EAST · GULF",
     "Houthis claim strikes on Saudi targets",
     "A tanker burns after hitting a mine near the Strait of Hormuz as "
     "Gulf tensions flare."),
    ("WASHINGTON · IRAN",
     "Trump puts Iran decision off to 2027",
     "\u201cSee what happens after January 1\u201d — no new US strikes on "
     "Iran this year."),
    ("EUROPE · UKRAINE",
     "Europe ready for talks with Russia",
     "Leaders say they are ready to negotiate with Moscow on ending "
     "the war in Ukraine."),
    ("SPACE · NASA",
     "Voyager 1 reaches one light-day",
     "The 1977 probe is so far away that its signals now take a full "
     "day to reach Earth."),
    ("MARKETS · TAIWAN",
     "Taiwan curbs short-selling",
     "Five measures unveiled after shares slid 5,248 points in three "
     "straight sessions."),
]

KICK = font(SANS_BOLD, 16)
HEAD = font(SERIF_BOLD, 24)
BODYF = font(SANS, 17)
gap = 22
col_w = (R - M - 2 * gap) // 3
gy = lead_end + 14
for row in range(2):
    row_h = 0
    for col in range(3):
        kicker, head, body = stories[row * 3 + col]
        x = M + col * (col_w + gap)
        yy = gy
        d.text((x, yy), kicker, font=KICK, fill=ACCENT)
        yy += 22
        yy = para(d, x, yy, head, HEAD, col_w, 29)
        yy += 3
        yy = para(d, x, yy, body, BODYF, col_w, 22, fill=BODY)
        row_h = max(row_h, yy - gy)
        if col < 2:
            vx = x + col_w + gap // 2
            d.line([(vx, gy + 2), (vx, gy + row_h)], fill=FAINT, width=1)
    gy += row_h + 11
    if row == 0:
        hline(d, M, R, gy - 6, 1, fill=FAINT)

# ---------------------------------------------------------------- briefs strip
hline(d, M, R, gy + 2, 3)
by = gy + 13
d.text((M, by), "ALSO TODAY", font=font(SANS_BOLD, 19), fill=ACCENT)
briefs = (
    "Japan's Hayabusa2 probe gives up its asteroid landing after engine "
    "trouble  ·  GTA VI sales pass $1.8 billion days after launch  ·  "
    "Genoa airport halts flights over unidentified drones"
)
brief_end = para(d, M + 126, by - 2, briefs, font(SANS_SEMI, 19), R - M - 126, 23)

# ---------------------------------------------------------------- footer
hline(d, M, R, H - 42, 2)
centered(d, W // 2, H - 34, "The day's world news, on one page — Friday, 20 November 2026",
         font(SANS, 17), fill=GREY)

assert brief_end < H - 50, f"layout overflow: briefs end at {brief_end}"
img.save("/home/hatch/workspace/makefun/news-image-20261120-repo/entry.png", optimize=True)
print("saved entry.png; briefs end at", brief_end)
