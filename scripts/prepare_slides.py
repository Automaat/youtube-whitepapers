#!/usr/bin/env python3
"""Prepare slides for video generation.

Extracts slides from PDF and ensures thumbnail/last-slide match dimensions.
This prevents ffmpeg concat demuxer from dropping frames due to resolution changes.
Also compresses images exceeding 1.9MB threshold.
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
COMPRESS_THRESHOLD = 1.9 * 1024 * 1024  # 1.9MB in bytes
YOUTUBE_DIR = SCRIPT_DIR / "youtube"
ASSETS_DIR = YOUTUBE_DIR / "pl"
THUMBNAILS_DIR = YOUTUBE_DIR / "thumbnails"
LAST_SLIDE = ASSETS_DIR / "slides" / "last-slide.png"


def run_cmd(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run command and return result."""
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable string."""
    if size_bytes >= 1024**2:
        return f"{size_bytes / 1024**2:.1f}MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f}KB"
    return f"{size_bytes}B"


def compress_image(src: Path, quality: int = 80, colors: int = 256) -> tuple[int, int]:
    """Compress PNG image in-place. Returns (old_size, new_size)."""
    old_size = src.stat().st_size
    tmp_path = src.with_suffix(".tmp.png")

    cmd = [
        "convert",
        str(src),
        "-quality",
        str(quality),
        "-colors",
        str(colors),
        str(tmp_path),
    ]

    result = run_cmd(cmd, check=False)
    if result.returncode != 0:
        if tmp_path.exists():
            tmp_path.unlink()
        raise RuntimeError(f"Compression failed: {result.stderr}")

    new_size = tmp_path.stat().st_size

    # Only replace if smaller
    if new_size < old_size:
        tmp_path.replace(src)
    else:
        tmp_path.unlink()
        new_size = old_size

    return old_size, new_size


def compress_large_images(images: list[Path]) -> None:
    """Compress images exceeding threshold."""
    large = [(img, img.stat().st_size) for img in images if img.stat().st_size > COMPRESS_THRESHOLD]

    if not large:
        print(f"   ✅ All images under {format_size(int(COMPRESS_THRESHOLD))}")
        return

    print(f"   🔄 Compressing {len(large)} images > {format_size(int(COMPRESS_THRESHOLD))}")

    for img, _ in large:
        try:
            old_size, new_size = compress_image(img)
            if new_size < old_size:
                savings = (1 - new_size / old_size) * 100
                print(f"      {img.name}: {format_size(old_size)} → {format_size(new_size)} ({savings:.0f}% smaller)")
            else:
                print(f"      {img.name}: {format_size(old_size)} (already optimal)")
        except RuntimeError as e:
            print(f"      ❌ {img.name}: {e}")


def get_image_dimensions(image_path: Path) -> tuple[int, int]:
    """Get image width and height using ImageMagick identify."""
    result = run_cmd(["identify", "-format", "%wx%h", str(image_path)])
    if result.returncode != 0:
        raise ValueError(f"Cannot get dimensions: {result.stderr}")
    w, h = result.stdout.strip().split("x")
    return int(w), int(h)


def scale_image(src: Path, dst: Path, width: int, height: int) -> None:
    """Scale image to exact dimensions with padding using ImageMagick."""
    cmd = [
        "convert",
        str(src),
        "-colorspace",
        "sRGB",
        "-resize",
        f"{width}x{height}",
        "-background",
        "black",
        "-gravity",
        "center",
        "-extent",
        f"{width}x{height}",
        str(dst),
    ]
    result = run_cmd(cmd, check=False)
    if result.returncode != 0:
        print(f"   ❌ Failed to scale {src.name}")
        print(f"      {result.stderr}")
        sys.exit(1)


def ensure_rgb(image_path: Path) -> None:
    """Ensure image is in sRGB colorspace to prevent ffmpeg concat issues."""
    run_cmd(["mogrify", "-colorspace", "sRGB", str(image_path)])


def find_episode(ep_num: str) -> Path | None:
    """Find PDF file matching episode number."""
    slides_dir = ASSETS_DIR / "slides"
    matches = list(slides_dir.glob(f"{ep_num}-*.pdf"))
    return matches[0] if matches else None


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: ./prepare-slides.py <episode_number>")
        print("Example: ./prepare-slides.py 26")
        print()
        print("This script:")
        print("  1. Extracts slides from PDF using pdftoppm")
        print("  2. Scales thumbnail to match slide dimensions")
        print("  3. Copies last-slide.png to output folder")
        print()
        print("Available episodes:")
        slides_dir = ASSETS_DIR / "slides"
        if slides_dir.exists():
            for f in sorted(slides_dir.glob("*.pdf")):
                print(f"  {f.stem}")
        return 1

    ep_num = sys.argv[1]
    pdf_file = find_episode(ep_num)

    if not pdf_file:
        print(f"❌ No PDF file found for episode {ep_num}")
        return 1

    ep_name = pdf_file.stem
    output_dir = pdf_file.parent / ep_name
    thumbnail_src = THUMBNAILS_DIR / f"{ep_name}.png"

    print(f"📋 Preparing slides for: {ep_name}")
    print("━" * 50)

    # Check required files
    if not pdf_file.exists():
        print(f"❌ PDF not found: {pdf_file}")
        return 1

    if not thumbnail_src.exists():
        print(f"❌ Thumbnail not found: {thumbnail_src}")
        return 1

    if not LAST_SLIDE.exists():
        print(f"❌ Last slide not found: {LAST_SLIDE}")
        return 1

    # Create output directory
    output_dir.mkdir(exist_ok=True)
    print(f"✅ Output directory: {output_dir.relative_to(SCRIPT_DIR)}")

    # Extract slides from PDF
    print("🔄 Extracting slides from PDF...")
    result = run_cmd(
        ["pdftoppm", "-png", "-r", "150", str(pdf_file), str(output_dir / "slide")], check=False
    )

    if result.returncode != 0:
        print(f"❌ pdftoppm failed: {result.stderr}")
        return 1

    slides = sorted(output_dir.glob("slide-*.png"))
    print(f"   ✅ Extracted {len(slides)} slides")

    if not slides:
        print("❌ No slides extracted")
        return 1

    # Get reference dimensions from first slide
    width, height = get_image_dimensions(slides[0])
    print(f"   📐 Reference dimensions: {width}x{height}")

    # Normalize slides: sRGB colorspace + consistent dimensions
    print("🔄 Normalizing slides...")
    scaled_count = 0
    for slide in slides:
        slide_w, slide_h = get_image_dimensions(slide)
        if (slide_w, slide_h) != (width, height):
            print(f"   📐 Scaling {slide.name}: {slide_w}x{slide_h} → {width}x{height}")
            scale_image(slide, slide, width, height)
            scaled_count += 1
        else:
            ensure_rgb(slide)

    if scaled_count > 0:
        print(f"   ✅ Scaled {scaled_count} slides to match reference")
    print(f"   ✅ Normalized {len(slides)} slides")

    # Scale and copy thumbnail
    print("🔄 Preparing thumbnail...")
    thumb_dst = output_dir / "thumbnail.png"
    thumb_w, thumb_h = get_image_dimensions(thumbnail_src)

    if (thumb_w, thumb_h) == (width, height):
        # Just copy if dimensions match
        thumb_dst.write_bytes(thumbnail_src.read_bytes())
        print("   ✅ Thumbnail copied (dimensions already match)")
    else:
        print(f"   📐 Scaling from {thumb_w}x{thumb_h} to {width}x{height}")
        scale_image(thumbnail_src, thumb_dst, width, height)
        print("   ✅ Thumbnail scaled and copied")

    # Scale and copy last-slide
    print("🔄 Preparing last-slide...")
    last_dst = output_dir / "last-slide.png"
    last_w, last_h = get_image_dimensions(LAST_SLIDE)

    if (last_w, last_h) == (width, height):
        last_dst.write_bytes(LAST_SLIDE.read_bytes())
        print("   ✅ Last slide copied (dimensions already match)")
    else:
        print(f"   📐 Scaling from {last_w}x{last_h} to {width}x{height}")
        scale_image(LAST_SLIDE, last_dst, width, height)
        print("   ✅ Last slide scaled and copied")

    # Verify all images have same dimensions
    print("🔍 Verifying image consistency...")
    all_images = [thumb_dst, *slides, last_dst]
    dimensions_ok = True

    for img in all_images:
        w, h = get_image_dimensions(img)
        status = "✅" if (w, h) == (width, height) else "❌"
        if (w, h) != (width, height):
            dimensions_ok = False
            print(f"   {status} {img.name}: {w}x{h} (expected {width}x{height})")

    if dimensions_ok:
        print(f"   ✅ All {len(all_images)} images have consistent dimensions")

    # Compress large images
    print("🔄 Checking file sizes...")
    compress_large_images(all_images)

    # Summary
    print()
    print("━" * 50)
    print("✅ Slides prepared successfully!")
    print()
    print("Files created:")
    print(f"   📁 {output_dir.relative_to(SCRIPT_DIR)}/")
    print(f"      thumbnail.png  ({width}x{height})")
    for s in slides:
        print(f"      {s.name}")
    print(f"      last-slide.png ({width}x{height})")
    print()
    print("Next: Generate video with Claude Code using /generate-video")

    return 0


if __name__ == "__main__":
    sys.exit(main())
