from dataclasses import dataclass, field
import numpy as np

@dataclass()
class RoiRectangle:
    """
    A class representing a rectangle.

    Args:
        x1 (int): The x-coordinate of the top-left corner of the rectangle.
        y1 (int): The y-coordinate of the top-left corner of the rectangle.
        x2 (int): The x-coordinate of the bottom-right corner of the rectangle.
        y2 (int): The y-coordinate of the bottom-right corner of the rectangle.
    """

    x1: int = field(init=True, repr=True)
    y1: int = field(init=True, repr=True)
    x2: int = field(init=True, repr=True)
    y2: int = field(init=True, repr=True)
    width: int = field(init=False, repr=False)
    height: int = field(init=False, repr=False)

    def __post_init__(self):
        if self.x1 > self.x2:
            self.x1, self.x2 = self.x2, self.x1
        if self.y1 > self.y2:
            self.y1, self.y2 = self.y2, self.y1

        self.x1, self.y1, self.x2, self.y2 = map(int, [self.x1, self.y1, self.x2, self.y2])
        self.width = self.x2 - self.x1
        self.height = self.y2 - self.y1

    @property
    def center(self) -> tuple[int, int]:
        """
        Get the center coordinates of the ROI.
        """
        return (self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2

    def move_to_center(self, new_center: tuple[int, int]):
        """
        Move the ROI to a new center position.

        Args:
            new_center (tuple): New center coordinates (x, y).
        """
        cx, cy = new_center
        dx, dy = self.width // 2, self.height // 2
        self.x1, self.y1, self.x2, self.y2 = cx - dx, cy - dy, cx + dx, cy + dy

    def resize(self, new_width: int, new_height: int):
        """
        Resize the ROI to a new width and height.

        Args:
            new_width (int): New width of the ROI.
            new_height (int): New height of the ROI.
        """
        cx, cy = self.center
        dx, dy = new_width // 2, new_height // 2
        self.x1, self.y1, self.x2, self.y2 = cx - dx, cy - dy, cx + dx, cy + dy
        self.width, self.height = new_width, new_height

    def get_coordinate(self) -> tuple[int, int, int, int]:
        """
        Get the coordinates of the ROI.
        """
        return self.x1, self.y1, self.x2, self.y2

    def get_area(self) -> int:
        """
        Get the area of the ROI.
        """
        return self.width * self.height

    def slice(self, image: np.ndarray) -> np.ndarray:
        """
        Slice the specified region from the image.

        Args:
            image (np.ndarray): Input image.

        Returns:
            np.ndarray: Sliced region of the image.
        """
        return image[..., self.y1 : self.y2 + 1, self.x1 : self.x2 + 1]

    def __repr__(self) -> str:
        """
        Represent the ROI as a string.
        """
        return f"RoiRectangle(x1={self.x1}, y1={self.y1}, x2={self.x2}, y2={self.y2})"
    
    
if __name__ == "__main__":
    import numpy as np
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
    roi.move_to_center(new_center)
    print("\nAfter Moving to Center:")
    print(roi)

    # ROI 크기 조절 테스트
    new_width, new_height = 30, 40
    roi.resize(new_width, new_height)
    print("\nAfter Resizing:")
    print(roi)

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
    plt.gca().add_patch(plt.Rectangle((roi.x1, roi.y1), roi.width, roi.height, linewidth=2, edgecolor='r', facecolor='none'))
    plt.show()