Quick Start — Media Presets Automator

What this does (in simple words):
• Takes a source video and makes platform‑ready copies for Instagram Reels, TikTok, YouTube, etc.
• Each platform copy can have different size (resizing), frame shape (cropping), and file size/quality (bitrate or CRF).
• You trigger everything with one Python command, instead of doing it manually every time.

Prereqs:
1) Install Python 3.10+
2) Install FFmpeg and add it to PATH (Windows: download ffmpeg.org and add /bin to PATH; macOS: brew install ffmpeg; Ubuntu: sudo apt-get install ffmpeg).

Files:
- process_media.py  → the script you run
- presets.json      → platform settings (you can edit or add more)
- outputs/          → will be created for results

Basic usage:
    python process_media.py input.mp4 --preset instagram_reel
    python process_media.py input.mp4 --preset instagram_reel,youtube_1080p
    python process_media.py ./input_folder --preset tiktok_vertical

Override example (optional):
    python process_media.py input.mp4 --preset instagram_reel --strategy contain --mode crf --crf 20 --fps 24

Where do results go?
• Default output folder is ./outputs
• Filenames look like: input_instagram_reel.mp4, input_youtube_1080p.mp4

How cropping works:
• strategy=cover   → fills target size and center‑crops (no black bars)
• strategy=contain → fits inside target size and pads (letterbox/pillarbox)

Troubleshooting:
• If you get 'ffmpeg not found' install or add it to PATH.
• If Instagram/TikTok rejects the file, try lowering bitrate (e.g., 5000k) or using CRF mode with a slightly higher CRF number (22–24).

Customize presets:
• Open presets.json and duplicate a block to make your own preset.
• Common fields: width, height, fps, strategy, encode.mode('bitrate' or 'crf'), video_bitrate or crf, audio_bitrate.