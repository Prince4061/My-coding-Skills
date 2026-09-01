"""HSV Trackbar Color Finder Tool

Interactive trackbar utility to find and calibrate exact HSV min/max
thresholds for color detection and object tracking in real-time or from an image.
"""

import argparse
import sys
import cv2
from cvzone.ColorModule import ColorFinder
import cvzone


def main():
    parser = argparse.ArgumentParser(description=HSV Trackbar Color Detection Calibrator)
    parser.add_argument(--image, type=str, help=Path to input image file (optional, defaults to webcam))
    parser.add_argument(--cam, type=int, default=0, help=Camera index (default: 0))
    args = parser.parse_args()

    # Initialize ColorFinder with trackBar=True (Debug Mode)
    my_color_finder = ColorFinder(trackBar=True)

    # Initial default values (can be adjusted live via trackbars)
    hsv_vals = {'hmin': 0, 'smin': 0, 'vmin': 0, 'hmax': 179, 'smax': 255, 'vmax': 255}

    if args.image:
        img_static = cv2.imread(args.image)
        if img_static is None:
            print(fError: Could not load image at {args.image})
            sys.exit(1)
        print(fLoaded image '{args.image}'. Adjust sliders to isolate your target color.)
        print(Press 'q' or 'ESC' to exit and print final HSV values.)

        while True:
            img = img_static.copy()
            img_color, mask = my_color_finder.update(img, hsv_vals)
            img_stack = cvzone.stackImages([img, img_color, mask], cols=3, scale=0.6)
            cv2.imshow(HSV Calibrator - Image Mode, img_stack)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
    else:
        cap = cv2.VideoCapture(args.cam)
        if not cap.isOpened():
            print(fError: Could not open camera {args.cam}.)
            sys.exit(1)

        print(Webcam started. Adjust trackbars until target color is white in mask and isolated in color view.)
        print(Press 'q' or 'ESC' to exit.)

        while True:
            success, img = cap.read()
            if not success:
                print(Failed to capture frame from webcam.)
                break

            img_color, mask = my_color_finder.update(img, hsv_vals)
            img_stack = cvzone.stackImages([img, img_color, mask], cols=3, scale=0.6)
            cv2.imshow(HSV Calibrator - Webcam Mode, img_stack)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break

        cap.release()

    cv2.destroyAllWindows()
    print(\n + = * 50)
    print(Locked HSV Values:)
    print(fhsvVals = {hsv_vals})
    print(= * 50)


if __name__ == __main__:
    main()
