#!/usr/bin/env python3
"""
prepare_images.py — resize + watermark photos before adding them to a gallery.

This is the one step that provides *durable* protection: everything else in
this site (right-click blocking, canvas rendering) is a deterrent that lives
in the browser and can be bypassed. A watermark baked into the pixels here,
and a resolution cap that never uploads your full-size original, survives
screenshots, downloads, and any AI scraper that ignores robots.txt.

Usage:
    pip install pillow --break-system-packages
    python3 scripts/prepare_images.py INPUT_DIR OUTPUT_DIR [--watermark "Your Name"]

Example:
    python3 scripts/prepare_images.py ~/Photos/coastal-shoot assets/images/galleries/coastal-light --watermark "Jane Doe"
"""
import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    sys.exit("Pillow is required: pip install pillow --break-system-packages")

MAX_LONG_EDGE = 2000  # px — plenty sharp for on-screen viewing, well below print/resale quality


def strip_metadata_and_resize(img):
    img = ImageOps.exif_transpose(img)  # respect rotation, then drop EXIF (incl. GPS) below
    img = img.convert("RGB")
    w, h = img.size
    if max(w, h) > MAX_LONG_EDGE:
        scale = MAX_LONG_EDGE / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    return img


def add_watermark(img, text):
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    font_size = max(16, img.size[0] // 32)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
    label = f"\u00A9 {text}"
    tw = draw.textlength(label, font=font)
    step_x, step_y = int(tw + 80), font_size * 6
    for y in range(-img.size[1], img.size[1] * 2, step_y):
        for x in range(-img.size[0], img.size[0] * 2, step_x):
            draw.text((x, y), label, font=font, fill=(255, 255, 255, 40))
    rotated = overlay.rotate(-22, expand=0)
    return Image.alpha_composite(img.convert("RGBA"), rotated).convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir")
    ap.add_argument("output_dir")
    ap.add_argument("--watermark", default=None, help="Text to tile across the image; omit to skip watermarking")
    ap.add_argument("--quality", type=int, default=85)
    args = ap.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    exts = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp")
    files = sorted(f for f in os.listdir(args.input_dir) if f.lower().endswith(exts))
    if not files:
        sys.exit(f"No images found in {args.input_dir}")

    for i, fname in enumerate(files, start=1):
        path = os.path.join(args.input_dir, fname)
        img = Image.open(path)
        img = strip_metadata_and_resize(img)
        if args.watermark:
            img = add_watermark(img, args.watermark)
        out_name = f"{i:02d}.jpg"
        out_path = os.path.join(args.output_dir, out_name)
        img.save(out_path, "JPEG", quality=args.quality, optimize=True)
        print(f"  {fname}  ->  {out_path}")

    print(f"\nDone. {len(files)} image(s) written to {args.output_dir}")
    print("Now add matching entries (file/alt/caption) to the gallery's .md front matter.")


if __name__ == "__main__":
    main()
