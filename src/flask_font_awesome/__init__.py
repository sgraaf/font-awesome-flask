"""Font-Awesome-Flask is an extension for Flask that adds support for Font Awesome to your web application."""
import re
import sys
import urllib.request
from pathlib import Path
from typing import Optional, Union

from flask import Blueprint, Flask, Markup, current_app, url_for

__version__ = "0.1.1"

STATIC_FOLDER = Path(__file__).parent / "static"
CDN_URL_TEMPLATE = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/{version}/{type}/{style}{possibly_min}.{ext}"
VERSION_PATTERN = re.compile(r"Font Awesome (?:Free\s)?(\d+.\d+.\d+)")


def _remove_prefix(s: str, prefix: str) -> str:
    if sys.version_info < (3, 9):
        return s[len(prefix) :] if s.startswith(prefix) else s
    return s.removeprefix(prefix)


class FontAwesome:
    """Font Awesome icons for Flask."""

    style = "all"
    style_choices = ("all", "regular", "solid", "brands")
    core_style = "fontawesome"
    use_min = True
    use_css = False
    version = "6.2.0"
    css_sri_map = {
        "all": "sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==",
        "regular": "sha512-aNH2ILn88yXgp/1dcFPt2/EkSNc03f9HBFX0rqX3Kw37+vjipi1pK3L9W08TZLhMg4Slk810sPLdJlNIjwygFw==",
        "solid": "sha512-uj2QCZdpo8PSbRGL/g5mXek6HM/APd7k/B5Hx/rkVFPNOxAQMXD+t+bG4Zv8OAdUpydZTU3UHmyjjiHv2Ww0PA==",
        "brands": "sha512-+oRH6u1nDGSm3hH8poU85YFIVTdSnS2f+texdPGrURaJh8hzmhMiZrQth6l56P4ZQmxeZzd2DqVEMqQoJ8J89A==",
        "fontawesome": "sha512-uj2QCZdpo8PSbRGL/g5mXek6HM/APd7k/B5Hx/rkVFPNOxAQMXD+t+bG4Zv8OAdUpydZTU3UHmyjjiHv2Ww0PA==",
    }
    js_sri_map = {
        "all": "sha512-naukR7I+Nk6gp7p5TMA4ycgfxaZBJ7MO5iC3Fp6ySQyKFHOGfpkSZkYVWV5R7u7cfAicxanwYQ5D1e17EfJcMA==",
        "regular": "sha512-Kcbb5bDGCQQwo67YHS9uDvRmyrNEqHLPA1Kmn0eqrritqGDp3OpkBGvHk36GNEH44MtWM1L5k3i9MSQPMkNIuA==",
        "solid": "sha512-dcTe66qF6q/NW1X64tKXnDDcaVyRowrsVQ9wX6u7KSQpYuAl5COzdMIYDg+HqAXhPpIz1LO9ilUCL4qCbHN5Ng==",
        "brands": "sha512-1e+6G7fuQ5RdPcZcRTnR3++VY2mjeh0+zFdrD580Ell/XcUw/DQLgad5XSCX+y2p/dmJwboZYBPoiNn77YAL5A==",
        "fontawesome": "sha512-j3gF1rYV2kvAKJ0Jo5CdgLgSYS7QYmBVVUjduXdoeBkc4NFV4aSRTi+Rodkiy9ht7ZYEwF+s09S43Z1Y+ujUkA==",
    }
    webfonts_map = {
        "regular": "fa-regular-400",
        "solid": "fa-solid-900",
        "brands": "fa-brands-400",
    }

    def __init__(self, app: Optional[Flask] = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """Initialize the Flask application for use with this extension instance."""
        # register extension instance with the Flask application
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["font_awesome"] = self

        # create and register blueprint for this extension instance
        blueprint = Blueprint(
            "font_awesome",
            __name__,
            static_folder=STATIC_FOLDER.name,
            static_url_path=f"/font_awesome{app.static_url_path}",
            template_folder="templates",
        )
        app.register_blueprint(blueprint)

        # register extension instance with the Jinja2 environment (for use in templates)
        app.jinja_env.globals["font_awesome"] = self

        # set default configuration values for this extension instance
        app.config.setdefault("FONT_AWESOME_SERVE_LOCAL", False)

    @staticmethod
    def _get_file(
        style: str, use_min: bool, ext: str, type: Optional[str] = None
    ) -> Path:
        """Get the file path for the given style, extension, and possibly-minified suffix."""
        possibly_min = ".min" if use_min else ""
        return (
            STATIC_FOLDER
            / (type if type is not None else ext)
            / f"{style}{possibly_min}.{ext}"
        )

    @staticmethod
    def _get_url(
        version: str,
        style: str,
        use_min: bool,
        ext: str,
        serve_local: bool,
        type: Optional[str] = None,
    ) -> str:
        """Get the URL for the given version, style, extension, and possibly-minified suffix."""
        possibly_min = ".min" if use_min else ""
        if serve_local:
            return url_for(
                "font_awesome.static", filename=f"{ext}/{style}{possibly_min}.{ext}"
            )
        return CDN_URL_TEMPLATE.format(
            version=version,
            type=type if type is not None else ext,
            style=style,
            possibly_min=possibly_min,
            ext=ext,
        )

    @staticmethod
    def _get_version(file: Path) -> Optional[str]:
        """Get the version from the given file."""
        match = VERSION_PATTERN.search(file.read_text())
        return match.group(1) if match is not None else None

    @classmethod
    def _request_file(
        cls,
        version: str,
        style: str,
        use_min: bool,
        ext: str,
        file: Path,
        type: Optional[str] = None,
    ) -> None:
        """Request the file for serving locally."""
        file.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(
            cls._get_url(version, style, use_min, ext, False, type)
        ) as response:
            file.write_bytes(response.read())

    @classmethod
    def _request_webfont_files(
        cls,
        version: str,
        webfont_style: str,
    ) -> None:
        """Request the webfont files (ttf and woff2) for serving locally."""
        _type = "webfonts"
        for ext in ("ttf", "woff2"):
            file = cls._get_file(webfont_style, False, ext, _type)
            cls._request_file(version, webfont_style, False, ext, file, _type)

    @classmethod
    def _possibly_request_file(
        cls, version: str, style: str, use_min: bool, ext: str
    ) -> None:
        """Possibly request the file for serving locally."""
        file = cls._get_file(style, use_min, ext)
        if not file.exists() or cls._get_version(file) != version:
            cls._request_file(version, style, use_min, ext, file)
            if ext == "css":  # also request webfonts
                if style == "all":
                    for _style in cls.style_choices[1:]:
                        webfont_style = cls.webfonts_map[_style]
                        cls._request_webfont_files(version, webfont_style)
                else:
                    webfont_style = cls.webfonts_map[style]
                    cls._request_webfont_files(version, webfont_style)

    def load(
        self,
        version: str = version,
        style: str = style,
        css_sri: str = css_sri_map[style],
        core_css_sri: str = css_sri_map[core_style],
        js_sri: str = js_sri_map[style],
        core_js_sri: str = js_sri_map[core_style],
        use_min: bool = use_min,
        use_css: bool = use_css,
    ) -> Markup:
        """Load Font Awesome's `WebFonts + CSS <https://fontawesome.com/docs/web/setup/host-yourself/webfonts>`_ / `SVG + JS <https://fontawesome.com/docs/web/setup/host-yourself/svg-js>`_ resources for the given version. Defaults to `SVG + JS`.

        Some examples:
            >>> font_awesome.load()
            >>> font_awesome.load(style="solid", use_css=True)
            >>> font_awesome.load(
            ...     version="5.9.0",
            ...     js_sri="sha512-q3eWabyZPc1XTCmF+8/LuE1ozpg5xxn7iO89yfSOd5/oKvyqLngoNGsx8jq92Y8eXJ/IRxQbEC+FGSYxtk2oiw=="
            ... )

        Args:
            version (str): The version to load. Defaults to `6.2.0`.
            style (str): The `icon style(s) <https://fontawesome.com/v6/docs/web/dig-deeper/styles>`_ to load. Defaults to `all`.
            css_sri (str): The `Subresource Integrity (SRI) <https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity>`_ for the CSS resource file when not served locally. Defaults to `sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==`.
            core_css_sri (str): The `SRI <https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity>`_ for the core CSS resource file when not served locally. Defaults to `sha512-uj2QCZdpo8PSbRGL/g5mXek6HM/APd7k/B5Hx/rkVFPNOxAQMXD+t+bG4Zv8OAdUpydZTU3UHmyjjiHv2Ww0PA==`.
            js_sri (str): The `SRI <https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity>`_ for the JS resource file when not served locally. Defaults to `sha512-naukR7I+Nk6gp7p5TMA4ycgfxaZBJ7MO5iC3Fp6ySQyKFHOGfpkSZkYVWV5R7u7cfAicxanwYQ5D1e17EfJcMA==`.
            core_js_sri (str): The `SRI <https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity>`_ for the core JS resource file when not served locally. Defaults to `sha512-j3gF1rYV2kvAKJ0Jo5CdgLgSYS7QYmBVVUjduXdoeBkc4NFV4aSRTi+Rodkiy9ht7ZYEwF+s09S43Z1Y+ujUkA==`.
            use_min (bool): Whether to use the minified resource or not. Defaults to `True`.
            use_css (bool): Whether to use `WebFonts + CSS <https://fontawesome.com/docs/web/setup/host-yourself/webfonts>`_ over `SVG + JS <https://fontawesome.com/docs/web/setup/host-yourself/svg-js>`_. Defaults to `False`.

        Raises:
            ValueError: When trying to load a non-free icon style (i.e. not one of `all`, `regular`, `solid`, or `brands`)

        Returns:
            flask.Markup: The HTML markup for the WebFonts + CSS / SVG + JS resource(s).
        """
        if use_css:
            return self.load_css(style, version, css_sri, core_css_sri, use_min)
        return self.load_js(style, version, js_sri, core_js_sri, use_min)

    def load_css(
        self,
        version: str = version,
        style: str = style,
        sri: str = css_sri_map[style],
        core_sri: str = css_sri_map[core_style],
        use_min: bool = use_min,
    ) -> Markup:
        """Load Font Awesome's `WebFonts + CSS <https://fontawesome.com/docs/web/setup/host-yourself/webfonts>`_ resources for the given version.

        Some examples:
            >>> font_awesome.load_css()
            >>> font_awesome.load_css(style="regular")

        Args:
            version (str): The version to load. Defaults to `6.2.0`.
            style (str): The `icon style(s) <https://fontawesome.com/v6/docs/web/dig-deeper/styles>`_ to load. Defaults to `all`.
            sri (str): The `Subresource Integrity (SRI) <https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity>`_ for the CSS resource file when not served locally. Defaults to `sha512-xh6O/CkQoPOWDdYTDqeRdPCVd1SpvCA9XXcUnZS2FmJNp1coAFzvtCN9BmamE+4aHK8yyUHUSCcJHgXloTyT2A==`.
            core_sri (str): The `SRI <https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity>`_ for the core CSS resource file when not served locally. Defaults to `sha512-uj2QCZdpo8PSbRGL/g5mXek6HM/APd7k/B5Hx/rkVFPNOxAQMXD+t+bG4Zv8OAdUpydZTU3UHmyjjiHv2Ww0PA==`.
            use_min (bool): Whether to use the minified resources or not. Defaults to `True`.

        Raises:
            ValueError: When trying to load a non-free icon style (i.e. not one of `all`, `regular`, `solid`, or `brands`)

        Returns:
            flask.Markup: The HTML markup for the WebFonts + CSS resources.
        """
        if style not in self.style_choices:
            raise ValueError(f"`style` must be one of {', '.join(self.style_choices)}")

        serve_local = current_app.config["FONT_AWESOME_SERVE_LOCAL"]
        ext = "css"

        url = self._get_url(version, style, use_min, ext, serve_local)
        if serve_local:
            self._possibly_request_file(version, style, use_min, ext)
            css = f'<link rel="stylesheet" href="{url}" />'
        else:
            css = f'<link rel="stylesheet" href="{url}" integrity="{sri}" crossorigin="anonymous" />'

        if style != "all":
            core_url = self._get_url(
                version, self.core_style, use_min, ext, serve_local
            )
            if serve_local:
                self._possibly_request_file(version, self.core_style, use_min, ext)
                css += f'\n<link rel="stylesheet" href="{core_url}" />'
            else:
                css += f'\n<link rel="stylesheet" href="{core_url}" integrity="{core_sri}" crossorigin="anonymous" />'

        return Markup(css)

    def load_js(
        self,
        version: str = version,
        style: str = style,
        sri: str = js_sri_map[style],
        core_sri: str = js_sri_map[core_style],
        use_min: bool = use_min,
    ) -> Markup:
        """Load Font Awesome's `SVG + JS <https://fontawesome.com/docs/web/setup/host-yourself/svg-js>`_ resource for the given version.

        Some examples:
            >>> font_awesome.load_js()
            >>> font_awesome.load_js(
            ...     use_min=False,
            ...     sri="sha512-8XtSBQOB+R4dpcpQBpYC5Q7ti7y/MjIF0l/1ZiSd4xM04Dr052S/Py981Pzmwo2HrXCR2JhYE1MYR15aZGMnig=="
            ... )

        Args:
            version (str): The version to load. Defaults to `6.2.0`.
            style (str): The `icon style(s) <https://fontawesome.com/v6/docs/web/dig-deeper/styles>`_ to load. Defaults to `all`.
            sri (str): The `SRI <https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity>`_ for the JS resource file when not served locally. Defaults to `sha512-naukR7I+Nk6gp7p5TMA4ycgfxaZBJ7MO5iC3Fp6ySQyKFHOGfpkSZkYVWV5R7u7cfAicxanwYQ5D1e17EfJcMA==`.
            core_sri (str): The `SRI <https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity>`_ for the core JS resource file when not served locally. Defaults to `sha512-j3gF1rYV2kvAKJ0Jo5CdgLgSYS7QYmBVVUjduXdoeBkc4NFV4aSRTi+Rodkiy9ht7ZYEwF+s09S43Z1Y+ujUkA==`.
            use_min (bool): Whether to use the minified resource or not. Defaults to `True`.

        Raises:
            ValueError: When trying to load a non-free icon style (i.e. not one of `all`, `regular`, `solid`, or `brands`)

        Returns:
            flask.Markup: The HTML markup for the SVG + JS resource.
        """
        if style not in self.style_choices:
            raise ValueError(f"`style` must be one of {', '.join(self.style_choices)}")

        serve_local = current_app.config["FONT_AWESOME_SERVE_LOCAL"]
        ext = "js"

        url = self._get_url(version, style, use_min, ext, serve_local)
        if serve_local:
            self._possibly_request_file(version, style, use_min, ext)
            js = f'<script defer src="{url}"></script>'
        else:
            js = f'<script defer src="{url}" integrity="{sri}" crossorigin="anonymous"></script>'

        if style != "all":
            core_url = self._get_url(
                version, self.core_style, use_min, ext, serve_local
            )
            if serve_local:
                self._possibly_request_file(version, self.core_style, use_min, ext)
                js += f'\n<script defer src="{core_url}"></script>'
            else:
                js += f'\n<script defer src="{core_url}" integrity="{core_sri}" crossorigin="anonymous"></script>'

        return Markup(js)

    def render_icon(
        self,
        name: str,
        inverse: bool = False,
        size: Optional[str] = None,
        fixed_with: bool = False,
        rotation: Optional[Union[str, int]] = None,
        animation: Optional[str] = None,
        border: bool = False,
        pull: Optional[str] = None,
        swap_opacity: bool = False,
        aria_hidden: bool = True,
        style: Optional[str] = None,
        _stack_size: Optional[str] = None,
    ) -> Markup:
        """Render an icon.

        See the `Font Awesome documentation <https://fontawesome.com/search?o=r&m=free>`_ for the complete list of available icons.

        Some examples:
            >>> font_awesome.render_icon('fas fa-house')
            >>> font_awesome.render_icon('fa-regular fa-square', size='xl')
            >>> font_awesome.render_icon('fab fa-github', inverse=True, rotation=90)

        Args:
            name (str): The name of the icon (e.g. `fa-solid fa-user`).
            inverse (bool): Inverts the color of the icon to white. Defaults to `False`.
            size (Optional[str]): The `relative or literal size <https://fontawesome.com/v6/docs/web/style/size>`_ of the icon. Defaults to `None`.
            fixed_with (bool): Set the icon to a `fixed width <https://fontawesome.com/v6/docs/web/style/fixed-width>`_ for easy vertical alignment. Defaults to `False`.
            rotation (Optional[Union[str, int]]): `Rotate or flip <https://fontawesome.com/v6/docs/web/style/rotate>`_ the icon. Defaults to `None`.
            animation (Optional[str]): `Animate <https://fontawesome.com/v6/docs/web/style/animate>`_ the icon. Defaults to `None`.
            border (bool): Add a `border <https://fontawesome.com/v6/docs/web/style/pull>`_ to the icon. Defaults to `False`.
            pull (Optional[str]): `Pull <https://fontawesome.com/v6/docs/web/style/pull>`_ the icon left or right. Defaults to `None`.
            swap_opacity (bool): Swap the default opacity of each layer in a `duotone <https://fontawesome.com/v6/docs/web/style/duotone>`_ icon. Defaults to `False`.
            aria_hidden (bool): Add the `aria-hidden` attribute to the icon. Defaults to `True`.
            style (Optional[str]): Customize the icon even further using `CSS styling <https://fontawesome.com/v6/docs/web/style/custom>`_. Defaults to `None`.

        Returns:
            flask.Markup: The HTML markup for the icon.
        """
        icon = f'<i class="{name}'
        if _stack_size:
            icon += f" fa-stack-{_remove_prefix(_stack_size, 'fa-stack-')}"
        if inverse:
            icon += " fa-inverse"
        if size is not None:
            icon += f" fa-{_remove_prefix(size, 'fa-')}"
        if fixed_with:
            icon += " fa-fw"
        if rotation is not None:
            if isinstance(rotation, int):
                rotation = f"rotate-{rotation}"
            icon += f" fa-{_remove_prefix(rotation, 'fa-')}"
        if animation is not None:
            icon += f" fa-{_remove_prefix(animation, 'fa-')}"
        if border:
            icon += " fa-border"
        if pull is not None:
            icon += f" fa-pull-{_remove_prefix(pull, 'fa-pull-')}"
        if swap_opacity:
            icon += " fa-swap-opacity"
        icon += '"'
        if style is not None:
            icon += f' style="{style}"'
        if aria_hidden:
            icon += ' aria-hidden="true"'
        icon += "></i>"
        return Markup(icon)

    def render_stacked_icon(
        self,
        name_1: str,
        name_2: str,
        stack_size_1: str = "2x",
        stack_size_2: str = "1x",
        inverse: bool = False,
        size: Optional[str] = None,
        aria_hidden: bool = True,
        style: Optional[str] = None,
        style_1: Optional[str] = None,
        style_2: Optional[str] = None,
    ) -> Markup:
        """Render a `stacked <https://fontawesome.com/v6/docs/web/style/stack>`_ icon.

        Some examples:
            >>> font_awesome.render_stacked_icon(
            ...     "fa-solid fa-square",
            ...     "fab fa-twitter",
            ...     inverse=True,
            ...     size="2x",
            ... )
            >>> font_awesome.render_stacked_icon(
            ...     "fa-solid fa-camera",
            ...     "fa-solid fa-ban",
            ...     stack_size_1="1x",
            ...     stack_size_2="2x",
            ...     size="2x",
            ...     style_2="color:Tomato",
            ... )

        Args:
            name_1 (str): The name of the first icon (e.g. `fa-solid fa-square`).
            name_2 (str): The name of the second icon (e.g. `fab fa-twitter`).
            stack_size_1 (str): The relative size of the first icon. One of `1x` or `2x`. Defaults to `2x`.
            stack_size_2 (str): The relative size of the second icon. One of `1x` or `2x`. Defaults to `1x`.
            inverse (bool): Inverts the color of the icon to white. Defaults to `False`.
            size (Optional[str]): The `relative or literal size <https://fontawesome.com/v6/docs/web/style/size>`_ of the stacked icon. Defaults to `None`.
            aria_hidden (bool): Add the `aria-hidden` attribute to the icon. Defaults to `True`.
            style (Optional[str]): Customize the stacked icon even further using `CSS styling <https://fontawesome.com/v6/docs/web/style/custom>`_. Defaults to `None`.
            style_1 (Optional[str]): Customize the first icon even further using `CSS styling <https://fontawesome.com/v6/docs/web/style/custom>`_. Defaults to `None`.
            style_2 (Optional[str]): Customize the second icon even further using `CSS styling <https://fontawesome.com/v6/docs/web/style/custom>`_. Defaults to `None`.

        Returns:
            flask.Markup: The HTML markup for the icon.
        """
        span = '<span class="fa-stack'
        if size is not None:
            span += f" fa-{_remove_prefix(size, 'fa-')}"
        span += '"'
        if style is not None:
            span += f' style="{style}"'
        if aria_hidden:
            span += ' aria-hidden="true"'
        span += ">"
        span += f"\n    {self.render_icon(name_1, inverse if stack_size_1 == '1x' else False, aria_hidden=False, style=style_1, _stack_size=stack_size_1)}"
        span += f"\n    {self.render_icon(name_2, inverse if stack_size_2 == '1x' else False, aria_hidden=False, style=style_2, _stack_size=stack_size_2)}"
        span += "\n</span>"
        return Markup(span)
