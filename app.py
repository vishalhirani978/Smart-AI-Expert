import sys
import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from router.main_router import get_expert_answer

app = Flask(
    __name__,
    static_folder='static',
    template_folder='templates'
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message.strip():
            return jsonify({"error": "Empty message"}), 400

        result = get_expert_answer(user_message)

        return jsonify({
            "success":         True,
            "question":        result["question"],
            "intent":          result["intent"],
            "lead_model":      result["lead_model"],
            "lead_answer":     result["lead_answer"],
            "support_answers": result["support_answers"],
            "final_answer":    result["final_answer"],
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error":   str(e)
        }), 500

# Health check for Render
@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        debug=False,
        host="0.0.0.0",
        port=port
    )