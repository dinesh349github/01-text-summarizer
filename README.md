# 📝 AI Text Summarizer

A Streamlit app that summarizes long text into a configurable length and
style using Claude. Paste text directly or upload a `.txt` file.

## Features
- Paste text or upload a `.txt` file
- Choose summary length: short / medium / long
- Choose output style: bullet points / paragraph / executive summary
- Download the generated summary as a `.txt` file
- Clean error handling (missing API key, empty input)

## Tech stack
- Python 3.10+
- [Streamlit](https://streamlit.io/) — UI
- [Anthropic Claude API](https://docs.claude.com/) — summarization
- `python-dotenv` — local environment config

## Architecture
```
User input (text / .txt upload)
        │
        ▼
build_prompt()  ──►  Claude API (messages.create)
        │
        ▼
  Summary text  ──►  Streamlit UI + download button
```
`build_prompt()` and `summarize()` are pure-ish functions kept separate from
the Streamlit UI so they can be unit tested without hitting the real API
(see `test_app.py`, which mocks the Anthropic client).

## Setup

```bash
cd 01-text-summarizer
python3 -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt
cp .env.example .env
# edit .env and add your real ANTHROPIC_API_KEY
streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`).

## Running tests
```bash
python3 -m unittest test_app.py -v
```

## Deploying a live demo (free, ~5 min)
1. Push this folder to a public GitHub repo.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect the repo.
3. Add `ANTHROPIC_API_KEY` as a secret in the app settings.
4. Deploy — you get a public URL to put on your resume/LinkedIn.

## Suggested resume bullets
- Built and deployed an AI text summarization web app (Python, Streamlit,
  Claude API) supporting configurable summary length and format, with unit
  tests covering core prompt-construction logic.
- Designed a clean separation between UI and business logic to make LLM
  prompt behavior independently testable via mocking, avoiding live API
  calls in CI.
