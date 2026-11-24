"""Temporary AI hero images (sunrise, midday, sunset) -> site/assets/img/hero-*.webp.

Placeholders until the client supplies real full-size photos.
Usage: python3 build/hero_ai.py sunrise.png midday.png sunset.png
To go back to real photos, change HERO in build/build.py.
"""
import sys
from pathlib import Path
from PIL import Image

out = Path(__file__).resolve().parent.parent / "site/assets/img"
for name, src in zip(("sunrise", "midday", "sunset"), sys.argv[1:4]):
    im = Image.open(src).convert("RGB")
    for tag, px in (("lg", 1920), ("sm", 800)):
        c = im.copy(); c.thumbnail((px, px)); c.save(out / f"hero-{name}-{tag}.webp", "WEBP", quality=80, method=6)
    print(name, im.size)
