"""Production Color Detection Template with cvzone

Robust template for color detection and optional object tracking / contour extraction.
Customize the 'PROJECT LOGIC' section for your specific application (drawing, games, sorting).
"""

import argparse
import sys
import cv2
from cvzone.ColorModule import ColorFinder
import cvzone


# =====================================================================
# CALIBRATED HSV VALUES (Replace with values discovered from find_color_trackbar.py)
# =====================================================================
# Preset examples:
# Orange / Ball: {'hmin': 5, 'smin': 100, 'vmin': 100, 'hmax': 25, 'smax': 255, 'vmax': 255}
# Yellow:        {'hmin': 20, 'smin': 100, 'vmin': 100, 'hmax': 35, 'smax': 255, 'vmax': 255}
# Green:         {'hmin': 40, 'smin': 80, 'vmin': 80, 'hmax': 85, 'smax': 255, 'vmax': 255}
# Blue:          {'hmin': 90, 'smin': 100, 'vmin': 100, 'hmax': 130, 'smax': 255, 'vmax': 255}

HSV_VALS = {
    'hmin': 20,
    'smin': 100,
    'vmin': 100,
    'hmax': 35,
    'smax': 255,
    'vmax': 255
}


def process_frame(img, color_finder, hsv_vals, min_area=500, track_contours=True):
    """Detect color, extract mask, and optionally find contours for tracking."""
    # 1. Update color finder mask
    img_color, mask = color_finder.update(img, hsv_vals)
    img_contours = img.copy()
    contours_info = []

    # 2. Track position with findContours if requested
    if track_contours:
        img_contours, contours = cvzone.findContours(img, mask, minArea=min_area)
        if contours:
            for cnt in contours:
                cx, cy = cnt['center']
                area = cnt['area']
                bbox = cnt['bbox']
                contours_info.append({'center': (cx, cy), 'area': area, 'bbox': bbox})

                # =========================================================
                # PROJECT LOGIC (Customize for your specific application)
                # =========================================================
                # Example: Draw visual crosshair / center indicator
                cv2.circle(img_contours, (cx, cy), 6, (0, 0, 255), cv2.FILLED)
                cv2.putText(
                    img_contours,
                    fPos: ({cx},{cy}) Area: {int(area)},
                    (bbox[0], max(bbox[1] - 10, 20)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2,
                )

    return img_color, mask, img_contours, contours_info


def main():
    parser = argparse.ArgumentParser(description=Color Detection & Object Tracking)
    parser.add_argument(--image, type=str, help=Path to input image file)
    parser.add_argument(--cam, type=int, default=0, help=Camera index (default: 0))
    parser.add_argument(--min-area, type=int, default=500, help=Min area for contour detection)
    args = parser.parse_args()

    # In production, trackBar=False ensures clean performance without debug UI
    color_finder = ColorFinder(trackBar=False)

    if args.image:
        img = cv2.imread(args.image)
        if img is None:
            print(fError: Could not load image at {args.image})
            sys.exit(1)

        img_color, mask, img_contours, contours_info = process_frame(
            img, color_finder, HSV_VALS, min_area=args.min_area
        )
        print(fDetected {len(contours_info)} color target(s):)
        for idx, info in enumerate(contours_info, 1):
            print(f {idx}. Center: {info['center']}, Area: {info['area']}, BBox: {info['bbox']})

        img_stack = cvzone.stackImages([img, img_color, mask, img_contours], cols=2, scale=0.6)
        cv2.imshow(Color Detection Result, img_stack)
        print(Press any key to exit.)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        cap = cv2.VideoCapture(args.cam)
        if not cap.isOpened():
            print(fError: Could not open camera {args.cam}.)
            sys.exit(1)

        print(Color tracking active. Press 'q' or 'ESC' to exit.)
        while True:
            success, img = cap.read()
            if not success:
                break

            img_color, mask, img_contours, contours_info = process_frame(
                img, color_finder, HSV_VALS, min_area=args.min_area
            )

            img_stack = cvzone.stackImages([img, img_color, mask, img_contours], cols=2, scale=0.5)
            cv2.imshow(Live Color Tracking, img_stack)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == __main__:
    main()
