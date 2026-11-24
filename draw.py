#!/usr/bin/env python3
"""Draw the 23 November 2026 world-news front page (1024x1024 PNG).

Written fresh for make.fun news-image-20261123. Every story was verified
against news first reported on Monday 23 November 2026 (Reuters/AP, CNN,
CNA, Xinhua, SCMP, FMT, The Economic Times). Layout follows the winning
newspaper formula: serif masthead with the date as hero, a key-numbers
strip, three illustrated lead stories, nine small cards each with its own
visual, and a world map with pins plus a briefs column.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

PAPER = (245, 239, 226)
PAPER2 = (251, 247, 238)
INK = (28, 25, 22)
RED = (178, 32, 38)
RED_DK = (138, 20, 26)
NAVY = (26, 44, 76)
BLUE = (40, 86, 140)
TEAL = (26, 112, 98)
GOLD = (200, 144, 34)
GREY = (98, 92, 82)
LINE = (182, 172, 152)
CARD = (253, 250, 241)
OCEAN = (198, 218, 230)
LAND = (228, 212, 174)
FD = "/usr/share/fonts/truetype/dejavu/"

def _font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)

def serif_b(s):
    return _font("DejaVuSerif-Bold.ttf", s)

def serif(s):
    return _font("DejaVuSerif.ttf", s)

def sans_b(s):
    return _font("DejaVuSans-Bold.ttf", s)

def sans(s):
    return _font("DejaVuSans.ttf", s)

def wrap(dr, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if dr.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def block(dr, x, y, text, fnt, color, max_w, leading):
    for ln in wrap(dr, text, fnt, max_w):
        dr.text((x, y), ln, font=fnt, fill=color)
        y += leading
    return y

def tag(dr, x, y, label, color=RED):
    f = sans_b(13)
    w = dr.textlength(label, font=f) + 14
    dr.rounded_rectangle([x, y, x + w, y + 20], radius=3, fill=color)
    dr.text((x + 7, y + 3), label, font=f, fill=(255, 255, 255))
    return y + 20

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")
M = 28

# ---------------- masthead ----------------
d.text((M, 14), "THE WORLD IN ONE PAGE", font=sans_b(15), fill=RED)
right = "MONDAY EDITION"
d.text((W - M - d.textlength(right, font=sans_b(15)), 14), right,
       font=sans_b(15), fill=INK)
d.line([(M, 38), (W - M, 38)], fill=INK, width=2)
title = "MONDAY 23 NOVEMBER 2026"
tf = serif_b(52)
d.text(((W - d.textlength(title, font=tf)) / 2, 46), title, font=tf, fill=INK)
sub = "The day's world news \u2014 in one picture"
d.text(((W - d.textlength(sub, font=serif(19))) / 2, 108), sub,
       font=serif(19), fill=GREY)
d.line([(M, 136), (W - M, 136)], fill=INK, width=2)

# ---------------- data strip: the day in numbers ----------------
strip = [
    ("258", "Democrats' House seats \u2014 biggest since 1992"),
    ("14", "killed in Russian strikes on the Kyiv region"),
    ("0", "deal at COP31 \u2014 talks collapse, first since 2009"),
    ("1,000+", "Delta flights delayed by a tech fault in Atlanta"),
    ("24", "bodies recovered after the Indonesia factory fire"),
]
sy, sh = 146, 58
cw = (W - 2 * M - 4 * 10) / 5
for i, (num, lab) in enumerate(strip):
    x0 = M + i * (cw + 10)
    d.rounded_rectangle([x0, sy, x0 + cw, sy + sh], radius=6, fill=CARD,
                        outline=LINE, width=1)
    d.text((x0 + 10, sy + 4), num, font=sans_b(23), fill=RED)
    block(d, x0 + 10, sy + 30, lab, sans(9.5), INK, cw - 20, 11.5)

# ---------------- lead-story illustrations ----------------
def art_cop(x0, y0, w, h):
    """COP31 collapse: a cracked globe under a grey sun, NO DEAL stamp."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(34, 66, 58))
    d.ellipse([x0 + w - 66, y0 + 10, x0 + w - 14, y0 + 62], fill=(190, 178, 140))
    cx, cy, r = x0 + 96, y0 + 66, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 164, 208))
    d.ellipse([cx - 36, cy - 42, cx + 4, cy - 8], fill=(74, 164, 94))
    d.ellipse([cx - 4, cy + 6, cx + 38, cy + 42], fill=(74, 164, 94))
    d.ellipse([cx + 14, cy - 36, cx + 36, cy - 14], fill=(74, 164, 94))
    d.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=(20, 60, 50), width=3)
    # crack across the globe
    d.line([(cx - 20, cy - 52), (cx - 4, cy - 18), (cx - 16, cy + 6),
            (cx + 8, cy + 28), (cx - 2, cy + 52)], fill=(20, 60, 50), width=4)
    # fallen leaf
    lx, ly = x0 + 200, y0 + 56
    d.polygon([(lx, ly), (lx + 34, ly + 10), (lx + 16, ly + 34), (lx - 8, ly + 18)],
              fill=(120, 150, 70))
    d.line([(lx + 4, ly + 6), (lx + 26, ly + 26)], fill=(60, 90, 40), width=2)
    # NO DEAL stamp
    d.rounded_rectangle([x0 + w - 118, y0 + h - 34, x0 + w - 10, y0 + h - 8],
                        radius=3, outline=(255, 90, 80), width=3)
    d.text((x0 + w - 108, y0 + h - 31), "NO DEAL", font=sans_b(15),
           fill=(255, 120, 105))
    # delegates' empty chairs row
    for i in range(4):
        bx = x0 + 14 + i * 52
        d.rectangle([bx, y0 + h - 22, bx + 34, y0 + h - 8], fill=(70, 110, 96))

