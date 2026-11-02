"""Smoke tests for the Font-Awesome-Flask package.

These tests verify that the most critical functionality of the package works.
They are designed to catch major breakage and ensure basic operations succeed.
"""


def test_import() -> None:
    """Test importing the package."""
    import flask_font_awesome  # noqa: F401, PLC0415
