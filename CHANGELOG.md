# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.1.0] - Unreleased

### Added
- `py.typed` marker; the package passes `mypy --strict`.
- Tests for validation, unbounded axes, image borders and float coordinates.
- `LICENSE` (MIT), `CITATION.cff`, CI test workflow.

### Fixed
- `resize()` no longer moves `x1`/`y1` of an unbounded (`None`) axis.
- README example used a wrong import and a non-existent method.

### Changed
- Packaging moved from `setup.py` to `pyproject.toml`; author email is now isaacyong@naver.com.
- Removed the matplotlib demo from the module's `__main__` block.

## [1.0.1] - 2026-10-14

### Changed
- GitHub username renamed to NaNIsaac.

[1.1.0]: https://github.com/NaNIsaac/roi_rectangle/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/NaNIsaac/roi_rectangle/compare/v1.0.0...v1.0.1
