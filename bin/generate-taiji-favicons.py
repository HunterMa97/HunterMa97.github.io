#!/usr/bin/env python3
"""Generate taiji favicon assets for the landing page."""

from __future__ import annotations

import struct
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "img"


def draw_taiji(size: int) -> Image.Image:
    scale = size / 64.0
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx = cy = size / 2.0
    outer_r = 30 * scale
    stroke = max(1, round(3 * scale))

    def ellipse_box(x: float, y: float, r: float) -> tuple[float, float, float, float]:
        return (x - r, y - r, x + r, y + r)

    # White disk with dark outline.
    draw.ellipse(ellipse_box(cx, cy, outer_r), fill="#ffffff", outline="#111111", width=stroke)

    # Black teardrop on the right (matches favicon.svg path).
    teardrop = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    td = ImageDraw.Draw(teardrop)
    td.pieslice(ellipse_box(cx, cy, outer_r), start=270, end=90, fill="#111111")
    small_r = 15 * scale
    td.ellipse(ellipse_box(cx, cy - 15 * scale, small_r), fill="#111111")
    td.ellipse(ellipse_box(cx, cy + 15 * scale, small_r), fill="#ffffff")
    img = Image.alpha_composite(img, teardrop)

    # Reinforce the S-curve lobes and dots for small sizes.
    draw = ImageDraw.Draw(img)
    draw.ellipse(ellipse_box(cx, cy - 15 * scale, small_r), fill="#ffffff", outline="#111111", width=max(1, stroke // 2))
    draw.ellipse(ellipse_box(cx, cy + 15 * scale, small_r), fill="#111111", outline="#111111", width=max(1, stroke // 2))

    dot_r = max(1, round(5 * scale))
    draw.ellipse(ellipse_box(cx, cy - 15 * scale, dot_r), fill="#111111")
    draw.ellipse(ellipse_box(cx, cy + 15 * scale, dot_r), fill="#ffffff")

    return img.convert("RGB")


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
    path.write_text(
        """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <circle cx="32" cy="32" r="30" fill="#ffffff" stroke="#111111" stroke-width="3" />
  <path d="M32 2a30 30 0 0 1 0 60 15 15 0 0 1 0-30 15 15 0 0 0 0-30z" fill="#111111" />
  <circle cx="32" cy="17" r="15" fill="#ffffff" />
  <circle cx="32" cy="47" r="15" fill="#111111" />
  <circle cx="32" cy="17" r="5" fill="#111111" />
  <circle cx="32" cy="47" r="5" fill="#ffffff" />
</svg>
""",
        encoding="utf-8",
    )


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

    print("Generated taiji favicon assets:")
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
