# Gombe StudyMate AI

A small, open-source AI study assistant designed to help students turn lecture notes into understandable explanations and practice quizzes.

## Features

- Ask questions about pasted lecture notes.
- Generate five multiple-choice practice questions with an answer key.
- Clean, responsive web interface.
- Uses an open-weight Gemma model through Ollama.
- No database or account required for this MVP.
- Notes are processed for the request and are not saved by this app.

## Tech stack

- Python 3.10+
- Flask
- HTML, CSS, JavaScript
- Ollama
- Gemma 4 (`gemma4:e2b` by default)

## Prerequisites

1. Install Python 3.10 or newer.
2. Install Ollama: https://ollama.com/download
3. Open a terminal and download the model:

```bash
ollama pull gemma4:e2b
```

The first model download can take time and requires free disk space. Check current model tags and hardware requirements in the Ollama/Gemma documentation if this tag is unavailable.

## Run locally (Windows PowerShell)

Open this folder in VS Code, then in the terminal run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
ollama run gemma4:e2b
```

Leave Ollama available, then open a **second terminal** in VS Code and run:

```powershell
.\.venv\Scripts\Activate.ps1
python app.py
```

Open http://127.0.0.1:5000 in your browser.

If PowerShell blocks virtual-environment activation, use Command Prompt instead:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python app.py
```

Make sure the Ollama app is running and the model is downloaded before testing the Ask or Quiz buttons.

## Configuration

The default model is `gemma4:e2b`. To use another model already installed in Ollama, set `OLLAMA_MODEL` before starting Flask.

PowerShell example:

```powershell
$env:OLLAMA_MODEL="gemma3:1b"
python app.py
```

Use the actual model tag returned by `ollama list`. Do not claim Gemma 4 was used if you changed the model.

## Open source

This project is released under the MIT License. Contributions, bug reports, and improvements are welcome.

## Responsible use

AI-generated answers may be inaccurate. Students should verify important information against course materials. The app is a learning aid, not an official exam source.

## Hackathon submission note

Before submitting, test both modes on your laptop, confirm the repository is public, and include a short screen recording or live demo if possible. Only list AI tools and technologies that were actually used.
