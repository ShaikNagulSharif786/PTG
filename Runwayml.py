from flask import Flask, render_template, request
import requests
import base64

app = Flask(__name__)

# Put your RunwayML API key here
RUNWAY_API_KEY = "YOUR_RUNWAYML_API_KEY"

# Model to use (check your Runway account for available models)
MODEL_ID = "stable-diffusion-v1-5"  # Example model

@app.route("/", methods=["GET", "POST"])
def index():
    image_data_url = None
    error = None

    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        
        if not prompt:
            error = "Please enter some text."
        else:
            try:
                url = f"https://api.runwayml.com/v1/models/{MODEL_ID}/generate"

                headers = {
                    "Authorization": f"Bearer {RUNWAY_API_KEY}",
                    "Content-Type": "application/json"
                }

                payload = {
                    "prompt": prompt,
                    "width": 512,
                    "height": 512,
                    "num_images": 1
                }

                response = requests.post(url, headers=headers, json=payload)

                if response.status_code != 200:
                    error = f"Runway API Error: {response.text}"
                else:
                    data = response.json()

                    # Runway usually returns Base64 image data
                    if "images" in data and len(data["images"]) > 0:
                        img_base64 = data["images"][0]
                        image_data_url = f"data:image/png;base64,{img_base64}"
                    else:
                        error = "No image returned from API."

            except Exception as e:
                error = str(e)

    return render_template("index.html", image=image_data_url, error=error)


if __name__ == "__main__":
    app.run(debug=True)
