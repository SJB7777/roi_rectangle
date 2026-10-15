from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np
import numpy.typing as npt


@dataclass()
class RoiRectangle:
    """
    A class representing a rectangle.

    Args:
        y1 (int): The y-coordinate of the top-left corner of the rectangle.
        y2 (int | None): The y-coordinate of the bottom-right corner of the rectangle.
            If it is None it mean infinit range.
        x1 (int): The x-coordinate of the top-left corner of the rectangle.
        x2 (int | None): The x-coordinate of the bottom-right corner of the rectangle.
            If it is None it mean infinit range.
        The cropping operation uses half-open intervals [x1, x2) and [y1, y2).
        This means the coordinates (x2, y2) are not included in the cropped region.
    """

    y1: int = field(init=True, repr=True)
    y2: Optional[int] = field(init=True, repr=True)
    x1: int = field(init=True, repr=True)
    x2: Optional[int] = field(init=True, repr=True)

    def __post_init__(self) -> None:
        if self.x2 is not None and self.x2 < self.x1:
            raise ValueError("x2 must be >= x1")
        if self.y2 is not None and self.y2 < self.y1:
            raise ValueError("y2 must be >= y1")

    @property
    def width(self) -> Optional[int]:
        return None if self.x2 is None else self.x2 - self.x1

    @property
    def height(self) -> Optional[int]:
        return None if self.y2 is None else self.y2 - self.y1

    @property
    def center(self) -> Optional[tuple[int, int]]:
        if self.x2 is None or self.y2 is None:
            return None
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    def move(self, dx: int, dy: int) -> RoiRectangle:
        """Move the ROI relative to its current position.
        """
        return RoiRectangle(
            self.y1 + dy,
            self.y2 + dy if self.y2 is not None else None,
            self.x1 + dx,
            self.x2 + dx if self.x2 is not None else None,
        )

    def recenter(self, new_center: tuple[int, int]) -> RoiRectangle:
        x_i, y_i = self.center if self.center else (
            self.x1 + (self.width or 0) // 2,
            self.y1 + (self.height or 0) // 2,
        )
        x_f, y_f = new_center
        dx, dy = x_f - x_i, y_f - y_i

        return RoiRectangle(
            y1=self.y1 + dy,
            y2=self.y2 + dy if self.y2 is not None else None,
            x1=self.x1 + dx,
            x2=self.x2 + dx if self.x2 is not None else None,
        )

    def resize(self, new_width: int, new_height: int) -> RoiRectangle:
        if self.center is None:
            if self.x2 is None and self.y2 is None:
                return self
            cx = self.x1 + (self.width or 0) // 2
            cy = self.y1 + (self.height or 0) // 2
        else:
            cx, cy = self.center

        half_w, half_h = new_width // 2, new_height // 2
        new_x1, new_y1 = cx - half_w, cy - half_h
        new_x2, new_y2 = cx + (new_width - half_w), cy + (new_height - half_h)

        # An unbounded (None) axis has no size to change: keep its start.
        return RoiRectangle(
            y1=new_y1 if self.y2 is not None else self.y1,
            y2=new_y2 if self.y2 is not None else None,
            x1=new_x1 if self.x2 is not None else self.x1,
            x2=new_x2 if self.x2 is not None else None,
        )


    def to_tuple(self) -> tuple[int, Optional[int], int, Optional[int]]:
        """
        Get the coordinates of the ROI.
        """
        return self.y1, self.y2, self.x1, self.x2

    @property
    def area(self) -> Optional[int]:
        """
        Get the area of the ROI.
        """
        if self.width is None or self.height is None:
            return None
        return self.width * self.height

    @property
    def shape(self) -> tuple[Optional[int], Optional[int]]:
        """
        get the shape of the ROI.
        """
        return (self.height, self.width)

    def get_slices(self) -> tuple[slice, slice]:
        """
        Get the slices for the ROI.

        Returns:
            tuple: Slices for the y and x axes, in that order.
        """
        return slice(self.y1, self.y2), slice(self.x1,  self.x2)

    def slice(self, image: npt.NDArray[Any]) -> npt.NDArray[Any]:
        """
        Slice the specified region from the last two axes of the image.

        Args:
            image (np.ndarray): Input image.

        Returns:
            np.ndarray: Sliced region of the image.
        """
        return image[..., self.y1 : self.y2, self.x1 : self.x2]

    @classmethod
    def from_tuple(cls, coords: tuple[int, Optional[int], int, Optional[int]]) -> RoiRectangle:
        """
        Create a RoiRectangle instance from a tuple of coordinates.
        The tuple should contain four integers: (y1, y2, x1, x2).   
        """
        y1, y2, x1, x2 = coords
        return cls(y1=y1, y2=y2, x1=x1, x2=x2)


RoiRectangle.__module__ = "roi_rectangle"

