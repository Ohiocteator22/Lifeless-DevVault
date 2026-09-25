"""Build a multi-size app_icon.ico from the largest image in this folder."""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))

# Find image files in this folder
candidates = [
    f for f in os.listdir(HERE)
    if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".webp"))
    and "app_icon" in f.lower()
]

if not candidates:
    raise SystemExit("No app_icon*.png files found in this folder.")

# Pick the largest by pixel area
def area(name):
    with Image.open(os.path.join(HERE, name)) as im:
        return im.width * im.height

largest = max(candidates, key=area)
src = os.path.join(HERE, largest)

with Image.open(src) as im:
    im = im.convert("RGBA")
    # Make sure the source is at least 256x256
    if im.width < 256 or im.height < 256:
        im = im.resize((256, 256), Image.LANCZOS)

    out = os.path.join(HERE, "app_icon.ico")
    im.save(
        out,
        format="ICO",
        sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)],
    )

print(f"Source:  {largest}")
print(f"Created: {out}")