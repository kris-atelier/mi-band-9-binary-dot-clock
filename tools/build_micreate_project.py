from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
import shutil
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects" / "MiBand9BinaryDotClock"
IMAGES = PROJECT / "images"
AOD = PROJECT / "AOD"
OUTPUT = PROJECT / "output"
for folder in (IMAGES, AOD, OUTPUT):
    folder.mkdir(parents=True, exist_ok=True)

W, H = 192, 490
ON = (255, 255, 255, 255)
OFF = (21, 21, 21, 255)
BLACK = (0, 0, 0, 0)
R = 6
BIT_Y = [40, 88, 124, 160, 196, 304, 330, 356, 382, 408, 434]

def bits(value, width):
    return [(value >> (width - i - 1)) & 1 for i in range(width)]

def display_bits(value, width):
    """Render MSB->LSB data from the bottom/right edge of the elongated face."""
    return list(reversed(bits(value, width)))

def dot_sprite(y, enabled=True, color=ON):
    image = Image.new("RGBA", (12, 12), BLACK)
    ImageDraw.Draw(image).ellipse((0, 0, 11, 11), fill=color if enabled else OFF)
    return image

def group_sprite(values, height=48):
    image = Image.new("RGBA", (12, height), BLACK)
    draw = ImageDraw.Draw(image)
    step = height / len(values)
    for index, value in enumerate(values):
        y = round((index + 0.5) * step)
        draw.ellipse((0, y - R, 11, y + R - 1), fill=ON if value else OFF)
    return image

def save(name, image):
    image.save(IMAGES / name)

Image.new("RGBA", (W, H), (0, 0, 0, 255)).save(IMAGES / "background.png")
save("ampm-0.png", dot_sprite(0, False))
save("ampm-1.png", dot_sprite(0, True))
for hour in range(24):
    save(f"hour-{hour:02d}.png", group_sprite(display_bits(hour % 12 or 12, 4), 60))
for minute in range(60):
    save(f"minute-{minute:02d}.png", group_sprite(display_bits(minute, 6), 78))
for second in range(60):
    rail = Image.new("RGBA", (8, 395), BLACK)
    draw = ImageDraw.Draw(rail)
    draw.rectangle((3, 0, 4, 394), fill=(16, 16, 16, 255))
    y = round(394 * second / 59)
    draw.rectangle((0, max(0, y - 4), 7, min(394, y + 3)), fill=ON)
    save(f"second-{second:02d}.png", rail)

def widget(name, bitmap_list, x, y, width, height, source, default=0):
    indexed_bitmaps = [f"({index}):{filename}" for index, filename in enumerate(bitmap_list)]
    return {
        "Shape": "31", "Name": name, "BitmapList": "|".join(indexed_bitmaps),
        "X": str(x), "Y": str(y), "Width": str(width), "Height": str(height),
        "Alpha": "255", "Alignment": "0", "DefaultIndex": str(default),
        "Index_Src": source, "Spacing": "0", "Blanking": "0", "Visible_Src": "0"
    }

def make_project(path, aod=False):
    root = Element("FaceProject", {"DeviceType": "366"})
    screen = SubElement(root, "Screen", {"Title": "Binary Dot Clock", "Bitmap": "background.png"})
    if not aod:
        widgets = [
            widget("am_pm", [f"ampm-{i}.png" for i in range(2)], 90, 34, 12, 12, "0813"),
            widget("hour", [f"hour-{i:02d}.png" for i in range(24)], 90, 58, 12, 180, "0811"),
            widget("minute", [f"minute-{i:02d}.png" for i in range(60)], 90, 265, 12, 180, "1011"),
            widget("seconds_tick", [f"second-{i:02d}.png" for i in range(60)], 122, 40, 8, 395, "1811")
        ]
    else:
        widgets = [
            widget("am_pm_aod", ["ampm-0.png", "ampm-1.png"], 90, 34, 12, 12, "0813"),
            widget("hour_aod", [f"hour-{i:02d}.png" for i in range(24)], 90, 58, 12, 180, "0811"),
            widget("minute_aod", [f"minute-{i:02d}.png" for i in range(60)], 90, 265, 12, 180, "1011")
        ]
    for data in widgets:
        SubElement(screen, "Widget", data)
    ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)

make_project(PROJECT / "MiBand9BinaryDotClock.fprj")
(AOD / "images").mkdir(parents=True, exist_ok=True)
for image in IMAGES.glob("*.png"):
    shutil.copy2(image, AOD / "images" / image.name)
make_project(AOD / "MiBand9BinaryDotClock-AOD.fprj", aod=True)