def art_house(x0, y0, w, h):
    """US House: Capitol dome over a blue bar that towers over the red."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=NAVY)
    # stars
    for sx, sy in [(x0 + 22, y0 + 16), (x0 + 60, y0 + 34), (x0 + 300, y0 + 14),
                   (x0 + 268, y0 + 40), (x0 + 150, y0 + 10)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # Capitol dome, white silhouette
    cx = x0 + 78
    d.rectangle([cx - 46, y0 + 88, cx + 46, y0 + h - 6], fill=(235, 232, 222))
    d.polygon([(cx - 34, y0 + 88), (cx + 34, y0 + 88), (cx, y0 + 46)],
              fill=(235, 232, 222))
    d.rectangle([cx - 3, y0 + 36, cx + 3, y0 + 48], fill=(235, 232, 222))
    d.ellipse([cx - 5, y0 + 30, cx + 5, y0 + 40], fill=(235, 232, 222))
    for col in (-34, -18, 0, 18, 34):
        d.rectangle([cx + col - 3, y0 + 96, cx + col + 3, y0 + h - 6],
                    fill=NAVY)
    # bars: blue 258 vs red 173
    bx = x0 + 168
    d.rectangle([bx, y0 + 26, bx + 52, y0 + h - 6], fill=(70, 130, 220))
    d.rectangle([bx + 66, y0 + 58, bx + 118, y0 + h - 6], fill=(210, 70, 70))
    d.text((bx + 6, y0 + 8), "258", font=sans_b(17), fill=(255, 255, 255))
    d.text((bx + 72, y0 + 40), "173", font=sans_b(15), fill=(255, 200, 200))
    d.text((bx, y0 + h - 22), "DEM", font=sans_b(11), fill=(255, 255, 255))
    d.text((bx + 66, y0 + h - 22), "GOP", font=sans_b(11), fill=(255, 255, 255))
    d.text((x0 + w - 96, y0 + 12), "+44 seats", font=sans_b(14),
           fill=(255, 220, 90))

def art_kyiv(x0, y0, w, h):
    """Kyiv region: night sky, a damaged apartment block, rescue beam."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(14, 18, 34))
    for sx, sy in [(x0 + 30, y0 + 12), (x0 + 90, y0 + 26), (x0 + 200, y0 + 10),
                   (x0 + 260, y0 + 30), (x0 + 150, y0 + 20)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
    # searchlight beam from the right
    d.polygon([(x0 + w - 8, y0 + 8), (x0 + w - 60, y0 + h - 10),
               (x0 + w - 96, y0 + h - 10), (x0 + w - 30, y0 + 8)],
              fill=(255, 240, 170))
    # damaged apartment block
    bx, bw, bh = x0 + 18, 120, 96
    d.rectangle([bx, y0 + h - bh, bx + bw, y0 + h], fill=(52, 58, 80))
    d.polygon([(bx + bw, y0 + h - bh), (bx + bw, y0 + h - bh + 34),
               (bx + bw - 34, y0 + h - bh + 34), (bx + bw - 12, y0 + h - bh)],
              fill=(14, 18, 34))
    for row in range(4):
        for col in range(4):
            wx, wy = bx + 12 + col * 28, y0 + h - bh + 12 + row * 22
            lit = (row + col) % 3 == 0
            d.rectangle([wx, wy, wx + 16, wy + 12],
                        fill=(255, 214, 110) if lit else (30, 34, 52))
    # smoke curls
    for i, (sx, sy, sr) in enumerate([(bx + 96, y0 + 18, 12), (bx + 108, y0 + 6, 9),
                                      (bx + 84, y0 + 30, 10)]):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 130))
    # second block + ambulance light
    d.rectangle([x0 + 168, y0 + h - 66, x0 + 252, y0 + h], fill=(44, 50, 70))
    for wy in range(y0 + h - 58, y0 + h - 8, 18):
        d.rectangle([x0 + 178, wy, x0 + 194, wy + 9], fill=(255, 214, 110))
        d.rectangle([x0 + 212, wy, x0 + 228, wy + 9], fill=(30, 34, 52))
    d.ellipse([x0 + 268, y0 + h - 24, x0 + 282, y0 + h - 10], fill=(255, 70, 60))
    d.text((x0 + 8, y0 + 8), "DYMER", font=sans_b(12), fill=(255, 255, 255))

