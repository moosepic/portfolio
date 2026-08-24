#!/usr/bin/env python3
"""
prepare_images.py — resize + watermark photos before adding them to a gallery.

This is the one step that provides *durable* protection: everything else in
this site (right-click blocking, canvas rendering) is a deterrent that lives
in the browser and can be bypassed. A logo watermark baked into the pixels
here, and a resolution cap that never uploads your full-size original,
survives screenshots, downloads, and any AI scraper that ignores robots.txt.

Usage:
    pip install pillow --break-system-packages
    python3 scripts/prepare_images.py INPUT_DIR OUTPUT_DIR [--logo path/to/logo.png]

Example:
    python3 scripts/prepare_images.py ~/Photos/coastal-shoot assets/images/galleries/coastal-light --logo assets/images/logo.png
"""
import argparse
import os
import re
import sys

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    sys.exit("Pillow is required: pip install pillow --break-system-packages")

MAX_LONG_EDGE = 2000  # px — plenty sharp for on-screen viewing, well below print/resale quality

NUMBERED_NAME_RE = re.compile(r"^(\d+)\.jpg$", re.IGNORECASE)


def next_start_number(output_dir):
    """Look at existing NN.jpg files already in output_dir and return the
    next free number, so new images get appended rather than re-sequencing
    everything from scratch."""
    highest = 0
    if os.path.isdir(output_dir):
        for fname in os.listdir(output_dir):
            m = NUMBERED_NAME_RE.match(fname)
            if m:
                highest = max(highest, int(m.group(1)))
    return highest + 1


def strip_metadata_and_resize(img):
    img = ImageOps.exif_transpose(img)  # respect rotation, then drop EXIF (incl. GPS) below
    img = img.convert("RGB")
    w, h = img.size
    if max(w, h) > MAX_LONG_EDGE:
        scale = MAX_LONG_EDGE / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    return img


def add_watermark(img, logo_path):
    """Composite a transparent PNG logo into the bottom-right corner,
    scaled proportionally to the image's own width."""
    logo = Image.open(logo_path).convert("RGBA")
    target_width = int(img.size[0] * 0.14)  # logo scales to ~14% of image width
    scale = target_width / logo.size[0]
    logo = logo.resize((target_width, int(logo.size[1] * scale)), Image.LANCZOS)

    base = img.convert("RGBA")
    margin = int(img.size[0] * 0.03)
    pos = (base.size[0] - logo.size[0] - margin, base.size[1] - logo.size[1] - margin)
    base.alpha_composite(logo, dest=pos)
    return base.convert("RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input_dir")
    ap.add_argument("output_dir")
    ap.add_argument("--logo", default=None, help="Path to a transparent PNG logo to stamp into the bottom-right corner; omit to skip watermarking")
    ap.add_argument("--quality", type=int, default=85)
    ap.add_argument("--restart", action="store_true",
                     help="Ignore existing NN.jpg files in output_dir and renumber from 01 "
                          "(old behavior). Default is to append after the highest existing number.")
    args = ap.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    exts = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp")
    files = sorted(f for f in os.listdir(args.input_dir) if f.lower().endswith(exts))
    if not files:
        sys.exit(f"No images found in {args.input_dir}")

    start = 1 if args.restart else next_start_number(args.output_dir)
    if start > 1:
        print(f"Existing numbered images found in {args.output_dir}; appending starting at {start:02d}.jpg")

    for i, fname in enumerate(files, start=start):
        path = os.path.join(args.input_dir, fname)
        img = Image.open(path)
        img = strip_metadata_and_resize(img)
        if args.logo:
            img = add_watermark(img, args.logo)
        out_name = f"{i:02d}.jpg"
        out_path = os.path.join(args.output_dir, out_name)
        img.save(out_path, "JPEG", quality=args.quality, optimize=True)
        print(f"  {fname}  ->  {out_path}")

    print(f"\nDone. {len(files)} image(s) written to {args.output_dir}")
    print("Now add matching entries (file/alt/caption) to the gallery's .md front matter.")


if __name__ == "__main__":
    main()
