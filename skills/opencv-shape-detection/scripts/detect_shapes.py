"""OpenCV Shape Detection Pipeline

Detects geometric shapes (triangle, square, rectangle, pentagon, hexagon, circle)
using Grayscale -> Canny -> Dilation -> findContours -> Classification.
"""

import argparse
import sys
import cv2
import numpy as np


def classify_shape(corners_count: int, bbox: tuple) -> str:
    """Classifies shape based on corner count and aspect ratio."""
    if corners_count == 3:
        return "Triangle"
    elif corners_count == 4:
        _, _, w, h = bbox
        aspect_ratio = float(w) / float(h) if h != 0 else 0
        if 0.95 <= aspect_ratio <= 1.05:
            return "Square"
        return "Rectangle"
    elif corners_count == 5:
        return "Pentagon"
    elif corners_count == 6:
        return "Hexagon"
    elif corners_count >= 7:
        return "Circle"
    return f"Polygon ({corners_count} corners)"


def process_image(
    img: np.ndarray,
    min_area: int = 500,
    canny_thresh1: int = 50,
    canny_thresh2: int = 150,
    filter_corners: list = None,
):
    """Processes image and returns processed stack and detected shapes metadata."""
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (5, 5), 1)
    img_canny = cv2.Canny(img_blur, canny_thresh1, canny_thresh2)

    kernel = np.ones((5, 5), np.uint8)
    img_dilated = cv2.dilate(img_canny, kernel, iterations=1)

    img_contour = img.copy()

    # Find contours using OpenCV
    contours, hierarchy = cv2.findContours(
        img_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    detected_shapes = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > min_area:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            corners = len(approx)

            if filter_corners and corners not in filter_corners:
                continue

            x, y, w, h = cv2.boundingRect(approx)
            bbox = (x, y, w, h)
            shape_name = classify_shape(corners, bbox)

            # Draw contour and bounding box
            cv2.drawContours(img_contour, [approx], -1, (0, 255, 0), 2)
            cv2.rectangle(img_contour, (x, y), (x + w, y + h), (255, 0, 0), 2)

            # Center text
            cx, cy = x + w // 2, y + h // 2
            cv2.circle(img_contour, (cx, cy), 4, (0, 0, 255), -1)
            cv2.putText(
                img_contour,
                shape_name,
                (x, max(y - 10, 15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )

            detected_shapes.append(
                {
                    "shape": shape_name,
                    "corners": corners,
                    "area": area,
                    "center": (cx, cy),
                    "bbox": bbox,
                }
            )

    return img_contour, img_gray, img_canny, img_dilated, detected_shapes


def main():
    parser = argparse.ArgumentParser(description="OpenCV Shape Detection Tool")
    parser.add_argument("--image", type=str, help="Path to input image file")
    parser.add_argument("--webcam", action="store_true", help="Use webcam stream")
    parser.add_argument(
        "--min-area", type=int, default=500, help="Minimum contour area to filter noise"
    )
    parser.add_argument(
        "--filter",
        type=int,
        nargs="+",
        help="Filter specific corner counts (e.g. --filter 3 4)",
    )
    args = parser.parse_args()

    if args.webcam:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            sys.exit(1)
        print("Starting webcam... Press 'q' to quit.")
        while True:
            success, frame = cap.read()
            if not success:
                break
            result, _, _, _, _ = process_image(
                frame, min_area=args.min_area, filter_corners=args.filter
            )
            cv2.imshow("Live Shape Detection", result)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
    elif args.image:
        img = cv2.imread(args.image)
        if img is None:
            print(f"Error: Could not read image at {args.image}")
            sys.exit(1)
        result, gray, canny, dilated, detected = process_image(
            img, min_area=args.min_area, filter_corners=args.filter
        )
        print(f"Detected {len(detected)} shapes:")
        for idx, item in enumerate(detected, 1):
            print(f" {idx}. {item['shape']} (Corners: {item['corners']}, Area: {item['area']:.1f}, Center: {item['center']}, BBox: {item['bbox']})")
        cv2.imshow("Shape Detection Result", result)
        print("Press any key on image window to close.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Usage: python detect_shapes.py --image <path_to_image> OR python detect_shapes.py --webcam")


if __name__ == "__main__":
    main()
