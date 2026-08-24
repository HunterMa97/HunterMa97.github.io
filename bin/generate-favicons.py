#!/usr/bin/env python3
"""Generate polaris (north star) favicon assets for the landing page."""

from __future__ import annotations

import math
import struct
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "img"

# Eight-point north star: long N/S axis, medium E/W, short diagonals.
POLARIS_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" fill="#ffffff" />
  <polygon fill="#111111" points="32,4 36.5,23 56,23 40,34 45.5,54 32,43 18.5,54 24,34 8,23 27.5,23" />
</svg>
"""


def polaris_data_uri() -> str:
    compact = " ".join(POLARIS_SVG.split())
    return "data:image/svg+xml," + quote(compact)


def polaris_points(cx: float, cy: float, scale: float) -> list[tuple[float, float]]:
    radii = [28, 11, 20, 11, 28, 11, 20, 11]
    points: list[tuple[float, float]] = []
    for i, radius in enumerate(radii):
        angle = math.radians(-90 + i * 45)
        points.append((cx + radius * scale * math.cos(angle), cy + radius * scale * math.sin(angle)))
    return points


def draw_polaris(size: int) -> Image.Image:
    cx = cy = size / 2.0
    scale = size / 64.0
    black = (17, 17, 17)
    white = (255, 255, 255)

    img = Image.new("RGB", (size, size), white)
    draw = ImageDraw.Draw(img)
    draw.polygon(polaris_points(cx, cy, scale), fill=black)
    return img


def write_png(path: Path, size: int) -> None:
    draw_polaris(size).save(path, format="PNG", optimize=True)


def _png_bytes(image: Image.Image) -> bytes:
    from io import BytesIO

    buf = BytesIO()
    image.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def write_ico(path: Path) -> None:
    sizes = [16, 32, 48]
    png_entries = [(size, _png_bytes(draw_polaris(size))) for size in sizes]

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
    path.write_text(POLARIS_SVG.strip() + "\n", encoding="utf-8")


def verify_ico(path: Path) -> None:
    data = path.read_bytes()
    if len(data) < 6:
        raise SystemExit(f"{path}: ICO too small")
    reserved, icotype, count = struct.unpack("<HHH", data[:6])
    if reserved != 0 or icotype != 1:
        raise SystemExit(f"{path}: invalid ICO header")
    if count < 2:
        raise SystemExit(f"{path}: expected multiple icon sizes, got {count}")


def verify_polaris_image(size: int = 64) -> None:
    cx = cy = size // 2
    img = draw_polaris(size)
    px = img.load()
    white = (255, 255, 255)
    black = (17, 17, 17)

    checks = [
        (cx, max(1, cy - size // 4), black, "north tip should be black"),
        (cx, min(size - 2, cy + size // 4), black, "south tip should be black"),
        (2, 2, white, "corner should stay white"),
        (cx, cy, black, "center should be black"),
    ]
    for x, y, expected, label in checks:
        got = px[x, y]
        if got != expected:
            raise SystemExit(f"{label} at ({x},{y}): expected {expected}, got {got}")


def main() -> None:
    verify_polaris_image()

    ASSETS.mkdir(parents=True, exist_ok=True)

    write_svg(ASSETS / "polaris-favicon.svg")
    write_svg(ROOT / "favicon.svg")

    for size in (16, 32, 48, 180):
        write_png(ASSETS / f"favicon-{size}.png", size)

    write_png(ASSETS / "polaris-favicon.png", 64)
    write_png(ROOT / "apple-touch-icon.png", 180)
    write_ico(ROOT / "favicon.ico")
    write_ico(ASSETS / "favicon.ico")

    verify_ico(ROOT / "favicon.ico")
    verify_ico(ASSETS / "favicon.ico")

    print("Inline SVG data URI:")
    print(polaris_data_uri())
    print("\nGenerated polaris favicon assets:")
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
            ASSETS / "polaris-favicon.png",
            ASSETS / "polaris-favicon.svg",
        ]
    ):
        print(f"  {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
