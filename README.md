# Bad Apple!! — Terminal ASCII Player

Play **Bad Apple!!** as animated ASCII art right in your Linux terminal.

## Requirements

- Python 3.10+
- `ffmpeg`
- `yt-dlp` (only needed for the automatic first download)

On Ubuntu/Kubuntu/Debian:

```bash
sudo apt update
sudo apt install ffmpeg yt-dlp
```

## Run it

Clone the repository and start the player:

```bash
git clone https://github.com/xxSwar4jxx/badapple.git
cd badapple
python3 badapple.py
```

The first run downloads the video into the repository directory. Later runs reuse that local copy.

## Options

```bash
python3 badapple.py --width 100
python3 badapple.py --fps 18
python3 badapple.py --video ~/Videos/bad_apple.mp4
```

- `--width`: ASCII frame width; defaults to your terminal width.
- `--fps`: playback frame rate; defaults to 24.
- `--video`: play a local video file instead of the default download.

Press **Ctrl+C** to stop. The terminal cursor is restored when playback ends.

## Troubleshooting

- If automatic downloading fails, update `VIDEO_URL` in `badapple.py` or provide a local video with `--video`.
- If playback looks too wide or is slow, try a smaller `--width`, such as `80`.
