"""
AI Text Summarizer
-------------------
Paste or upload text and get a concise, configurable summary using Claude.
Supports adjustable length and output style (bullets / paragraph / executive summary).
"""

import os
import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "claude-3-5-sonnet-latest"

LENGTH_MAP = {
    "Short (2-3 sentences)": "in 2-3 sentences",
    "Medium (1 paragraph)": "in a single concise paragraph",
    "Long (detailed)": "in detail, covering all key points, in 2-4 paragraphs",
}

STYLE_MAP = {
    "Bullet points": "Format the summary as bullet points.",
    "Paragraph": "Format the summary as flowing prose.",
    "Executive summary": (
        "Format the summary as an executive summary with a bolded one-line "
        "takeaway followed by supporting bullet points."
    ),
}


def get_client() -> Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set. Add it to your .env file.")
    return Anthropic(api_key=api_key)


def build_prompt(text: str, length: str, style: str) -> str:
    """Pure function (no API calls) so it can be unit tested in isolation."""
    return (
        f"Summarize the following text {LENGTH_MAP[length]}. "
        f"{STYLE_MAP[style]}\n\n"
        f"TEXT:\n{text}"
    )


def summarize(client: Anthropic, text: str, length: str, style: str) -> str:
    prompt = build_prompt(text, length, style)
    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def main():
    st.set_page_config(page_title="AI Text Summarizer", page_icon="📝")
    st.title("📝 AI Text Summarizer")
    st.caption("Paste text or upload a .txt file. Get a clean summary in seconds.")

    uploaded = st.file_uploader("Upload a .txt file (optional)", type=["txt"])
    default_text = uploaded.read().decode("utf-8") if uploaded else ""

    text = st.text_area("Or paste text here", value=default_text, height=250)

    col1, col2 = st.columns(2)
    with col1:
        length = st.selectbox("Summary length", list(LENGTH_MAP.keys()), index=1)
    with col2:
        style = st.selectbox("Style", list(STYLE_MAP.keys()), index=0)

    if st.button("Summarize", type="primary"):
        if not text.strip():
            st.warning("Please paste some text or upload a file first.")
            return
        with st.spinner("Summarizing..."):
            try:
                client = get_client()
                summary = summarize(client, text, length, style)
                st.subheader("Summary")
                st.write(summary)
                st.download_button("Download summary", summary, file_name="summary.txt")
            except Exception as e:
                st.error(f"Something went wrong: {e}")


if __name__ == "__main__":
    main()
