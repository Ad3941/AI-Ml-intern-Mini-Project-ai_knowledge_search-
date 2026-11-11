import pytest
from src.loader import load_file

def test_load_text_file():
    content = b"Hello, Python world!"
    filename = "test.txt"
    text = load_file(content, filename)
    assert text == "Hello, Python world!"

def test_load_markdown_file():
    content = b"# Markdown Header"
    filename = "test.md"
    text = load_file(content, filename)
    assert text == "# Markdown Header"