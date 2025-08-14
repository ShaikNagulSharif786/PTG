# Day 4 – Script-to-Scene Mapping & API Integration

## Overview
This project demonstrates **script-to-scene mapping** by integrating multiple AI APIs to generate creative outputs programmatically.  
The workflow includes:
1. **Text-to-Voice** conversion using **ElevenLabs API**.
2. **Text-to-Image/Video** generation using **RunwayML API**.
3. **Prompt generation** using **Gemini API**.
4. A **Flask**-based web interface to interact with each API.

The implementation follows the **Day 4** task requirement of combining narrative beats (scripts) with visual/audio outputs.

---

## Features
- **ElevenLabs Integration** – Convert generated or provided text into realistic speech.
- **RunwayML Integration** – Convert text prompts into images or short videos.
- **Gemini Integration** – Generate creative prompts from given text for better scene mapping.
- **Flask Web App** – User-friendly web pages for each API, allowing direct interaction.
- **Template Structure** – Organized HTML templates for different API functionalities.


## File Structure

project-root/
│
├── Elevenlabs.py # Flask route for ElevenLabs API
├── Runwayml.py # Flask route for RunwayML API
├── Gemini.py # Flask route for Gemini API
│
├── templates/
│ ├── Elevenlabs.html # HTML UI for ElevenLabs integration
│ ├── Runwayml.html # HTML UI for RunwayML integration
│ ├── Gemini.html # HTML UI for Gemini integration
│
└── README.md # Project documentation



## Tools & Technologies
- **Languages**: Python 3, HTML5
- **Framework**: Flask
- **APIs**:  
  - OpenAI API *(for generating script text)*
  - ElevenLabs API *(text-to-speech conversion)*
  - RunwayML API *(text-to-image/video generation)*
  - Gemini API *(prompt generation)*
- **Utilities**: Python `requests`, Postman for API testing


## How It Works
1. **User inputs** text/script in the Flask web app.
2. **Gemini API** can be used to enhance or transform the text into a better prompt.
3. **ElevenLabs API** converts text to audio output.
4. **RunwayML API** converts the text/prompt into an image or short video.
5. The results are displayed directly on the web page.


## Setup Instructions
1. **Clone this repository**:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. Install dependencies:
pip install flask requests

3. Add your API keys:

Open the Python files (Elevenlabs.py, Runwayml.py, Gemini.py)

Replace the placeholder API keys with your actual keys.

4. Run the Flask app:

python Elevenlabs.py
python Runwayml.py
python Gemini.py

(Each API can be run separately depending on your need.)

5. Open in browser:

Go to http://127.0.0.1:5000/ for ElevenLabs

Go to http://127.0.0.1:5001/ for RunwayML

Go to http://127.0.0.1:5002/ for Gemini
(Port numbers may vary based on your configuration.)

Evaluation Criteria (Task Requirement)

✅ API usage fluency

✅ Mapping visuals to narrative beats

✅ Integration of multiple APIs into a functional workflow