from flask import Flask, render_template, request, send_file
import requests
import os
from io import BytesIO

app = Flask(__name__)

# Put your ElevenLabs API key here
ELEVENLABS_API_KEY = "sk_a9beb9de299e23948bc852f97d8b40ad7396a9ee3b93a0b0"

# The voice ID from ElevenLabs (choose one from your account)
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Example: 'Rachel'


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("text")

        if not text.strip():
            return render_template("txtvoi.html", error="Please enter some text.")

        # ElevenLabs API URL
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

        # API request
        response = requests.post(
            url,
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            },
            json={
                "text": text,
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
        )

        if response.status_code != 200:
            return render_template("txtvoi.html", error=f"API Error: {response.text}")

        # Save audio in memory
        audio_data = BytesIO(response.content)

        # Send file back to browser
        return send_file(
            audio_data,
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="speech.mp3"
        )

    return render_template("txtvoi.html")


if __name__ == "__main__":
    app.run(debug=True)
