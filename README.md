# roi_rectangle

A small, typed helper for rectangular regions of interest (ROI) in NumPy images.

[![PyPI version](https://img.shields.io/pypi/v/roi-rectangle)](https://pypi.org/project/roi-rectangle/)
[![Python versions](https://img.shields.io/pypi/pyversions/roi-rectangle)](https://pypi.org/project/roi-rectangle/)
[![Tests](https://github.com/NaNIsaac/roi_rectangle/actions/workflows/tests.yml/badge.svg)](https://github.com/NaNIsaac/roi_rectangle/actions/workflows/tests.yml)
[![License](https://img.shields.io/pypi/l/roi-rectangle)](https://github.com/NaNIsaac/roi_rectangle/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/roi-rectangle)](https://pepy.tech/project/roi-rectangle)

## Install

```sh
pip install roi-rectangle
```

## Quickstart

```python
import numpy as np
from roi_rectangle import RoiRectangle

image = np.arange(100 * 120).reshape(100, 120)

roi = RoiRectangle(y1=30, y2=80, x1=20, x2=70)  # rows [30, 80), cols [20, 70)
print(roi.shape, roi.center, roi.area)          # (50, 50) (45, 55) 2500

crop = roi.slice(image)                         # same as image[30:80, 20:70]
print(crop.shape)                               # (50, 50)

roi2 = roi.recenter((60, 40)).resize(10, 20)    # methods return new ROIs
print(roi2)                                     # RoiRectangle(y1=30, y2=50, x1=55, x2=65)
print(image[roi2.get_slices()].shape)           # (20, 10)
```

## API overview

`RoiRectangle(y1, y2, x1, x2)` is a dataclass. Intervals are half-open: `[y1, y2)` and `[x1, x2)`.
`y2` or `x2` may be `None`, meaning the region extends to the image edge on that axis.
A `ValueError` is raised if `y2 < y1` or `x2 < x1`.

| Member | Description |
| --- | --- |
| `width`, `height`, `shape`, `area` | Size properties (`shape` is `(height, width)`); `None` for unbounded axes. |
| `center` | `(x, y)` center, rounded down; `None` if any axis is unbounded. |
| `move(dx, dy)` | New ROI shifted by `(dx, dy)`. |
| `recenter((x, y))` | New ROI of the same size centered at `(x, y)`. |
| `resize(width, height)` | New ROI with the given size around the same center. |
| `slice(image)` | `image[..., y1:y2, x1:x2]`; works on stacks with leading axes. |
| `get_slices()` | `(slice(y1, y2), slice(x1, x2))` for indexing. |
| `to_tuple()`, `from_tuple(t)` | Convert to/from `(y1, y2, x1, x2)`. |

Coordinates are passed to NumPy unchanged: an ROI past the bottom or right edge is clipped by NumPy,
while negative coordinates count from the end of the axis.

## Citation

If you use this package in your work, please cite it using the metadata in
[CITATION.cff](https://github.com/NaNIsaac/roi_rectangle/blob/main/CITATION.cff).

## License

MIT. See [LICENSE](https://github.com/NaNIsaac/roi_rectangle/blob/main/LICENSE).
