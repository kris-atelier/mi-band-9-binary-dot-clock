from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

def dot(path, color):
    scale = 4
    image = Image.new("RGBA", (12 * scale, 12 * scale), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, 12 * scale - 1, 12 * scale - 1), fill=color)
    image.resize((12, 12), Image.Resampling.LANCZOS).save(path)

dot(ASSETS / "dot-on.png", (255, 255, 255, 255))
dot(ASSETS / "dot-off.png", (21, 21, 21, 255))
bits = [1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0]  # PM, 12, 34

def elongated_preview(angle, filename):
    image = Image.new("RGB", (192, 490), (0, 0, 0))
    target = ImageDraw.Draw(image)
    ys = [40, 88, 124, 160, 196, 232, 304, 330, 356, 382, 408, 434]
    # The face is read from the bottom edge in the 90-degree orientation.
    # Keep the 270-degree reference as the opposite physical direction.
    display = list(reversed(bits))
    if angle == 270:
        display.reverse()
    for y, bit in zip(ys, display):
        color = (255, 255, 255) if bit else (21, 21, 21)
        target.ellipse((90, y - 6, 101, y + 5), fill=color)
    target.rectangle((125, 40, 126, 434), fill=(16, 16, 16))
    tick_y = 40 + round((434 - 40) * 37 / 59)
    target.rectangle((122, tick_y - 4, 129, tick_y + 3), fill=(255, 255, 255))
    image.save(ASSETS / filename)

elongated_preview(90, "preview-192x490-elongated-90.png")
elongated_preview(270, "preview-192x490-elongated-270.png")
