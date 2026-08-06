from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "all-baseball-skills-camp-flyer.png"
OUT_PDF = ROOT / "all-baseball-skills-camp-flyer.pdf"

W, H = 2550, 3300
BG = "#04070c"
TEXT = "#f4f7fb"
MUTED = "#a9b2c3"
LIME = "#c9ff1a"
GREEN = "#4fd229"
INK = "#061008"
PANEL = "#0a1018"

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
IMPACT = FONT_DIR / "Impact.ttf"
ARIAL = FONT_DIR / "Arial.ttf"
ARIAL_BOLD = FONT_DIR / "Arial Bold.ttf"


def font(path, size):
    return ImageFont.truetype(str(path), size)


F_SUPER = font(IMPACT, 310)
F_HERO = font(IMPACT, 245)
F_BIG = font(IMPACT, 132)
F_LABEL = font(ARIAL_BOLD, 48)
F_BODY = font(ARIAL_BOLD, 64)
F_SMALL = font(ARIAL_BOLD, 38)


def glow_layer(box, color, blur=90):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(box, fill=color)
    return layer.filter(ImageFilter.GaussianBlur(blur))


def text_center(draw, box, text, font_obj, fill):
    left, top, right, bottom = box
    tb = draw.textbbox((0, 0), text, font=font_obj)
    tw = tb[2] - tb[0]
    th = tb[3] - tb[1]
    draw.text((left + (right - left - tw) / 2, top + (bottom - top - th) / 2 - tb[1]), text, font=font_obj, fill=fill)


def slant(draw, points, fill, outline=None, width=1):
    draw.polygon(points, fill=fill)
    if outline:
        draw.line(points + [points[0]], fill=outline, width=width, joint="curve")


img = Image.new("RGB", (W, H), BG).convert("RGBA")
img = Image.alpha_composite(img, glow_layer((-500, -360, 1000, 850), (79, 210, 41, 90)))
img = Image.alpha_composite(img, glow_layer((1220, -500, 3300, 980), (201, 255, 26, 76)))
img = Image.alpha_composite(img, glow_layer((500, 2150, 2200, 3850), (79, 210, 41, 44), blur=130))
draw = ImageDraw.Draw(img)

# Subtle field/grid texture.
for x in range(-250, W + 250, 150):
    draw.line((x, 0, x + 920, H), fill="#101722", width=2)
for y in range(0, H, 150):
    draw.line((0, y, W, y), fill="#0d1420", width=2)

# Stadium-light inspired bursts.
for side in [0, 1]:
    base_x = 190 if side == 0 else W - 190
    direction = 1 if side == 0 else -1
    for i in range(6):
        x = base_x + direction * i * 62
        y = 300 + i * 24
        draw.ellipse((x - 34, y - 34, x + 34, y + 34), fill=(244, 247, 251, 180))
        draw.ellipse((x - 52, y - 52, x + 52, y + 52), outline=(201, 255, 26, 100), width=5)

# Poster frame and aggressive motion shapes.
draw.rounded_rectangle((110, 95, W - 110, H - 95), radius=58, fill=PANEL, outline="#263040", width=5)
slant(draw, [(110, 95), (W - 110, 95), (W - 180, 160), (180, 160)], LIME)
slant(draw, [(0, 860), (W, 630), (W, 830), (0, 1080)], "#132018")
slant(draw, [(120, 1070), (W - 120, 900), (W - 220, 1050), (220, 1220)], LIME)
slant(draw, [(0, 2550), (W, 2320), (W, 2470), (0, 2710)], "#121d14")

for y in [690, 760, 830, 2470, 2550]:
    draw.line((160, y, W - 160, y - 140), fill=LIME, width=8)
    draw.line((180, y + 30, W - 180, y - 85), fill=GREEN, width=4)

# Logo.
logo = Image.open(ROOT / "westside-logo-cutout.png").convert("RGBA")
logo.thumbnail((620, 620))
img.alpha_composite(logo, ((W - logo.width) // 2, 205))
draw = ImageDraw.Draw(img)

# Main headline.
draw.text((190, 835), "ALL BASEBALL", font=F_HERO, fill=TEXT, stroke_width=5, stroke_fill="#1a2028")
draw.text((190, 1070), "SKILLS CAMP", font=F_HERO, fill=LIME, stroke_width=5, stroke_fill="#102008")
draw.text((190, 1330), "FALL", font=F_SUPER, fill=TEXT, stroke_width=5, stroke_fill="#1a2028")
draw.text((840, 1330), "SESSIONS", font=F_SUPER, fill=GREEN, stroke_width=5, stroke_fill="#102008")

# Date/time band.
band = (220, 1745, W - 220, 1925)
draw.rounded_rectangle(band, radius=90, fill=LIME)
text_center(draw, (band[0], band[1] + 8, band[2], band[3] - 8), "TUESDAYS & THURSDAYS  |  5:00-6:30 PM", F_BODY, INK)
draw.text((435, 1978), "AUG. 25-OCT. 1", font=F_BIG, fill=TEXT, stroke_width=4, stroke_fill="#151c24")
draw.text((1265, 1992), "3RD-8TH GRADE PLAYERS", font=F_BODY, fill=LIME)

# Location callout.
loc = (350, 2155, W - 350, 2300)
draw.rounded_rectangle(loc, radius=34, fill="#121a24", outline="#33441c", width=4)
text_center(draw, loc, "PARKER HIGH SCHOOL", F_BODY, TEXT)

# Skill badges.
skills = ["HITTING", "SPEED", "THROWING", "DEFENSE"]
badge_y = 2485
badge_w = 500
badge_h = 185
gap = 70
start_x = (W - (badge_w * 4 + gap * 3)) // 2
for i, skill in enumerate(skills):
    x = start_x + i * (badge_w + gap)
    pts = [(x + 42, badge_y), (x + badge_w - 42, badge_y), (x + badge_w, badge_y + badge_h // 2),
           (x + badge_w - 42, badge_y + badge_h), (x + 42, badge_y + badge_h), (x, badge_y + badge_h // 2)]
    slant(draw, pts, "#111922", outline=LIME, width=5)
    text_center(draw, (x, badge_y + 10, x + badge_w, badge_y + badge_h - 10), skill, F_LABEL, TEXT)

# Footer slogan only. No registration link.
draw.text((245, 2885), "WESTSIDE BASEBALL", font=F_LABEL, fill=LIME)
draw.text((245, 2960), "WORK TOGETHER STAY TOGETHER", font=F_BIG, fill=TEXT, stroke_width=3, stroke_fill="#1a2028")

img.convert("RGB").save(OUT, quality=95)
img.convert("RGB").save(OUT_PDF, "PDF", resolution=300)
print(OUT)
print(OUT_PDF)
