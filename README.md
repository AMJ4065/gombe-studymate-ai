# Gombe StudyMate AI

Gombe StudyMate AI is an open-source educational web application designed to help students understand lecture notes, ask questions about their study materials, and practise with AI-generated multiple-choice quizzes.

The project aims to make personalised study support more accessible to students in Gombe, Nigeria, and beyond.

Features

- Ask questions: Get student-friendly explanations based on supplied lecture notes.
- Generate practice quizzes: Create five multiple-choice questions with four options each and an answer key with explanations.
- Responsive interface: A clean web interface for studying and revising.
- Local AI inference: Integrates with an open-weight Gemma model through Ollama.
- No account required: The MVP does not require registration or a database.
- Note privacy: The application does not intentionally save submitted notes to a database. Notes are processed to answer the current request.

Technology Stack

- Python 3.10+
- Flask
- HTML, CSS, and JavaScript
- "Ollama" (https://ollama.com/)
- "Gemma 3 1B" (https://ollama.com/library/gemma3:1b) for local AI development and testing
- "Render" (https://render.com/) for web hosting
- GitHub for source-code management

Prerequisites

Before running the project locally, install:

1. Python 3.10 or newer.
2. "Ollama for Windows" (https://ollama.com/download/windows).
3. Git (optional if you download the project ZIP instead of cloning the repository).

Gemma 3 1B is a relatively small model, but performance depends on available RAM, CPU, and other running applications.

Installation and Setup

1. Download the project

Clone the repository:

git clone https://github.com/AMJ4065/gombe-studymate-ai.git
cd gombe-studymate-ai

Alternatively, download the ZIP from GitHub and extract it.

2. Create a Python virtual environment

In VS Code, open the project folder and run:

py -m venv .venv

Activate the environment in PowerShell:

.\.venv\Scripts\Activate.ps1

If activation is blocked by your PowerShell execution policy, use Command Prompt:

.venv\Scripts\activate.bat

3. Install Python dependencies

With the virtual environment activated, run:

python -m pip install -r requirements.txt

4. Download Gemma 3 1B

Make sure Ollama is installed and running. Then download the model:

ollama pull gemma3:1b

Confirm the model is installed:

ollama list

You should see "gemma3:1b" in the model list.

5. Start the application

Run the Flask application from the project directory:

py app.py

Open the local application in your browser:

http://127.0.0.1:5000

Make sure Ollama is running and the model is available before testing the Ask a Question and Make a Quiz features.

Configuration

The application supports these environment variables:

Variable| Default| Purpose
"OLLAMA_URL"| "http://localhost:11434"| Ollama API address
"OLLAMA_MODEL"| "gemma3:1b"| Model tag used by the application

To select the model explicitly in Windows PowerShell:

$env:OLLAMA_MODEL="gemma3:1b"
py app.py

To use another model, download it through Ollama first and set "OLLAMA_MODEL" to the exact tag shown by "ollama list".

Running Tests

After starting the application:

1. Open the website in your browser.
2. Paste at least a few sentences of lecture notes.
3. Enter a question and test Ask a Question.
4. Select Make a Quiz and verify the generated questions, options, and answer key.
5. Try a short set of notes first if responses are slow.

AI-generated content can contain errors. Always verify important answers against your course materials.

Deployment

The web application can be hosted on a platform such as Render. However, the default Ollama address, "http://localhost:11434", refers to the machine running the Flask application.

When Flask runs on Render, "localhost" refers to the Render service—not your personal computer. Therefore, the hosted application cannot access Gemma running on your laptop through this address.

The public website needs a separately accessible AI endpoint before its AI features can work online. Do not publish a claim that hosted AI inference is working until it has been configured and tested.

Privacy and Responsible Use

- The MVP does not require a user account or database.
- Submitted notes are sent to the configured AI service to generate responses.
- The application does not intentionally persist study notes in a database.
- Avoid submitting passwords, personal records, or other sensitive information.
- AI-generated explanations and practice questions may be inaccurate. Verify important information against trusted learning materials.
- Generated questions are for practice and are not official examination questions.

Open Source and Contributions

This project is released under the MIT License. See ""LICENSE"" (LICENSE) for the licence terms.

Contributions, suggestions, bug reports, and improvements are welcome. Please open an issue to discuss a significant change before submitting a pull request.

Project Links

- Source code: https://github.com/AMJ4065/gombe-studymate-ai
- Live web application: https://gombe-studymate-ai.onrender.com

The live website may not have working AI features until a hosted AI endpoint is configured.

---

Built to support students in Gombe and beyond through accessible AI-assisted learning.
