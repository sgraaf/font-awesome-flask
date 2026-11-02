# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Calendar Versioning](https://calver.org/).

The **first number** of the version is the year.
The **second number** is incremented with each release, starting at 1 for each year.
The **last three numbers** are the version of the bundled Font Awesome library (e.g. `2026.1.7.3.1` bundles Font Awesome 7.3.1).

## [2026.1.7.3.1](https://github.com/sgraaf/font-awesome-flask/compare/v0.1.5...2026.1.7.3.1) - 2026-11-02

This release upgrades the bundled Font Awesome to version 7.3.1, a new major version, and fixes `import flask_font_awesome` failing in 0.1.5 because of missing data files. It also introduces a new versioning scheme that combines the release year and number with the bundled Font Awesome version. Upgrading may require changes to your code: most function arguments are now keyword-only, Python 3.11 or newer is required, `flask_font_awesome.__version__` has been removed, and the license is now GPL-3.0-only.

### Added

- `py.typed` marker, so type checkers use the package's type annotations

### Changed

- Combined the package version with the bundled Font Awesome version: versions are now `YYYY.N.FA_MAJOR.FA_MINOR.FA_PATCH` (e.g. `2026.1.7.3.1`)
- Upgraded Font Awesome to version 7.3.1, a new major version
- All arguments of `load()`, `load_css()` and `load_js()`, and all arguments after the icon name(s) of `render_icon()` and `render_stacked_icon()`, are now keyword-only
- Changed the license from GPL-3.0-or-later to GPL-3.0-only

### Removed

- `flask_font_awesome.__version__`; use `importlib.metadata.version("font-awesome-flask")` instead
- Support for Python 3.8, 3.9 and 3.10; Python 3.11 or newer is now required

### Fixed

- `load()` passing `version` and `style` to `load_css()` / `load_js()` in the wrong order
- `import flask_font_awesome` raising `FileNotFoundError` in 0.1.5, because the SRI hash data files it loads were not included in the package

## [0.1.5](https://github.com/sgraaf/font-awesome-flask/compare/v0.1.4...v0.1.5) - 2024-06-16

### Removed

- The `data/css_sris.json` and `data/js_sris.json` files, which are still loaded on import (see the fix under [2026.1.7.3.1])

## [0.1.4](https://github.com/sgraaf/font-awesome-flask/compare/v0.1.3...v0.1.4) - 2023-12-24

### Fixed

- Compatibility with Flask 3.0, which removed `flask.Markup`: `Markup` is now imported from `markupsafe` ([#6](https://github.com/sgraaf/font-awesome-flask/pull/6))

## [0.1.3](https://github.com/sgraaf/font-awesome-flask/compare/0.1.2...v0.1.3) - 2023-12-24

### Changed

- Upgraded Font Awesome to version 6.5.1

## [0.1.2](https://github.com/sgraaf/font-awesome-flask/compare/0.1.1...0.1.2) - 2023-09-05

### Changed

- Upgraded Font Awesome to version 6.4.2

### Removed

- Support for Python 3.7

## [0.1.1](https://github.com/sgraaf/font-awesome-flask/compare/0.1.0...0.1.1) - 2022-11-05

### Added

- [Documentation](https://font-awesome-flask.readthedocs.io/en/stable/)

## [0.1.0] - 2022-10-27

### Added

- Initial release of `Font-Awesome-Flask`
