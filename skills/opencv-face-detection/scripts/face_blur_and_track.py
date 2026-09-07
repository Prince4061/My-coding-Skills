"""Face Privacy Blurring and Pan-Tilt Tracking Vector Template

Demonstrates two high-demand real-world applications of face detection:
1. Dynamic Face Blurring (Privacy Mode): Automatically blurs all detected face regions.
2. Centroid Vector Tracking: Calculates offset (dx, dy) from the frame center for gimbal/servo/robotics control.

Hotkeys:
- 'b' : Toggle Face Blurring
- 't' : Toggle Tracking Vectors & Crosshairs
- 'd' : Toggle Bounding Box Drawing
- 'q' / ESC : Exit
"""

import argparse
import sys
import cv2
from cvzone.FaceDetectionModule import FaceDetector
import cvzone


def apply_face_blur(img, bbox, blur_strength=55):
    """Safely crop and apply Gaussian blur to the face bounding box."""
    h_img, w_img, _ = img.shape
    x, y, w, h = bbox

    # Clamp coordinates within frame boundaries
    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(w_img, x + w)
    y2 = min(h_img, y + h)

    if x2 > x1 and y2 > y1:
        face_roi = img[y1:y2, x1:x2]
        # Blur kernel size must be odd
        ksize = blur_strength if blur_strength % 2 == 1 else blur_strength + 1
        blurred = cv2.GaussianBlur(face_roi, (ksize, ksize), 30)
        img[y1:y2, x1:x2] = blurred
    return img


def draw_tracking_vectors(img, face_center, frame_center):
    """Draw crosshair and offset vector from frame center to target face."""
    fc_x, fc_y = frame_center
    t_x, t_y = face_center

    # Frame center crosshair
    cv2.drawMarker(img, (fc_x, fc_y), (255, 255, 255), cv2.MARKER_CROSS, 20, 2)

    # Line connecting frame center to target face
    cv2.line(img, (fc_x, fc_y), (t_x, t_y), (0, 255, 255), 2)

    # Target face crosshair
    cv2.circle(img, (t_x, t_y), 6, (0, 0, 255), cv2.FILLED)

    # Offset calculations
    dx = t_x - fc_x
    dy = t_y - fc_y

    cv2.putText(
        img,
        f"Offset: dX={dx:+04d}, dY={dy:+04d}",
        (t_x + 10, t_y - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 255, 255),
        1,
        cv2.LINE_AA,
    )
    return dx, dy


def main():
    parser = argparse.ArgumentParser(description="Face Blurring & Tracking Demo")
    parser.add_argument("--cam", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--blur-ksize", type=int, default=55, help="Blur kernel size (odd int)")
    args = parser.parse_args()

    cap = cv2.VideoCapture(args.cam)
    if not cap.isOpened():
        print(f"Error: Could not open camera {args.cam}.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detector = FaceDetector(minDetectionCon=0.6, modelSelection=0)
    fps_reader = cvzone.FPS()

    # Feature Toggles
    enable_blur = False
    enable_tracking = True
    enable_draw = True

    print("\n" + "=" * 55)
    print("  Face Blurring & Tracking Template Active")
    print("  ----------------------------------------")
    print("  [B] : Toggle Privacy Face Blur")
    print("  [T] : Toggle Centroid Tracking Vectors")
    print("  [D] : Toggle Detector BBox Drawing")
    print("  [Q] : Quit")
    print("=" * 55 + "\n")

    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)
        h_img, w_img, _ = img.shape
        frame_center = (w_img // 2, h_img // 2)

        # Detect faces (draw argument toggles cvzone default drawing)
        img, bboxs = detector.findFaces(img, draw=enable_draw and not enable_blur)

        if bboxs:
            # 1. Apply Blurring if enabled
            if enable_blur:
                for face in bboxs:
                    img = apply_face_blur(img, face["bbox"], blur_strength=args.blur_ksize)

            # 2. Tracking vectors for primary (first) face
            if enable_tracking:
                primary_face = bboxs[0]
                dx, dy = draw_tracking_vectors(img, primary_face["center"], frame_center)

        # HUD / Status display
        fps, img = fps_reader.update(img, pos=(20, 35), color=(0, 255, 0), scale=1.5, thickness=2)
        status_text = (
            f"Blur: {'ON' if enable_blur else 'OFF'} (B) | "
            f"Track: {'ON' if enable_tracking else 'OFF'} (T) | "
            f"Draw: {'ON' if enable_draw else 'OFF'} (D)"
        )
        cv2.putText(
            img,
            status_text,
            (20, h_img - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )

        cv2.imshow("Face Blur & Tracking Demo", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
        elif key == ord('b') or key == ord('B'):
            enable_blur = not enable_blur
            print(f">> Face Blurring: {'ENABLED' if enable_blur else 'DISABLED'}")
        elif key == ord('t') or key == ord('T'):
            enable_tracking = not enable_tracking
            print(f">> Tracking Vectors: {'ENABLED' if enable_tracking else 'DISABLED'}")
        elif key == ord('d') or key == ord('D'):
            enable_draw = not enable_draw
            print(f">> BBox Drawing: {'ENABLED' if enable_draw else 'DISABLED'}")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
