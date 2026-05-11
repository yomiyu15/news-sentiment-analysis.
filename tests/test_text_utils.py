"""Tests for src.text_utils."""

import pytest

from src.text_utils import extract_publisher_domain, headline_char_length


@pytest.mark.parametrize(
    "publisher,expected",
    [
        ("analyst@reuters.com", "reuters.com"),
        ("  Jane.Doe@Bloomberg.COM  ", "bloomberg.com"),
        ("Reuters", "reuters"),
        ("", ""),
        (None, ""),
    ],
)
def test_extract_publisher_domain(publisher, expected):
    assert extract_publisher_domain(publisher) == expected


def test_headline_char_length():
    assert headline_char_length("Hello") == 5
    assert headline_char_length("") == 0
    assert headline_char_length(None) == 0
