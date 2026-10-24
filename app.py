import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB request limit

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("OLLAMA_MODEL", "gemma4:e2b")


def ask_model(prompt):
    """Call an Ollama model. Raise a readable error if it is unavailable."""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are Gombe StudyMate, a patient study assistant. "
                            "Use the student's supplied notes as the primary source. "
                            "If the notes do not contain the answer, say so clearly and "
                            "separate general knowledge from information in the notes. "
                            "Never invent citations or claim certainty when unsure. "
                            "Explain concepts in clear, student-friendly English."
                        ),
                    },
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
                "options": {"temperature": 0.3},
            },
            timeout=150,
        )
        response.raise_for_status()
        data = response.json()
        answer = data.get("message", {}).get("content", "").strip()
        if not answer:
            raise RuntimeError("The model returned an empty response.")
        return answer
    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Ollama is not running. Install/start Ollama, then run "
            f"`ollama run {MODEL_NAME}` in a terminal."
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "The model took too long to respond. Try shorter notes or a smaller model."
        ) from exc
    except requests.exceptions.HTTPError as exc:
        detail = ""
        try:
            detail = response.json().get("error", "")
        except Exception:
            pass
        raise RuntimeError(
            f"Ollama could not use model '{MODEL_NAME}'. "
            f"Run `ollama pull {MODEL_NAME}`. {detail}"
        ) from exc


@app.get("/")
def index():
    return render_template("index.html", model_name=MODEL_NAME)


@app.post("/api/study")
def study():
    data = request.get_json(silent=True) or {}
    notes = (data.get("notes") or "").strip()
    question = (data.get("question") or "").strip()
    mode = (data.get("mode") or "explain").strip()

    if len(notes) < 20:
        return jsonify(error="Please paste at least a few sentences of study notes."), 400
    if len(notes) > 12000:
        return jsonify(error="Please keep the notes under 12,000 characters for this demo."), 400

    if mode == "quiz":
        prompt = (
            "Create a practice quiz based only on these study notes. "
            "Write 5 multiple-choice questions, each with options A-D. "
            "After all questions, provide an answer key with a brief explanation "
            "for each answer. Do not claim these are official exam questions.\n\n"
            f"STUDY NOTES:\n{notes}"
        )
    else:
        if not question:
            return jsonify(error="Enter a question about your notes."), 400
        prompt = (
            "Answer the student's question using the supplied notes. "
            "Start with a direct answer, then explain step by step, and finish "
            "with a short 'Remember' takeaway. If the notes do not contain enough "
            "information, be transparent.\n\n"
            f"STUDY NOTES:\n{notes}\n\nQUESTION:\n{question}"
        )

    try:
        answer = ask_model(prompt)
        return jsonify(answer=answer, model=MODEL_NAME)
    except RuntimeError as exc:
        return jsonify(error=str(exc)), 503


@app.errorhandler(413)
def too_large(_error):
    return jsonify(error="Request is too large. Shorten the notes and try again."), 413


if __name__ == "__main__":
    app.run(debug=True)