mains = [
    ("CLIMATE \u2014 COP31", "COP31 collapses: no deal\non fossil fuels",
     "After record overtime in Antalya, nearly 200 nations walk away with no pact \u2014 the first COP failure since 2009. The EU rejected a text with no mention of fossil fuels.",
     art_cop),
    ("US POLITICS", "Democrats clinch 258\nHouse seats",
     "The biggest House majority for either party since 1992. Chuck Hubbard's North Carolina win, by 330 votes after a recount, sealed a 44-seat midterm sweep.",
     art_house),
    ("UKRAINE", "Russian strikes kill\nat least 14 near Kyiv",
     "A drone hit a five-storey block in Dymer; a supermarket in Vyshneve was struck too. Rescuers searched the rubble for survivors through the night.",
     art_kyiv),
]
my, mh = 212, 272
mw = (W - 2 * M - 2 * 14) / 3
for i, (kick, head, body, painter) in enumerate(mains):
    x0 = M + i * (mw + 14)
    painter(int(x0), my, int(mw), 128)
    y = my + 136
    tag(d, int(x0), y, kick)
    y += 27
    for ln in head.split("\n"):
        d.text((x0, y), ln, font=serif_b(21), fill=INK)
        y += 25
    block(d, int(x0), y + 2, body, sans(12.5), INK, mw, 15)

# ---------------- small-card grid ----------------
d.line([(M, 498), (W - M, 498)], fill=INK, width=2)
d.text((M, 506), "MORE OF THE DAY", font=sans_b(15), fill=RED)
d.text((W - M - d.textlength("9 more stories", font=sans(14)), 507),
       "9 more stories", font=sans(14), fill=GREY)

def tile(x0, y0, s, color):
    d.rounded_rectangle([x0, y0, x0 + s, y0 + s], radius=8, fill=color)

def ic_plane(x0, y0, s):
    tile(x0, y0, s, (40, 90, 150))
    d.polygon([(x0 + 10, y0 + 34), (x0 + s - 8, y0 + 30), (x0 + s - 14, y0 + 36),
               (x0 + 14, y0 + 42)], fill=(255, 255, 255))
    d.polygon([(x0 + 30, y0 + 18), (x0 + 36, y0 + 30), (x0 + 30, y0 + 38),
               (x0 + 24, y0 + 30)], fill=(255, 255, 255))
    d.line([(x0 + 12, y0 + 50), (x0 + s - 12, y0 + 50)], fill=(255, 220, 90), width=3)

