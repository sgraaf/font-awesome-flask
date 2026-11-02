from collections.abc import Iterator

import pytest
from flask import Flask, render_template_string

from flask_font_awesome import FontAwesome

CDN = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome"


@pytest.fixture
def font_awesome() -> Iterator[FontAwesome]:
    app = Flask(__name__)
    font_awesome = FontAwesome(app)
    with app.app_context():
        yield font_awesome


def test_load_js_defaults(font_awesome: FontAwesome) -> None:
    assert font_awesome.load_js() == (
        f'<script defer src="{CDN}/{FontAwesome.version}/js/all.min.js" '
        f'integrity="{FontAwesome.js_sri_map["all"]}" crossorigin="anonymous"></script>'
    )


def test_load_passes_version_and_style(font_awesome: FontAwesome) -> None:
    markup = font_awesome.load(version="6.5.2", style="solid", use_css=True)
    assert f'href="{CDN}/6.5.2/css/solid.min.css"' in markup
    assert f'href="{CDN}/6.5.2/css/fontawesome.min.css"' in markup


def test_load_rejects_non_free_style(font_awesome: FontAwesome) -> None:
    with pytest.raises(ValueError, match="`style` must be one of"):
        font_awesome.load_css(style="light")


def test_render_icon(font_awesome: FontAwesome) -> None:
    assert font_awesome.render_icon("fas fa-house", size="2x", rotation=90) == (
        '<i class="fas fa-house fa-2x fa-rotate-90" aria-hidden="true"></i>'
    )


def test_render_stacked_icon(font_awesome: FontAwesome) -> None:
    assert font_awesome.render_stacked_icon(
        "fas fa-square", "fas fa-house", inverse=True
    ) == (
        '<span class="fa-stack" aria-hidden="true">\n'
        '    <i class="fas fa-square fa-stack-2x"></i>\n'
        '    <i class="fas fa-house fa-stack-1x fa-inverse"></i>\n'
        "</span>"
    )


@pytest.mark.usefixtures("font_awesome")
def test_available_in_templates() -> None:
    assert render_template_string("{{ font_awesome.render_icon('fas fa-house') }}") == (
        '<i class="fas fa-house" aria-hidden="true"></i>'
    )
