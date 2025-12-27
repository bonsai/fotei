#!/usr/bin/env python3
"""resize_images.py

Batch resize/compress images in a folder to achieve a target file size.

Usage:
    python resize_images.py --folder PATH --target-size 200KB [--max-dimension 1080]

Options:
    --folder          Directory containing images (processed recursively).
    --target-size     Desired maximum file size per image (e.g., 200KB, 0.5MB).
    --max-dimension   Optional maximum width or height in pixels. Images larger than this will be
                      resized while preserving aspect ratio before compression.
    --output          Optional output directory. If omitted, original files are overwritten.
    --dry-run         Show what would be done without modifying files.

The script determines the optimal JPEG quality (or PNG compression level) via binary search
to get as close as possible to the target size without exceeding it.
"""

import argparse
import os
import sys
from pathlib import Path
from io import BytesIO
from PIL import Image

def parse_size(size_str: str) -> int:
    """Parse a human‑readable size like '200KB' or '1.5MB' into bytes."""
    size_str = size_str.strip().upper()
    if size_str.endswith('KB'):
        return int(float(size_str[:-2]) * 1024)
    if size_str.endswith('MB'):
        return int(float(size_str[:-2]) * 1024 * 1024)
    if size_str.endswith('B'):
        return int(float(size_str[:-1]))
    # fallback: assume bytes
    return int(float(size_str))

def resize_image(img: Image.Image, max_dim: int) -> Image.Image:
    """Resize image so that the longest side is <= max_dim, preserving aspect ratio."""
    if max_dim <= 0:
        return img
    w, h = img.size
    if max(w, h) <= max_dim:
        return img
    if w >= h:
        new_w = max_dim
        new_h = int(h * (max_dim / w))
    else:
        new_h = max_dim
        new_w = int(w * (max_dim / h))
    return img.resize((new_w, new_h), Image.LANCZOS)

def compress_to_target(img: Image.Image, target_bytes: int, fmt: str, max_dim: int) -> bytes:
    """Return image bytes compressed to be <= target_bytes.
    Uses binary search on quality (JPEG) or compression level (PNG).
    """
    img = resize_image(img, max_dim)
    # For PNG we can only adjust compression level (0‑9). For JPEG we adjust quality (1‑95).
    if fmt.upper() == 'PNG':
        low, high = 0, 9
        best = None
        while low <= high:
            mid = (low + high) // 2
            buffer = BytesIO()
            img.save(buffer, format='PNG', compress_level=mid)
            size = buffer.tell()
            if size <= target_bytes:
                best = buffer.getvalue()
                high = mid - 1  # try lower compression (bigger file) to get closer
            else:
                low = mid + 1
        return best if best is not None else buffer.getvalue()
    else:  # JPEG/WEBP etc.
        low, high = 1, 95
        best = None
        while low <= high:
            mid = (low + high) // 2
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=mid, optimize=True)
            size = buffer.tell()
            if size <= target_bytes:
                best = buffer.getvalue()
                low = mid + 1  # try higher quality (bigger file) to get closer
            else:
                high = mid - 1
        return best if best is not None else buffer.getvalue()

def process_file(src_path: Path, target_bytes: int, max_dim: int, out_dir: Path, dry_run: bool):
    ext = src_path.suffix.lower()
    if ext not in {'.jpg', '.jpeg', '.png', '.webp'}:
        print(f"[skip] Unsupported format: {src_path}")
        return
    try:
        with Image.open(src_path) as im:
            fmt = im.format
            out_bytes = compress_to_target(im, target_bytes, fmt, max_dim)
            if dry_run:
                print(f"[dry‑run] {src_path} → {len(out_bytes)} bytes")
                return
            # Determine output path
            out_path = out_dir / src_path.relative_to(src_path.anchor) if out_dir else src_path
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, 'wb') as f:
                f.write(out_bytes)
            print(f"[done] {src_path} → {out_path} ({len(out_bytes)} bytes)")
    except Exception as e:
        print(f"[error] {src_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Batch resize/compress images to a target file size.')
    parser.add_argument('--folder', required=True, help='Directory containing images (recursively).')
    parser.add_argument('--target-size', required=True, help='Target size per image (e.g., 200KB, 1.5MB).')
    parser.add_argument('--max-dimension', type=int, default=0,
                        help='Maximum width/height in pixels before compression (0 = keep original size).')
    parser.add_argument('--output', help='Output directory (defaults to overwriting originals).')
    parser.add_argument('--dry-run', action='store_true', help='Show actions without writing files.')
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        print(f"Error: {folder} is not a directory.")
        sys.exit(1)
    target_bytes = parse_size(args.target_size)
    out_dir = Path(args.output).resolve() if args.output else None
    if out_dir and not out_dir.exists():
        out_dir.mkdir(parents=True)

    for root, _, files in os.walk(folder):
        for name in files:
            src_path = Path(root) / name
            process_file(src_path, target_bytes, args.max_dimension, out_dir, args.dry_run)

if __name__ == '__main__':
    main()
