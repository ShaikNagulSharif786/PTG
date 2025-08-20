import whisper
import re
import sys
import os

# Check if user provided an audio file as argument
if len(sys.argv) < 2:
    print("⚠️ Please drag & drop an audio file onto this script or run: python Day8_srt_english.py <audiofile>")
    sys.exit(1)

audio_path = sys.argv[1]

if not os.path.exists(audio_path):
    print(f"❌ File not found: {audio_path}")
    sys.exit(1)

# Load Whisper model
print("⏳ Loading Whisper model... (first time may take a while)")
model = whisper.load_model("small")

# Transcribe audio
print(f"🎤 Transcribing: {audio_path}")
result = model.transcribe(audio_path)

# Function to format time in SRT style
def format_timestamp(seconds: float) -> str:
    millis = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hrs:02}:{mins:02}:{secs:02},{millis:03}"

# Merge segments into full sentences
srt_content = ""
buffer_text = ""
start_time, end_time = None, None
counter = 1

for seg in result['segments']:
    text = seg['text'].strip()
    if not buffer_text:  # start new sentence
        start_time = seg['start']
    buffer_text += (" " if buffer_text else "") + text
    end_time = seg['end']

    # Flush at sentence end OR if segment too long (>7 sec)
    if re.search(r"[.!?]$", text) or (end_time - start_time > 7):
        srt_content += f"{counter}\n{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n{text.strip()}\n\n"
        counter += 1
        buffer_text = ""

# Flush any leftover text
if buffer_text:
    srt_content += f"{counter}\n{format_timestamp(start_time)} --> {format_timestamp(end_time)}\n{buffer_text.strip()}\n\n"

# Save SRT file
output_file = os.path.splitext(audio_path)[0] + "_english.srt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"✅ English-only SRT file generated: {output_file}")
