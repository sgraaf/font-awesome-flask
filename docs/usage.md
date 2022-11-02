# Usage

## Initialization

```{include} ../README.md
:start-after: <!-- start docs-include-initialization -->
:end-before: <!-- end docs-include-initialization -->
```

## Configuration

## Loading Resources

Font-Awesome-Flask provides three helper methods to load Font Awesome's resources: {func}`load() <flask_font_awesome.FontAwesome.load>`, {func}`load_js() <flask_font_awesome.FontAwesome.load_js>` and {func}`load_css() <flask_font_awesome.FontAwesome.load_css>`.

Font Awesome can be used either via [Web Fonts + CSS or via SVG + JS](https://fontawesome.com/docs/web/dig-deeper/webfont-vs-svg). Use the {func}`load_css() <flask_font_awesome.FontAwesome.load_css>` method for the former, and {func}`load_js() <flask_font_awesome.FontAwesome.load_js>` for the latter. You can also use the more general {func}`load() <flask_font_awesome.FontAwesome.load>` to load either, but which defaults to `SVG + JS`.

Whichever resource(s) you end up using, you can load them by simply including any of the `load()` methods in the head of your base template:

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
