import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024  # 1 MB request limit

# Ollama configuration
OLLAMA_URL = os.getenv(
    "OLLAMA_URL", "http://localhost:11434"
).rstrip("/")

MODEL_NAME = os.getenv("OLLAMA_MODEL", "gemma3:1b")


def ask_model(prompt):
    """Send a prompt to Gemma through the Ollama API."""

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": MODEL_NAME,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are Gombe StudyMate, a patient educational "
                            "assistant. Help students understand their lecture "
                            "notes in clear, student-friendly English. Use the "
                            "provided notes as your primary source. If the notes "
                            "do not contain enough information, say so clearly "
                            "and distinguish general knowledge from the notes. "
                            "Never invent citations or claim that generated "
                            "questions are official examination questions."
                        ),
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                "stream": False,
                "options": {
                    "temperature": 0.3,
                },
            },
            timeout=180,
        )

        response.raise_for_status()
        data = response.json()

        answer = data.get("message", {}).get("content", "").strip()

        if not answer:
            raise RuntimeError("The model returned an empty response.")

        return answer

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Cannot connect to Ollama. Make sure Ollama is running "
            "and available at " + OLLAMA_URL
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "The model took too long to respond. Try shorter notes "
            "or close other applications to free up memory."
        ) from exc

    except requests.exceptions.HTTPError as exc:
        detail = ""

        try:
            detail = response.json().get("error", "")
        except (ValueError, AttributeError):
            pass

        raise RuntimeError(
            f"Ollama could not use model '{MODEL_NAME}'. "
            f"Check that it is installed using `ollama list`. {detail}"
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            "An error occurred while communicating with Ollama. "
            "Please check your Ollama service and try again."
        ) from exc


@app.get("/")
def index():
    return render_template("index.html", model_name=MODEL_NAME)


@app.post("/api/study")
def study():
    data = request.get_json(silent=True) or {}

    notes = (data.get("notes") or "").strip()
    question = (data.get("question") or "").strip()
    mode = (data.get("mode") or "explain").strip().lower()

    if len(notes) < 20:
        return jsonify(
            error="Please paste at least a few sentences of study notes."
        ), 400

    if len(notes) > 12000:
        return jsonify(
            error="Please keep the notes under 12,000 characters for this demo."
        ), 400

    if mode not in ("explain", "quiz"):
        return jsonify(error="Invalid study mode selected."), 400

    if mode == "quiz":
        prompt = (
            "Create a practice quiz based on the study notes below. "
            "Generate exactly 5 multiple-choice questions, each with "
            "four options labelled A, B, C, and D. Make the questions "
            "clear and appropriate for a student revising this material. "
            "After all questions, provide an answer key with a brief "
            "explanation for each correct answer. Base the questions "
            "on the supplied notes. If the notes are insufficient, "
            "be transparent. These are practice questions, not official "
            "examination questions.\n\n"
            f"STUDY NOTES:\n{notes}"
        )

    else:
        if not question:
            return jsonify(
                error="Enter a question about your notes."
            ), 400

        if len(question) > 2000:
            return jsonify(
                error="Please keep your question under 2,000 characters."
            ), 400

        prompt = (
            "Answer the student's question using the supplied study notes. "
            "Begin with a direct answer, explain the concept step by step, "
            "and finish with a short 'Remember' takeaway. Use examples "
            "when helpful. If the notes do not contain enough information, "
            "say so and clearly label any additional general knowledge.\n\n"
            f"STUDY NOTES:\n{notes}\n\n"
            f"STUDENT'S QUESTION:\n{question}"
        )

    try:
        answer = ask_model(prompt)

        return jsonify(
            answer=answer,
            model=MODEL_NAME,
        )

    except RuntimeError as exc:
        app.logger.warning("Study request failed: %s", exc)

        return jsonify(error=str(exc)), 503


@app.errorhandler(413)
def too_large(_error):
    return jsonify(
        error="Request is too large. Shorten the notes and try again."
    ), 413


if __name__ == "__main__":
    # Local development only. Do not use Flask's debug server in production.
    app.run(debug=True)