def ic_fire(x0, y0, s):
    tile(x0, y0, s, (198, 72, 30))
    d.polygon([(x0 + s / 2, y0 + 8), (x0 + s - 12, y0 + 34), (x0 + s - 12, y0 + s - 10),
               (x0 + 12, y0 + s - 10), (x0 + 12, y0 + 34)], fill=(255, 192, 60))
    d.ellipse([x0 + s / 2 - 9, y0 + s - 26, x0 + s / 2 + 9, y0 + s - 8],
              fill=(255, 92, 40))

def ic_ship(x0, y0, s):
    tile(x0, y0, s, (24, 70, 110))
    d.polygon([(x0 + 12, y0 + 34), (x0 + s - 12, y0 + 34), (x0 + s - 20, y0 + 46),
               (x0 + 20, y0 + 46)], fill=(235, 232, 222))
    d.rectangle([x0 + s / 2 - 8, y0 + 16, x0 + s / 2 + 8, y0 + 34],
                fill=(235, 232, 222))
    d.ellipse([x0 + s - 22, y0 + 10, x0 + s - 10, y0 + 22], fill=(255, 120, 60))
    d.arc([x0 + 10, y0 + 50, x0 + 26, y0 + 60], 0, 180, fill=(255, 255, 255), width=3)
    d.arc([x0 + s - 26, y0 + 50, x0 + s - 10, y0 + 60], 0, 180,
          fill=(255, 255, 255), width=3)

def ic_ballot(x0, y0, s):
    tile(x0, y0, s, (150, 40, 90))
    d.rectangle([x0 + 12, y0 + 26, x0 + s - 12, y0 + s - 12], fill=(250, 246, 235))
    d.rectangle([x0 + s / 2 - 12, y0 + 22, x0 + s / 2 + 12, y0 + 30],
                fill=(150, 40, 90))
    d.text((x0 + s / 2 - 9, y0 + 36), "\u2713", font=sans_b(20), fill=RED)

def ic_flags(x0, y0, s):
    tile(x0, y0, s, (70, 70, 78))
    d.rectangle([x0 + 10, y0 + 14, x0 + 28, y0 + 30], fill=(60, 90, 180))
    d.rectangle([x0 + 10, y0 + 14, x0 + 28, y0 + 20], fill=(255, 255, 255))
    d.rectangle([x0 + 10, y0 + 24, x0 + 28, y0 + 30], fill=(200, 40, 40))
    d.rectangle([x0 + 34, y0 + 14, x0 + 52, y0 + 30], fill=(255, 255, 255))
    d.rectangle([x0 + 34, y0 + 14, x0 + 52, y0 + 20], fill=(255, 255, 255))
    d.rectangle([x0 + 34, y0 + 20, x0 + 52, y0 + 30], fill=(200, 40, 40))
    d.line([(x0 + 12, y0 + 30), (x0 + 12, y0 + 52)], fill=(250, 246, 235), width=2)
    d.line([(x0 + 36, y0 + 30), (x0 + 36, y0 + 52)], fill=(250, 246, 235), width=2)
    d.text((x0 + 8, y0 + 42), "FRIEND?", font=sans_b(9), fill=(255, 220, 90))

def ic_chip(x0, y0, s):
    tile(x0, y0, s, (24, 110, 96))
    d.rectangle([x0 + 16, y0 + 16, x0 + s - 16, y0 + s - 16], fill=(250, 246, 235))
    d.rectangle([x0 + 24, y0 + 24, x0 + s - 24, y0 + s - 24], fill=(24, 110, 96))
    d.text((x0 + 22, y0 + 26), "AI", font=sans_b(16), fill=(255, 255, 255))
    for px in (x0 + 22, x0 + 32, x0 + 42):
        d.line([(px, y0 + 10), (px, y0 + 16)], fill=(250, 246, 235), width=2)
        d.line([(px, y0 + s - 16), (px, y0 + s - 10)], fill=(250, 246, 235), width=2)

