"""Formatted tweet text test fixtures."""
import pytest


@pytest.fixture
def formatted_text():
    """Return properly formatted tweet text (str)."""
    text = """TweetsToText is a bot that lives on Twitter.

It collects your tweets into plain text files.

So you can take your brilliant observations somewhere else.

This bot was made in the RJI Futures Lab."""

    return text
