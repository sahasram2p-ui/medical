from flask import Flask, render_template, request, jsonify
from google import genai
from config import GEMINI_API_KEY, GEMINI_MODEL

app = Flask(__name__)
client = genai.Client(api_key=GEMINI_API_KEY)

MEDICAL_PROMPT = """
You are a Medical and Health information-only AI chatbot.
Answer ONLY questions about medicine and health: anatomy, common diseases,
symptoms, prevention, nutrition, medicines and their general uses, tests,
first aid, public health, and healthcare terminology.
Do not diagnose users, prescribe medicines, or recommend changing dosage.
For personal medical concerns, advise consulting a qualified healthcare
professional. For emergencies or life-threatening symptoms, advise seeking
immediate emergency medical care or contacting local emergency services.
For software, programming, web development, electronics, agriculture,
sports, movies, politics, or other unrelated topics, reply exactly:
"Sorry, I can answer only medical and health-related questions."
Keep answers clear, educational, and safety-focused.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "error": "No data received."}), 400
        user_message = data.get("message", "").strip()
        if not user_message:
            return jsonify({"success": False, "error": "Please enter a message."}), 400
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=f"{MEDICAL_PROMPT}\n\nUser question:\n{user_message}"
        )
        return jsonify({"success": True, "reply": response.text})
    except Exception as e:
        print("ERROR:", repr(e))
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