def ic_clock(x0, y0, s):
    tile(x0, y0, s, (120, 60, 30))
    cx, cy = x0 + s / 2, y0 + s / 2
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(250, 246, 235))
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], outline=(120, 60, 30), width=3)
    d.line([(cx, cy), (cx, cy - 14)], fill=INK, width=3)
    d.line([(cx, cy), (cx + 12, cy + 6)], fill=INK, width=3)
    d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=RED)

def ic_grad(x0, y0, s):
    tile(x0, y0, s, (26, 44, 76))
    d.polygon([(x0 + s / 2, y0 + 16), (x0 + s - 10, y0 + 28), (x0 + s / 2, y0 + 40),
               (x0 + 10, y0 + 28)], fill=(250, 246, 235))
    d.rectangle([x0 + s / 2 - 9, y0 + 38, x0 + s / 2 + 9, y0 + 50],
                fill=(250, 246, 235))
    d.text((x0 + s / 2 - 8, y0 + 50), "CSAT", font=sans_b(9), fill=(255, 220, 90))

def ic_storm(x0, y0, s):
    tile(x0, y0, s, (50, 80, 110))
    d.ellipse([x0 + 12, y0 + 14, x0 + 38, y0 + 34], fill=(250, 246, 235))
    d.ellipse([x0 + 26, y0 + 10, x0 + 52, y0 + 34], fill=(250, 246, 235))
    d.rectangle([x0 + 12, y0 + 26, x0 + 52, y0 + 34], fill=(250, 246, 235))
    for rx in (x0 + 18, x0 + 30, x0 + 42):
        d.line([(rx, y0 + 40), (rx - 3, y0 + 50)], fill=(140, 200, 255), width=3)
    d.arc([x0 + 10, y0 + 48, x0 + 30, y0 + 60], 0, 180, fill=(255, 255, 255), width=2)
    d.arc([x0 + 34, y0 + 48, x0 + 54, y0 + 60], 0, 180, fill=(255, 255, 255), width=2)

cards = [
    ("USA / TRAVEL", "Delta delays top 1,000 flights at Thanksgiving",
     "A system fault at the Atlanta hub delayed half of Sunday's flights.", ic_plane),
    ("INDONESIA", "Factory fire: 24 bodies found, 34 missing",
     "The search resumes at the Jakarta candy plant after a deadly blaze.", ic_fire),
    ("LIBYA", "Russian warship hit in sea-drone attack",
     "The corvette Merkury caught fire after sea drones slipped past defences.", ic_ship),
    ("SPAIN", "S\u00e1nchez seeks comeback in Spanish vote",
     "Polls put the PM behind Feij\u00f3o in a vote that could shift the EU balance.", ic_ballot),
    ("USA / RUSSIA", "Intel chief backs Trump calling Putin \u2018friend\u2019",
     "The warm greeting drew fire from Democrats as a betrayal of US values.", ic_flags),
    ("TECH", "Trump: rehire Jensen Huang at Nvidia",
     "Trump backs the ex-CEO's return as a probe into chip sales to China widens.", ic_chip),
    ("USA / IRAN", "Trump \u2018inclined\u2019 to resume war if no deal by New Year",
     "Tehran seeks a clear way out of the neither-war-nor-peace standoff.", ic_clock),
    ("SOUTH KOREA", "Education chief quits over exam cheating row",
     "The minister resigned after confusion over anti-cheating rules for the CSAT.", ic_grad),
    ("USA", "San Francisco faces historic flood threat",
     "A major storm bears down on the Bay Area as Thanksgiving travel peaks.", ic_storm),
]
gy, gh = 526, 94
gw = (W - 2 * M - 2 * 10) / 3
for i, (kick, head, body, painter) in enumerate(cards):
    r, c = divmod(i, 3)
    x0 = M + c * (gw + 10)
    y0 = gy + r * (gh + 8)
    d.rounded_rectangle([x0, y0, x0 + gw, y0 + gh], radius=6, fill=CARD,
                        outline=LINE, width=1)
    painter(int(x0 + 8), int(y0 + 14), 62)
    tx = x0 + 80
    d.text((tx, y0 + 8), kick, font=sans_b(11), fill=RED)
    y = block(d, int(tx), int(y0 + 24), head, sans_b(14.5), INK, gw - 90, 17)
    block(d, int(tx), int(y0 + 58), body, sans(11.5), GREY, gw - 90, 14)

