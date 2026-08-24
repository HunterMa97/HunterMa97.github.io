#!/usr/bin/env python3
"""Generate north-star favicon assets from assets/img/north-star.png."""

from __future__ import annotations

import struct
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "img"
SOURCE = ASSETS / "north-star.png"
ZOOM = 2.0  # center crop so the star appears 2x larger in the icon frame


def load_cropped_source() -> Image.Image:
    if not SOURCE.exists():
        raise SystemExit(f"Missing source image: {SOURCE}")

    src = Image.open(SOURCE).convert("RGBA")
    width, height = src.size
    crop_size = int(min(width, height) / ZOOM)
    left = (width - crop_size) // 2
    top = (height - crop_size) // 2
    return src.crop((left, top, left + crop_size, top + crop_size))


def render_icon(size: int) -> Image.Image:
    return load_cropped_source().resize((size, size), Image.Resampling.LANCZOS)


def write_png(path: Path, size: int) -> None:
    render_icon(size).convert("RGB").save(path, format="PNG", optimize=True)


def _png_bytes(image: Image.Image) -> bytes:
    buf = BytesIO()
    image.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def write_ico(path: Path) -> None:
    sizes = [16, 32, 48]
    png_entries = [(size, _png_bytes(render_icon(size))) for size in sizes]

    header = struct.pack("<HHH", 0, 1, len(png_entries))
    offset = 6 + 16 * len(png_entries)
    directory = bytearray()
    image_data = bytearray()

    for size, png in png_entries:
        directory.extend(struct.pack("<BBBBHHII", size, size, 0, 0, 1, 32, len(png), offset))
        image_data.extend(png)
        offset += len(png)

    path.write_bytes(header + directory + image_data)


def verify_ico(path: Path) -> None:
    data = path.read_bytes()
    if len(data) < 6:
        raise SystemExit(f"{path}: ICO too small")
    reserved, icotype, count = struct.unpack("<HHH", data[:6])
    if reserved != 0 or icotype != 1:
        raise SystemExit(f"{path}: invalid ICO header")
    if count < 2:
        raise SystemExit(f"{path}: expected multiple icon sizes, got {count}")


def verify_icon_image(size: int = 64) -> None:
    img = render_icon(size).convert("RGB")
    px = img.load()
    center = px[size // 2, size // 2]
    corner = px[2, 2]
    if sum(center) < sum(corner):
        raise SystemExit("icon center should be brighter than the corner background")


def main() -> None:
    verify_icon_image()

    ASSETS.mkdir(parents=True, exist_ok=True)

    for size in (16, 32, 48, 180):
        write_png(ASSETS / f"favicon-{size}.png", size)

    write_png(ASSETS / "north-star-favicon.png", 64)
    write_png(ROOT / "apple-touch-icon.png", 180)
    write_ico(ROOT / "favicon.ico")
    write_ico(ASSETS / "favicon.ico")

    verify_ico(ROOT / "favicon.ico")
    verify_ico(ASSETS / "favicon.ico")

    print("Generated north-star favicon assets:")
    for path in sorted(
        [
            ROOT / "favicon.ico",
            ROOT / "apple-touch-icon.png",
            ASSETS / "favicon.ico",
            ASSETS / "favicon-16.png",
            ASSETS / "favicon-32.png",
            ASSETS / "favicon-48.png",
            ASSETS / "favicon-180.png",
            ASSETS / "north-star-favicon.png",
            SOURCE,
        ]
    ):
        print(f"  {path.relative_to(ROOT)} ({path.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
