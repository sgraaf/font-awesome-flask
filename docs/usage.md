# Usage

## Configuration

Font-Awesome-Flask can be configured via the [Flask configuration API](https://flask.palletsprojects.com/en/latest/config/), using the {attr}`config <flask.Flask.config>` attribute of the {class}`Flask <flask.Flask>` object. These are the available configuration values along with their description:

| Configuration value        | Default | Description                                                                                                                                                                                       |
| -------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `FONT_AWESOME_SERVE_LOCAL` | `False` | Whether to serve Font Awesome's resources locally or from the CDN. When set to `True`, the appropriate resource(s) will be downloaded from the CDN once, after which they will be served locally. |

## Initialization

```{include} ../README.md
:start-after: <!-- start docs-include-initialization -->
:end-before: <!-- end docs-include-initialization -->
```

## Loading Resources

Font-Awesome-Flask provides three helper methods to load Font Awesome's resources: {func}`load() <flask_font_awesome.FontAwesome.load>`, {func}`load_js() <flask_font_awesome.FontAwesome.load_js>` and {func}`load_css() <flask_font_awesome.FontAwesome.load_css>`.

Font Awesome can be used either via [Web Fonts + CSS or via SVG + JS](https://fontawesome.com/docs/web/dig-deeper/webfont-vs-svg). Use the {func}`load_css() <flask_font_awesome.FontAwesome.load_css>` method for the former, and {func}`load_js() <flask_font_awesome.FontAwesome.load_js>` for the latter. You can also use the more general {func}`load() <flask_font_awesome.FontAwesome.load>` to load either, but which defaults to `SVG + JS`.

Whichever resource(s) you end up using, you can load them by simply including any of the methods mentioned above in the head of your base template:

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

By default, this will load **all** icon styles of the **latest** available version in **minified** form from the CDN. You can change this default behaviour by specifying options such as `version` or `style`. Please refer to the [API Reference](api) for a complete list of all available options.

## Rendering Icons

Font-Awesome-Flask provides two methods to render icons: {func}`render_icon() <flask_font_awesome.FontAwesome.render_icon>` to render a single icon, and {func}`render_stacked_icon() <flask_font_awesome.FontAwesome.render_stacked_icon>` to render a stacked icon. You can simply include these in your [Jinja](https://jinja.palletsprojects.com/en/latest/) template like so:

```
{{ font_awesome.render_icon("fas fa-house") }}
{{ font_awesome.render_stacked_icon("fas fa-square", "fas fa-house") }}
```

Both methods offer an exhaustive set of options to customize their styling. See the [API Reference](api) for more details.
