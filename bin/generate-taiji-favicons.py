#!/usr/bin/env python3
"""Generate taiji favicon assets for the landing page."""

from __future__ import annotations

import struct
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "img"

# Standard taijitu: white left + top lobe, black right + bottom lobe, no outer ring.
TAIJI_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="32" fill="#ffffff" />
  <path fill="#111111" d="M32,0 A32,32 0 0,1 32,64 A16,16 0 0,1 32,32 A16,16 0 0,0 32,0 Z" />
  <circle cx="32" cy="16" r="5" fill="#111111" />
  <circle cx="32" cy="48" r="5" fill="#ffffff" />
</svg>
"""


def taiji_data_uri() -> str:
    compact = " ".join(TAIJI_SVG.split())
    return "data:image/svg+xml," + quote(compact)


def _taiji_is_black(dx: float, dy: float, radius: float) -> bool:
    lobe_r = radius / 2.0
    if dx * dx + dy * dy > radius * radius:
        return False

    # Right half is yin (black); left half is yang (white).
    is_black = dx > 0

    # Top lobe (yang): white.
    if dx * dx + (dy + lobe_r) * (dy + lobe_r) <= lobe_r * lobe_r:
        is_black = False

    # Bottom lobe (yin): black.
    if dx * dx + (dy - lobe_r) * (dy - lobe_r) <= lobe_r * lobe_r:
        is_black = True

    return is_black


def draw_taiji(size: int) -> Image.Image:
    cx = cy = size // 2
    radius = size / 2.0
    lobe_r = radius / 2.0
    dot_r = max(1, round(radius * 5.0 / 32.0))
    lobe_offset = int(round(lobe_r))
    black = (17, 17, 17)
    white = (255, 255, 255)

    img = Image.new("RGB", (size, size), white)
    px = img.load()
    for y in range(size):
        for x in range(size):
            dx = x - cx
            dy = y - cy
            if _taiji_is_black(dx, dy, radius):
                px[x, y] = black

    draw = ImageDraw.Draw(img)
    top_y = cy - lobe_offset
    bottom_y = cy + lobe_offset
    draw.ellipse((cx - dot_r, top_y - dot_r, cx + dot_r, top_y + dot_r), fill=black)
    draw.ellipse((cx - dot_r, bottom_y - dot_r, cx + dot_r, bottom_y + dot_r), fill=white)
    return img


def write_png(path: Path, size: int) -> None:
    draw_taiji(size).save(path, format="PNG", optimize=True)


def _png_bytes(image: Image.Image) -> bytes:
    from io import BytesIO

    buf = BytesIO()
    image.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def write_ico(path: Path) -> None:
    sizes = [16, 32, 48]
    png_entries = [(size, _png_bytes(draw_taiji(size))) for size in sizes]

    header = struct.pack("<HHH", 0, 1, len(png_entries))
    offset = 6 + 16 * len(png_entries)
    directory = bytearray()
    image_data = bytearray()

    for size, png in png_entries:
        directory.extend(struct.pack("<BBBBHHII", size, size, 0, 0, 1, 32, len(png), offset))
        image_data.extend(png)
        offset += len(png)

    path.write_bytes(header + directory + image_data)


def write_svg(path: Path) -> None:
    path.write_text(TAIJI_SVG.strip() + "\n", encoding="utf-8")


def verify_ico(path: Path) -> None:
    data = path.read_bytes()
    if len(data) < 6:
        raise SystemExit(f"{path}: ICO too small")
    reserved, icotype, count = struct.unpack("<HHH", data[:6])
    if reserved != 0 or icotype != 1:
        raise SystemExit(f"{path}: invalid ICO header")
    if count < 2:
        raise SystemExit(f"{path}: expected multiple icon sizes, got {count}")


def verify_taiji_image(size: int = 64) -> None:
    cx = cy = size // 2
    radius = size / 2.0
    lobe_r = radius / 2.0
    lobe_offset = int(round(lobe_r))
    img = draw_taiji(size)
    px = img.load()
    white = (255, 255, 255)
    black = (17, 17, 17)

    checks = [
        (int(cx - radius * 0.45), cy, white, "left side should be white"),
        (int(cx + radius * 0.45), cy, black, "right side should be black"),
        (cx, cy - int(lobe_r * 0.65), white, "top lobe should be white"),
        (cx, cy + int(lobe_r * 0.65), black, "bottom lobe should be black"),
        (cx, cy - lobe_offset, black, "top dot should be black"),
        (cx, cy + lobe_offset, white, "bottom dot should be white"),
    ]
    for x, y, expected, label in checks:
        got = px[x, y]
        if got != expected:
            raise SystemExit(f"{label} at ({x},{y}): expected {expected}, got {got}")


def main() -> None:
    verify_taiji_image()

    ASSETS.mkdir(parents=True, exist_ok=True)

    write_svg(ASSETS / "taiji-favicon.svg")
    write_svg(ROOT / "favicon.svg")

    for size in (16, 32, 48, 180):
        write_png(ASSETS / f"favicon-{size}.png", size)

    write_png(ASSETS / "taiji-favicon.png", 64)
    write_png(ROOT / "apple-touch-icon.png", 180)
    write_ico(ROOT / "favicon.ico")
    write_ico(ASSETS / "favicon.ico")

    verify_ico(ROOT / "favicon.ico")
    verify_ico(ASSETS / "favicon.ico")

    print("Inline SVG data URI:")
    print(taiji_data_uri())
    print("\nGenerated taiji favicon assets:")
    for path in sorted(
        [
            ROOT / "favicon.ico",
            ROOT / "favicon.svg",
            ROOT / "apple-touch-icon.png",
            ASSETS / "favicon.ico",
            ASSETS / "favicon-16.png",
            ASSETS / "favicon-32.png",
            ASSETS / "favicon-48.png",
            ASSETS / "favicon-180.png",
            ASSETS / "taiji-favicon.png",
            ASSETS / "taiji-favicon.svg",
        ]
    ):
        print(f"  {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
