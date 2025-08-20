#!/usr/bin/env python3
"""
process_media.py
Automate video resizing, cropping, and bitrate settings in Python with platform presets.

Requires: ffmpeg installed and available on PATH.
Tested with Python 3.10+.

Usage examples:
  python process_media.py input.mp4 --preset instagram_reel
  python process_media.py input.mp4 --preset youtube_1080p --outdir outputs
  python process_media.py ./input_folder --preset instagram_reel,youtube_1080p

Optional overrides:
  --width 1080 --height 1920 --strategy cover --fps 30 --mode crf --crf 20
  --video-bitrate 6000k --audio-bitrate 128k
"""

import argparse
import subprocess
import json
import shutil
import sys
from pathlib import Path

VIDEO_EXTS = {".mp4", ".mov", ".m4v", ".mkv", ".avi", ".webm"}

def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        sys.exit("Error: ffmpeg is not installed or not in PATH.\n"
                 "Install it and try again (e.g., Windows: download from ffmpeg.org; "
                 "macOS: brew install ffmpeg; Ubuntu: sudo apt-get install ffmpeg).")

def load_presets(preset_path: Path) -> dict:
    if not preset_path.exists():
        sys.exit(f"Error: presets file not found at {preset_path}")
    with preset_path.open("r", encoding="utf-8") as f:
        return json.load(f)

def ensure_outdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def build_filter(width: int, height: int, strategy: str, pad_color: str = "black") -> str:
    """
    strategy 'cover': fill and center-crop to WxH (no letterbox)
    strategy 'contain': fit inside WxH and pad to WxH (letterbox/pillarbox)
    """
    if strategy == "cover":
        # Scale up to cover, then center-crop
        return (
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},setsar=1"
        )
    elif strategy == "contain":
        # Scale to fit, then pad to target
        return (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:{pad_color},setsar=1"
        )
    else:
        raise ValueError("strategy must be 'cover' or 'contain'")

def build_video_args(enc: dict) -> list:
    """
    enc: {
      'mode': 'bitrate' or 'crf',
      'video_bitrate': '6000k',
      'crf': 20,
      'x264_preset': 'medium'
    }
    """
    x264_preset = enc.get("x264_preset", "medium")
    args = ["-preset", x264_preset]
    mode = enc.get("mode", "bitrate").lower()
    if mode == "bitrate":
        vb = enc.get("video_bitrate", "5000k")
        # Use VBV for bitrate control
        args += ["-b:v", vb, "-maxrate", vb, "-bufsize", str(int(int(vb[:-1]) * 2)) + "k"]
    elif mode == "crf":
        crf = str(enc.get("crf", 20))
        args += ["-crf", crf, "-b:v", "0"]
    else:
        raise ValueError("encode.mode must be 'bitrate' or 'crf'")
    return args

def build_cmd(infile: Path, outfile: Path, p: dict) -> list:
    width = int(p["width"])
    height = int(p["height"])
    fps = int(p.get("fps", 30))
    strategy = p.get("strategy", "cover")
    pad_color = p.get("pad_color", "black")

    vcodec = p.get("vcodec", "libx264")
    pix_fmt = p.get("pix_fmt", "yuv420p")
    profile = p.get("profile", "high")
    audio_bitrate = p.get("audio_bitrate", "128k")

    vf = build_filter(width, height, strategy, pad_color)

    enc = p.get("encode", {"mode": "bitrate", "video_bitrate": "5000k", "x264_preset": "medium"})
    v_args = build_video_args(enc)

    # Build ffmpeg command
    cmd = [
        "ffmpeg", "-y",
        "-i", str(infile),
        "-vf", vf,
        "-r", str(fps),
        "-c:v", vcodec,
        "-profile:v", profile,
        "-pix_fmt", pix_fmt,
        *v_args,
        "-movflags", "+faststart",
        "-c:a", "aac",
        "-b:a", audio_bitrate,
        str(outfile),
    ]
    return cmd

