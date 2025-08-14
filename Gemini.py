from flask import Flask, render_template, request
import os
from langchain_google_genai import ChatGoogleGenerativeAI

app = Flask(__name__)

os.environ["GOOGLE_API_KEY"] = "AIzaSyAzuDENAX-TCPYz3DSFfJEXsSAaaDVKX78"

def model(prompt):
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro")
    response = llm.invoke([("human", prompt)])
    return response.content

@app.route("/", methods=["GET", "POST"])
def home():
    ai_response = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        if prompt.strip():
            ai_response = model(prompt)
    return render_template("index.html", response=ai_response)

if __name__ == "__main__":
    app.run(debug=True)
