<!-- start docs-include-index -->

# Font-Awesome-Flask

[![PyPI](https://img.shields.io/pypi/v/Font-Awesome-Flask)](https://img.shields.io/pypi/v/Font-Awesome-Flask)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/Font-Awesome-Flask)](https://pypi.org/project/Font-Awesome-Flask/)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sgraaf/font-awesome-flask/main.svg)](https://results.pre-commit.ci/latest/github/sgraaf/font-awesome-flask/main)
[![Documentation Status](https://readthedocs.org/projects/font-awesome-flask/badge/?version=latest)](https://font-awesome-flask.readthedocs.io/en/latest/?badge=latest)
[![PyPI - License](https://img.shields.io/pypi/l/Font-Awesome-Flask)](https://img.shields.io/pypi/l/Font-Awesome-Flask)

Font-Awesome-Flask is an extension for [Flask](https://flask.palletsprojects.com/en/latest/) that adds support for [Font Awesome](https://fontawesome.com/) to your web application. It adds methods to load Font Awesome's resources (both `Web Fonts + CSS` and `SVG + JS` are supported) and render icons.

<!-- end docs-include-index -->

## Installation

<!-- start docs-include-installation -->

### From PyPI

Font-Awesome-Flask is available on [PyPI](https://pypi.org/project/Font-Awesome-Flask/). Install with `pip` or your package manager of choice:

```bash
pip install Font-Awesome-Flask
```

### From source

If you'd like, you can also install Font-Awesome-Flask from source (with [`flit`](https://flit.readthedocs.io/en/latest/)):

```bash
git clone https://github.com/sgraaf/font-awesome-flask.git
cd font-awesome-flask
python3 -m pip install flit
flit install
```

<!-- end docs-include-installation -->

## Documentation

Check out the [Font-Awesome-Flask documentation](https://font-awesome-flask.readthedocs.io/en/stable/) for the [User's Guide](https://font-awesome-flask.readthedocs.io/en/stable/usage.html) and [API Reference](https://font-awesome-flask.readthedocs.io/en/stable/api.html).

## Example

### Configuration

Font-Awesome-Flask can be configured via the [Flask configuration API](https://flask.palletsprojects.com/en/latest/config/), using the `config` attribute of the `Flask` object. These are the available configuration values along with their description:

| Configuration value        | Default | Description                                                        |
| -------------------------- | ------- | ------------------------------------------------------------------ |
| `FONT_AWESOME_SERVE_LOCAL` | `False` | Whether to serve Font Awesome's resources locally or from the CDN. |

### Initialization

<!-- start docs-include-initialization -->

Initialize the extension with the Flask application normally...:

```python
from flask import Flask
from flask_font_awesome import FontAwesome

app = Flask(__name__)
font_awesome = FontAwesome(app)
```

... or using the [Application Factory](https://flask.palletsprojects.com/en/latest/patterns/appfactories/) pattern:

```python
from flask import Flask
from flask_font_awesome import FontAwesome

font_awesome = FontAwesome()


def create_app():
    app = Flask(__name__)
    font_awesome.init_app(app)
    return app
```

<!-- end docs-include-initialization -->

### Loading resources

Font-Awesome-Flask provides three helper methods to load Font Awesome's resources: `font_awesome.load()`, `font_awesome.load_js()` and `font_awesome.load_css()`.

Font Awesome can be used either via [Web Fonts + CSS or via SVG + JS](https://fontawesome.com/docs/web/dig-deeper/webfont-vs-svg). Use the `load_css()` method for the former, and `load_js()` for the latter. You can also use the more general `load()`, which defaults to `SVG + JS`.

Whichever resource(s) you end up using, you can load them by including any of the `load()` methods in the head of your base template:

<!-- prettier-ignore -->
```html
<head>
    ...
    {{ font_awesome.load_js() }}
    ...
</head>
<body>
    ...
</body>
```

### Rendering icons

Font-Awesome-Flask provides two ways of rendering icons: via the `font_awesome.render_icon()` and `font_awesome.render_stacked_icons()` methods...:

```python
{{font_awesome.render_icon("fas fa-house")}}
{{font_awesome.render_stacked_icons("fas fa-square", "fas fa-house")}}
```

... or via the [Jinja macros](https://jinja.palletsprojects.com/en/latest/templates/#macros) of the same names:

```
{% from 'font_awesome.html' import render_icon, render_stacked_icons %}
{{ render_icon('fas fa-house') }}
{{ render_stacked_icons('fas fa-square', 'fasfa-house') }}
```