def normalize_outname(stem: str, preset_name: str, container: str = "mp4") -> str:
    return f"{stem}_{preset_name}.{container}"

def process_one(infile: Path, outdir: Path, preset_name: str, p: dict, dry_run=False) -> int:
    container = p.get("container", "mp4")
    outfile = outdir / normalize_outname(infile.stem, preset_name, container)
    cmd = build_cmd(infile, outfile, p)
    if dry_run:
        print("DRY RUN:", " ".join(cmd))
        return 0
    print("Running:", " ".join(cmd))
    return subprocess.call(cmd)

def collect_inputs(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path]
    elif input_path.is_dir():
        files = []
        for ext in VIDEO_EXTS:
            files.extend(input_path.rglob(f"*{ext}"))
        if not files:
            print(f"Warning: No videos found in {input_path}")
        return sorted(files)
    else:
        sys.exit(f"Error: input path does not exist: {input_path}")

def apply_overrides(p: dict, args: argparse.Namespace) -> dict:
    # Shallow copy
    out = dict(p)
    if args.width: out["width"] = args.width
    if args.height: out["height"] = args.height
    if args.fps: out["fps"] = args.fps
    if args.strategy: out["strategy"] = args.strategy
    # Encode block
    enc = dict(out.get("encode", {}))
    if args.mode: enc["mode"] = args.mode
    if args.video_bitrate: enc["video_bitrate"] = args.video_bitrate
    if args.crf is not None:
        enc["mode"] = "crf"
        enc["crf"] = args.crf
    if args.x264_preset: enc["x264_preset"] = args.x264_preset
    out["encode"] = enc
    if args.audio_bitrate: out["audio_bitrate"] = args.audio_bitrate
    return out

def main():
    check_ffmpeg()

    ap = argparse.ArgumentParser(description="Batch render platform-specific video variants with ffmpeg.")
    ap.add_argument("input", help="Input video file OR folder containing videos")
    ap.add_argument("--preset", required=True,
                    help="Comma-separated preset names as defined in presets.json (e.g. instagram_reel,youtube_1080p)")
    ap.add_argument("--presets-file", default="presets.json", help="Path to presets.json")
    ap.add_argument("--outdir", default="outputs", help="Output directory")
    ap.add_argument("--dry-run", action="store_true", help="Print ffmpeg commands without running them")

    # Optional overrides
    ap.add_argument("--width", type=int)
    ap.add_argument("--height", type=int)
    ap.add_argument("--fps", type=int)
    ap.add_argument("--strategy", choices=["cover", "contain"])
    ap.add_argument("--mode", choices=["bitrate", "crf"])
    ap.add_argument("--video-bitrate", help="e.g. 6000k")
    ap.add_argument("--crf", type=int)
    ap.add_argument("--x264_preset", choices=["ultrafast","superfast","veryfast","faster","fast","medium","slow","slower","veryslow"])
    ap.add_argument("--audio-bitrate", help="e.g. 128k")

    args = ap.parse_args()

    presets = load_presets(Path(args.presets_file))
    names = [s.strip() for s in args.preset.split(",") if s.strip()]
    missing = [n for n in names if n not in presets]
    if missing:
        sys.exit(f"Error: Preset(s) not found in {args.presets_file}: {', '.join(missing)}")

    in_path = Path(args.input)
    outdir = Path(args.outdir)
    ensure_outdir(outdir)

    inputs = collect_inputs(in_path)
    if not inputs:
        sys.exit("No inputs to process.")

    exit_code = 0
    for infile in inputs:
        for n in names:
            base_p = presets[n]
            p = apply_overrides(base_p, args)
            code = process_one(infile, outdir, n, p, dry_run=args.dry_run)
            if code != 0:
                print(f"Error processing {infile} with preset {n} (exit {code})")
                exit_code = code

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
