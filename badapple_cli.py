"""Play Bad Apple!! as ASCII art in a Linux terminal."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

VIDEO_URL = "https://www.youtube.com/watch?v=FtutLA63Cp8"
CACHE_DIR = Path.home() / ".cache" / "badapple"
VIDEO_FILE = CACHE_DIR / "bad_apple.mp4"
RAMP = " .'^,:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"


def require_program(name: str) -> None:
    if shutil.which(name) is None:
        print(f"Missing required program: {name}", file=sys.stderr)
        print("Install it with your Linux package manager and try again.", file=sys.stderr)
        raise SystemExit(1)


def download_video() -> None:
    if VIDEO_FILE.exists() and VIDEO_FILE.stat().st_size > 0:
        return
    require_program("yt-dlp")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    print("Downloading Bad Apple!! video (this may take a while)...")
    result = subprocess.run(
        [
            "yt-dlp", "--no-playlist",
            "-f", "best[height<=480][ext=mp4]/best[height<=480]/best",
            "--merge-output-format", "mp4",
            "-o", str(VIDEO_FILE), VIDEO_URL,
        ],
        check=False,
    )
    if result.returncode != 0 or not VIDEO_FILE.exists():
        print(
            f"\nDownload failed. Put a video at {VIDEO_FILE}, "
            "or run badapple --video /path/to/video.mp4.",
            file=sys.stderr,
        )
        raise SystemExit(result.returncode or 1)


def play(video: Path, fps: float, width: int | None) -> None:
    require_program("ffmpeg")
    terminal = shutil.get_terminal_size(fallback=(100, 36))
    frame_width = max(20, width or terminal.columns)
    frame_height = max(8, min(terminal.lines - 1, frame_width * 9 // 32))
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-i", str(video),
        "-vf", f"fps={fps},scale={frame_width}:{frame_height}:flags=bilinear,format=gray",
        "-an", "-f", "rawvideo", "-pix_fmt", "gray", "pipe:1",
    ]
    frame_bytes = frame_width * frame_height
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    delay = 1.0 / fps
    sys.stdout.write("\033[2J\033[?25l")
    sys.stdout.flush()
    try:
        assert process.stdout is not None
        next_frame = time.perf_counter()
        while True:
            frame = process.stdout.read(frame_bytes)
            if len(frame) != frame_bytes:
                break
            lines = []
            for y in range(frame_height):
                row = frame[y * frame_width : (y + 1) * frame_width]
                lines.append("".join(RAMP[pixel * (len(RAMP) - 1) // 256] for pixel in row))
            sys.stdout.write("\033[H" + "\n".join(lines))
            sys.stdout.flush()
            next_frame += delay
            remaining = next_frame - time.perf_counter()
            if remaining > 0:
                time.sleep(remaining)
        code = process.wait()
        if code:
            raise SystemExit(code)
    except KeyboardInterrupt:
        print("\n\nStopped.")
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
        sys.stdout.write("\033[?25h\n")
        sys.stdout.flush()


def main() -> None:
    parser = argparse.ArgumentParser(description="Play Bad Apple!! as terminal ASCII art.")
    parser.add_argument("--video", type=Path, help="use a local video instead of downloading")
    parser.add_argument("--fps", type=float, default=24, help="playback frame rate (default: 24)")
    parser.add_argument("--width", type=int, help="ASCII width (default: terminal width)")
    args = parser.parse_args()
    if args.fps <= 0:
        parser.error("--fps must be greater than zero")
    if args.width is not None and args.width < 20:
        parser.error("--width must be at least 20")
    video = args.video.expanduser().resolve() if args.video else VIDEO_FILE
    if not video.exists():
        if args.video:
            parser.error(f"video file not found: {video}")
        download_video()
    play(video, args.fps, args.width)


if __name__ == "__main__":
    main()
