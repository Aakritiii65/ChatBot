from flask import Flask, render_template, request, jsonify
import pyttsx3
import google.generativeai as genai

# ✅ Set your Google Gemini API Key
GENAI_API_KEY = "AIzaSyB0_Wd4BT0DCIh0Gu5f5eKdVNyvqnVT0qE"
genai.configure(api_key=GENAI_API_KEY)

app = Flask(__name__)

# ✅ Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('voice', engine.getProperty('voices')[0].id)

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_response(query):
    """Generate a response using Google Gemini AI."""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(query, generation_config=genai.GenerationConfig(
            max_output_tokens=100,
            temperature=0.7,
        ))

        if hasattr(response, "text"):
            return response.text
        elif hasattr(response, "candidates") and response.candidates:
            return response.candidates[0].content
        else:
            return "Sorry, I couldn't generate a response."

    except Exception as e:
        return f"Sorry, I encountered an error: {e}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("message", "")

    if user_query:
        bot_response = generate_response(user_query)
        return jsonify({"response": bot_response})
    
    return jsonify({"response": "Please enter a valid question!"})

if __name__ == "__main__":
    app.run(debug=True)
