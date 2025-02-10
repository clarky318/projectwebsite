from flask import Flask, request, jsonify
import openai  # For AI email enhancement
import language_tool_python  # For grammar correction
from gtts import gTTS  # For text-to-speech
import os

app = Flask(__name__)

# Initialize grammar tool
tool = language_tool_python.LanguageTool('en-US')

# OpenAI API Key (Replace with your own key)
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route("/enhance", methods=["POST"])
def enhance_email():
    data = request.json
    email_text = data.get("email_text")
    tone = data.get("tone", "Professional")

    if not email_text:
        return jsonify({"error": "No email text provided"}), 400

    # Enhance email using OpenAI API
    prompt = f"Improve the following email for a travel agency with a {tone} tone:\n{email_text}"
    
    response = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}]
    )
    enhanced_email = response["choices"][0]["message"]["content"]

    return jsonify({"enhanced_email": enhanced_email})

@app.route("/fix_grammar", methods=["POST"])
def fix_grammar():
    data = request.json
    email_text = data.get("email_text")

    if not email_text:
        return jsonify({"error": "No email text provided"}), 400

    corrected_text = tool.correct(email_text)
    return jsonify({"corrected_email": corrected_text})

@app.route("/text_to_speech", methods=["POST"])
def text_to_speech():
    data = request.json
    email_text = data.get("email_text")

    if not email_text:
        return jsonify({"error": "No email text provided"}), 400

    tts = gTTS(text=email_text, lang="en")
    tts.save("static/email_audio.mp3")

    return jsonify({"audio_url": "/static/email_audio.mp3"})

if __name__ == "__main__":
    app.run(debug=True)
