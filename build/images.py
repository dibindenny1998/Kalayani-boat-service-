"""Resize the client's photos into web-ready WebP files (plus one JPG for link previews).

Usage: python3 build/images.py <folder with original photos>
Needs Pillow (pip install pillow). Output goes to site/assets/img/.
"""
import sys
from pathlib import Path
from PIL import Image, ImageOps

# output name -> original file name (from the client's WhatsApp photos)
PHOTOS = {
    "shikara-sunset-bow": "66998871-image.jpg",
    "shikara-kalyani": "84641894-image.jpg",
    "deck-sofa": "f9169968-image.jpg",
    "deck-front": "e52940fc-image.jpg",
    "deck-yellow": "c700ffa1-image.jpg",
    "chairs-green": "00215918-image.jpg",
    "guests-bow": "944c018f-image.jpg",
    "deck-pink": "5b07f775-image.jpg",
    "chairs-pink": "9e2711bb-image.jpg",
    "kayak-rainbow": "d14bb0f7-image.jpg",
    "kayak-sunset-solo": "edd8b1b9-image.jpg",
    "kayak-canal": "e72b8a1c-image.jpg",
    "kayak-sunrise-group": "a6b93117-image.jpg",
    "kayak-sunset-group": "10f481ab-image.jpg",
    "kayak-trees": "66581640-image.jpg",
}
SIZES = {"lg": 1280, "sm": 640}

src = Path(sys.argv[1])
out = Path(__file__).resolve().parent.parent / "site/assets/img"
out.mkdir(parents=True, exist_ok=True)
for name, file in PHOTOS.items():
    im = ImageOps.exif_transpose(Image.open(src / file)).convert("RGB")
    for tag, px in SIZES.items():
        copy = im.copy()
        copy.thumbnail((px, px))
        copy.save(out / f"{name}-{tag}.webp", "WEBP", quality=78, method=6)
    print(name, im.size)

# link-preview image for WhatsApp / Facebook shares
og = ImageOps.fit(ImageOps.exif_transpose(Image.open(src / PHOTOS["shikara-sunset-bow"])).convert("RGB"), (1200, 630), centering=(0.5, 0.55))
og.save(out / "og-image.jpg", "JPEG", quality=82, optimize=True, progressive=True)
