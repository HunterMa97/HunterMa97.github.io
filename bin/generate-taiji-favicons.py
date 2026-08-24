#!/usr/bin/env python3
"""Generate taiji favicon assets for the landing page."""

from __future__ import annotations

import struct
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "img"

TAIJI_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="32" fill="#ffffff" />
  <path d="M32 0a32 32 0 0 1 0 64 16 16 0 0 1 0-32 16 16 0 0 0 0-32z" fill="#111111" />
  <circle cx="32" cy="16" r="5" fill="#111111" />
  <circle cx="32" cy="48" r="5" fill="#ffffff" />
</svg>
"""


def taiji_data_uri() -> str:
    compact = " ".join(TAIJI_SVG.split())
    return "data:image/svg+xml," + quote(compact)


def draw_taiji(size: int) -> Image.Image:
    scale = size / 64.0
    cx = cy = size / 2.0
    outer_r = 32 * scale
    lobe_r = 16 * scale
    dot_r = max(1, round(5 * scale))
    black = (17, 17, 17)
    white = (255, 255, 255)

    def ellipse_box(x: float, y: float, r: float) -> tuple[float, float, float, float]:
        return (x - r, y - r, x + r, y + r)

    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    draw.ellipse(ellipse_box(cx, cy, outer_r), fill=(*white, 255))

    black_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bd = ImageDraw.Draw(black_layer)
    bd.pieslice(ellipse_box(cx, cy, outer_r), start=270, end=90, fill=(*black, 255))
    bd.ellipse(ellipse_box(cx, cy - 16 * scale, lobe_r), fill=(*black, 255))
    layer = Image.alpha_composite(layer, black_layer)

    draw = ImageDraw.Draw(layer)
    draw.ellipse(ellipse_box(cx, cy + 16 * scale, lobe_r), fill=(*white, 255))
    draw.ellipse(ellipse_box(cx, cy - 16 * scale, dot_r), fill=(*black, 255))
    draw.ellipse(ellipse_box(cx, cy + 16 * scale, dot_r), fill=(*white, 255))

    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse(ellipse_box(cx, cy, outer_r), fill=255)
    result = Image.new("RGB", (size, size), white)
    result.paste(layer, mask=mask)
    return result


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


def main() -> None:
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
