# Bad Apple!! — Terminal ASCII Player

Play **Bad Apple!!** as animated ASCII art right in your Linux terminal.

## Install with pip

First install the system tools (they are not Python packages):

```bash
sudo apt update
sudo apt install ffmpeg yt-dlp
```

Then install the player:

```bash
python3 -m pip install --user badapple-terminal
```

If your Linux distribution blocks user pip installs into its system Python, use a virtual environment or `pipx` instead. With pipx:

```bash
sudo apt install pipx ffmpeg yt-dlp
pipx ensurepath
pipx install badapple-terminal
```

Open a new terminal if needed, then run:

```bash
badapple
```

The first run downloads the video into `~/.cache/badapple/`; subsequent runs reuse it.

## Options

```bash
badapple --width 100
badapple --fps 18
badapple --video ~/Videos/bad_apple.mp4
```

- `--width`: ASCII frame width; defaults to your terminal width.
- `--fps`: playback frame rate; defaults to 24.
- `--video`: play a local video file instead of downloading the default video.

Press **Ctrl+C** to stop. The terminal cursor is restored when playback ends.

## Run from source

```bash
git clone https://github.com/xxSwar4jxx/badapple.git
cd badapple
python3 badapple.py
```

## Requirements

- Python 3.10+
- `ffmpeg` for converting video frames
- `yt-dlp` for the automatic first download (optional if using `--video`)

## Troubleshooting

- If `badapple` is not found after installation, reopen the terminal or check that your user scripts directory is on `PATH`.
- If automatic downloading fails, update `VIDEO_URL` in `badapple_cli.py` or provide a local video with `--video`.
- If playback looks too wide or is slow, try `badapple --width 80`.
- The package name on pip is `badapple-terminal`; the command you run is `badapple`.

Repository: https://github.com/xxSwar4jxx/badapple