# ---------------- bottom: map + briefs ----------------
by = 844
d.line([(M, by - 8), (W - M, by - 8)], fill=INK, width=2)
d.text((M, by), "WHERE IT HAPPENED", font=sans_b(15), fill=RED)
d.text((M + 348, by), "IN BRIEF", font=sans_b(15), fill=RED)

map_x, map_y, map_w, map_h = M, by + 24, 320, 96
d.rounded_rectangle([map_x, map_y, map_x + map_w, map_y + map_h], radius=6,
                    fill=OCEAN, outline=LINE, width=1)

def ll(lon, lat):
    return (map_x + (lon + 180) / 360 * map_w,
            map_y + (90 - lat) / 180 * map_h)

continents = {
    "NA": [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-75, 73), (-55, 60),
           (-65, 45), (-75, 35), (-80, 26), (-90, 21), (-97, 16), (-105, 20),
           (-115, 30), (-125, 40), (-125, 55), (-150, 60)],
    "SA": [(-78, 8), (-60, 10), (-50, 0), (-35, -8), (-40, -22), (-55, -35),
           (-70, -40), (-73, -50), (-70, -20), (-80, -5)],
    "AF": [(-17, 15), (-10, 31), (10, 37), (30, 32), (43, 12), (51, 10),
           (40, -5), (35, -25), (20, -35), (12, -18), (9, 0), (-8, 4)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (12, 55),
           (18, 56), (24, 60), (30, 70), (40, 68), (30, 60), (20, 45), (12, 44),
           (18, 40), (23, 36), (15, 38), (8, 39)],
    "AS": [(40, 68), (60, 70), (100, 77), (140, 72), (170, 66), (180, 65),
           (160, 60), (140, 45), (127, 40), (120, 32), (110, 20), (100, 8),
           (95, 15), (80, 8), (72, 20), (60, 25), (50, 30), (43, 12), (35, 32)],
    "OC": [(113, -22), (130, -12), (142, -11), (150, -22), (153, -27), (146, -39),
           (140, -38), (130, -32), (118, -35)],
}
for poly in continents.values():
    d.polygon([ll(lo, la) for lo, la in poly], fill=LAND, outline=(160, 145, 115))

dots = [
    (30, 50, "Kyiv"), (51, 24, "Antalya"), (-77, 39, "Washington"),
    (-122, 37, "San Francisco"), (107, -6, "Jakarta"), (18, 33, "Libya"),
    (-3, 40, "Madrid"), (127, 37, "Seoul"), (-95, 33, "Atlanta"),
]
for lon, lat, name in dots:
    px, py = ll(lon, lat)
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=RED,
              outline=(255, 255, 255), width=1)
    if name in ("Kyiv", "Antalya", "Washington", "Jakarta"):
        d.text((px + 6, py - 5), name, font=sans_b(9), fill=INK)

briefs = [
    "Bangladesh garment sector lost $428m in 18 days of unrest.",
    "Strong El Ni\u00f1o raises snow, avalanche and flood risks in the Himalayas.",
    "Brazil ex-leader Bolsonaro \u2018stable\u2019 in intensive care.",
    "BepiColombo enters orbit around Mercury after an eight-year trip.",
    "North Korea's Kim: country seeks security, not supremacy.",
    "WHO: fighting near the Congo Ebola outbreak disrupts the response.",
]
bx = M + 348
yy = by + 24
for b in briefs:
    d.ellipse([bx, yy + 4, bx + 6, yy + 10], fill=RED)
    yy = block(d, bx + 12, yy, b, sans(12), INK, W - M - bx - 12, 14) + 3

# ---------------- footer ----------------
fy = 992
d.line([(M, fy - 6), (W - M, fy - 6)], fill=LINE, width=1)
foot = ("Sources: Reuters, AP, CNN, CNA, Xinhua, SCMP, FMT \u2014 "
        "all events of Monday 23 November 2026")
d.text((M, fy + 2), foot, font=sans(11.5), fill=GREY)

img.save(OUT, optimize=True)
print("saved", OUT, img.size, os.path.getsize(OUT), "bytes")
