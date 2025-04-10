from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import numpy.typing as npt


@dataclass()
class RoiRectangle:
    """
    A class representing a rectangle.

    Args:
        x1 (int): The x-coordinate of the top-left corner of the rectangle.
        y1 (int): The y-coordinate of the top-left corner of the rectangle.
        x2 (int): The x-coordinate of the bottom-right corner of the rectangle.
        y2 (int): The y-coordinate of the bottom-right corner of the rectangle.

        The cropping operation uses half-open intervals [x1, x2) and [y1, y2).
        This means the coordinates (x2, y2) are not included in the cropped region.
    """

    x1: int = field(init=True, repr=True)
    y1: int = field(init=True, repr=True)
    x2: Optional[int] = field(init=True, repr=True)
    y2: Optional[int] = field(init=True, repr=True)
    width: Optional[int] = field(init=False, repr=False)
    height: Optional[int] = field(init=False, repr=False)

    def __post_init__(self):

        self.width = self.x2 - self.x1 if self.x2 is not None else None
        self.height = self.y2 - self.y1 if self.y2 is not None else None

    @property
    def center(self) -> Optional[tuple[int, int]]:
        """
        Get the center coordinates of the ROI.
        """
        if self.x2 is None or self.y2 is None:
            return None
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    def move(self, dx: int, dy: int) -> RoiRectangle:
        """move the ROI relative to its current position.
        """
        return RoiRectangle(
            self.x1 + dx,
            self.y1 + dy,
            self.x2 + dx,
            self.y2 + dy
        )

    def move_to_center(self, new_center: tuple[int, int]) -> RoiRectangle:
        """
        Move the ROI to a new center position.

        Args:
            new_center (tuple): New center coordinates (x, y).
        """
        if self.x2 is None or self.y2 is None:
            return None
        
        x_f, y_f = new_center
        x_i, y_i = self.center
        dx, dy = x_f - x_i, y_f - y_i

        return RoiRectangle(self.x1 + dx, self.y1 + dy, self.x2 + dx, self.y2 + dy)

    def resize(self, new_width: int, new_height: int) -> RoiRectangle:
        """
        Resize the ROI to a new width and height.

        Args:
            new_width (int): New width of the ROI.
            new_height (int): New height of the ROI.
        """
        if self.x2 is None or self.y2 is None:
            return None

        cx, cy = self.center
        sub_dx, sub_dy = new_width // 2, new_height // 2
        plus_dx, plus_dy = new_width - sub_dx, new_height - sub_dy
        return RoiRectangle(cx - sub_dx, cy - sub_dy, cx + plus_dx, cy + plus_dy)

    def to_tuple(self) -> tuple[Optional[int], Optional[int], Optional[int], Optional[int]]:
        """
        Get the coordinates of the ROI.
        """
        return self.x1, self.y1, self.x2, self.y2

    @property
    def area(self) -> Optional[int]:
        """
        Get the area of the ROI.
        """
        if self.x2 is None or self.y2 is None:
            return None

        return self.width * self.height

    @property
    def shape(self) -> Optional[tuple[int, int]]:
        """
        get the shape of the ROI.
        """
        return (self.height, self.width)

    def get_slices(self) -> tuple[slice, slice]:
        """
        Get the slices for the ROI.

        Returns:
            tuple: Slices for the x and y axes.
        """
        return ..., slice(self.y1, self.y2), slice(self.x1,  self.x2), 

    def slice(self, image: np.ndarray) -> npt.NDArray:
        """
        Slice the specified region from the image.

        Args:
            image (np.ndarray): Input image.

        Returns:
            np.ndarray: Sliced region of the image.
        """
        return image[..., self.y1 : self.y2, self.x1 : self.x2]

    def __repr__(self) -> str:
        """
        Represent the ROI as a string.
        """
        return f"RoiRectangle(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
    
    @classmethod
    def from_tuple(cls, coords: tuple[int, int, int, int]) -> 'RoiRectangle':
        """
        Create a RoiRectangle instance from a tuple of coordinates.
        The tuple should contain four integers: (x1, y1, x2, y2).   
        """
        x1, y1, x2, y2 = coords
        return cls(x1=x1, y1=y1, x2=x2, y2=y2)


if __name__ == "__main__":
    import matplotlib.pyplot as plt


    # 테스트용 이미지 생성
    test_image = np.random.random((100, 100))

    # RoiRectangle 인스턴스 생성
    roi = RoiRectangle(x1=20, y1=30, x2=70, y2=80)

    # ROI 정보 출력
    print("Initial ROI:")
    print(roi)

    # ROI 중심 좌표 출력
    print("Center Coordinate:", roi.center)

    # ROI 크기 출력
    print("Width:", roi.width)
    print("Height:", roi.height)

    # ROI 이동 테스트
    new_center = (50, 50)
    
    print("\nAfter Moving to Center:")
    print(roi.move_to_center(new_center))

    # ROI 크기 조절 테스트
    new_width, new_height = 30, 40
    
    print("\nAfter Resizing:")
    print(roi.resize(new_width, new_height))

    # ROI 영역 슬라이싱 테스트
    roi_slice = roi.slice(test_image)
    print("\nROI Slice:")
    print(roi_slice)

    # 원본 이미지 시각화
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(test_image, cmap='gray')

    # ROI 슬라이싱
    roi_slice = roi.slice(test_image)

    # 슬라이싱한 이미지 시각화
    plt.subplot(1, 2, 2)
    plt.title('ROI Slice')
    plt.imshow(roi_slice, cmap='gray')

    # ROI 영역 표시
    plt.gca().add_patch(plt.Rectangle(
        (roi.x1, roi.y1),
        roi.width,
        roi.height,
        linewidth=2,
        edgecolor='r',
        facecolor='none'
    ))
    plt.show()
