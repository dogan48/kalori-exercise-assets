"""6 keyframes + ghost blends; fixed paths for squat-k6-*.jpg in assets."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ASSETS = Path(r"C:\Users\Dogan\.cursor\projects\C-Users-Dogan-Projects\assets")
OUT_GIF = Path(r"C:\Users\Dogan\Projects\kalori-exercise-assets\squat-k6-ghost.gif")
GHOST_STEPS = 6
FRAME_MS = 90
SIZE = 512


def keyframe_paths() -> list[Path]:
    paths = [ASSETS / "squat-k6-01.jpg"]
    for i in range(2, 7):
        paths.append(ASSETS / f"squat-k6-{i:03d}.jpg")
    missing = [p for p in paths if not p.exists()]
    if missing:
        raise SystemExit(f"Missing: {missing}")
    return paths


def load_rgb(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB").resize((SIZE, SIZE), Image.Resampling.LANCZOS)


def build_sequence(keyframes: list[Image.Image], steps: int) -> list[Image.Image]:
    out: list[Image.Image] = []
    n = len(keyframes)
    for i in range(n):
        a, b = keyframes[i], keyframes[(i + 1) % n]
        out.append(a)
        for s in range(1, steps + 1):
            out.append(Image.blend(a, b, s / (steps + 1)))
    return out


def main() -> None:
    kf = [load_rgb(p) for p in keyframe_paths()]
    frames = build_sequence(kf, GHOST_STEPS)
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
