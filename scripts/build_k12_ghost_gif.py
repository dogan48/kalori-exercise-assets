"""12 keyframes + ghost (alpha blend) tweens -> GIF."""
from __future__ import annotations

import os
from pathlib import Path

from PIL import Image

ASSETS = Path(r"C:\Users\Dogan\.cursor\projects\C-Users-Dogan-Projects\assets")
OUT_GIF = Path(r"C:\Users\Dogan\Projects\kalori-exercise-assets\squat-k12-ghost.gif")
GHOST_STEPS = 4  # blends between each keyframe pair (excluding endpoints)
FRAME_MS = 88
SIZE = 512


def keyframe_paths() -> list[Path]:
    paths = [ASSETS / "squat-k12-01.jpg"]
    for i in range(2, 13):
        paths.append(ASSETS / f"squat-k12-{i:03d}.jpg")
    missing = [p for p in paths if not p.exists()]
    if missing:
        raise SystemExit(f"Missing keyframes: {missing}")
    return paths


def load_rgb(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def build_sequence(keyframes: list[Image.Image], steps: int) -> list[Image.Image]:
    out: list[Image.Image] = []
    n = len(keyframes)
    for i in range(n):
        a = keyframes[i]
        b = keyframes[(i + 1) % n]
        out.append(a)
        for s in range(1, steps + 1):
            t = s / (steps + 1)
            out.append(Image.blend(a, b, t))
    return out


def main() -> None:
    paths = keyframe_paths()
    kf = [load_rgb(p) for p in paths]
    frames = build_sequence(kf, GHOST_STEPS)
    OUT_GIF.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUT_GIF,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_MS,
        loop=0,
        optimize=True,
    )
    print(OUT_GIF, "keyframes", len(kf), "gif_frames", len(frames), "bytes", OUT_GIF.stat().st_size)


if __name__ == "__main__":
    main()
