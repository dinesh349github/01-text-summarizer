"""
Unit tests for app.py — uses unittest.mock so tests run without any
real API key or network call.
"""

import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import build_prompt, summarize


class TestBuildPrompt(unittest.TestCase):
    def test_short_bullets(self):
        prompt = build_prompt("Some article text.", "Short (2-3 sentences)", "Bullet points")
        self.assertIn("2-3 sentences", prompt)
        self.assertIn("bullet points", prompt.lower())
        self.assertIn("Some article text.", prompt)

    def test_executive_summary_style(self):
        prompt = build_prompt("Quarterly report.", "Long (detailed)", "Executive summary")
        self.assertIn("executive summary", prompt.lower())
        self.assertIn("Quarterly report.", prompt)


class TestSummarize(unittest.TestCase):
    def test_summarize_calls_client_and_extracts_text(self):
        class FakeBlock:
            type = "text"
            text = "This is the summary."

        class FakeResponse:
            content = [FakeBlock()]

        class FakeMessages:
            def create(self, **kwargs):
                self.last_kwargs = kwargs
                return FakeResponse()

        class FakeClient:
            messages = FakeMessages()

        client = FakeClient()
        result = summarize(client, "long text here", "Medium (1 paragraph)", "Paragraph")
        self.assertEqual(result, "This is the summary.")


if __name__ == "__main__":
    unittest.main()
