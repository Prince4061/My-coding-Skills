"""Live Webcam & Image Face Detection CLI with cvzone (MediaPipe BlazeFace)

Features:
- Real-time face detection with bounding box and confidence score percentage.
- Centroid calculation and target crosshairs.
- Live FPS counter display.
- Works on live webcam feed or static images.
"""

import argparse
import sys
import time
import cv2
from cvzone.FaceDetectionModule import FaceDetector
import cvzone


def run_image_detection(image_path, min_con=0.5, model_selection=0):
    """Detect faces on a single image and display results."""
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Could not load image from '{image_path}'.")
        sys.exit(1)

    detector = FaceDetector(minDetectionCon=min_con, modelSelection=model_selection)
    img_processed, bboxs = detector.findFaces(img.copy(), draw=True)

    print(f"\nDetection Results for {image_path}:")
    print(f"Total Faces Detected: {len(bboxs)}")

    for idx, face in enumerate(bboxs, 1):
        bbox = face["bbox"]
        score = face["score"][0]
        center = face["center"]
        print(f"  Face #{idx}: Confidence={score}%, BBox={bbox}, Center={center}")

    # Add text banner
    cv2.putText(
        img_processed,
        f"Faces Detected: {len(bboxs)}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        (0, 255, 0),
        2,
    )

    cv2.imshow("Face Detection - Image", img_processed)
    print("\nPress any key to close the window...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def run_webcam_detection(cam_index=0, min_con=0.5, model_selection=0):
    """Run real-time webcam face detection loop."""
    cap = cv2.VideoCapture(cam_index)
    if not cap.isOpened():
        print(f"Error: Could not open camera with index {cam_index}.")
        sys.exit(1)

    # Set standard resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detector = FaceDetector(minDetectionCon=min_con, modelSelection=model_selection)
    fps_reader = cvzone.FPS()

    print("\n" + "=" * 55)
    print("  Real-time Face Detection Started (cvzone + MediaPipe)")
    print(f"  Camera Index : {cam_index}")
    print(f"  Confidence   : {min_con}")
    print(f"  Model Mode   : {'0 (Short-range <= 2m)' if model_selection == 0 else '1 (Full-range <= 5m)'}")
    print("  Controls     : Press 'q' or 'ESC' to exit")
    print("=" * 55 + "\n")

    while True:
        success, img = cap.read()
        if not success:
            print("Warning: Failed to grab frame from camera.")
            break

        # Flip horizontally for natural mirror feel
        img = cv2.flip(img, 1)

        # Detect faces (draws bounding box, corners, confidence automatically)
        img, bboxs = detector.findFaces(img, draw=True)

        # Calculate and draw FPS
        fps, img = fps_reader.update(img, pos=(20, 50), color=(0, 255, 0), scale=2, thickness=2)

        # Overlay face count and centroid markers
        if bboxs:
            for idx, face in enumerate(bboxs):
                cx, cy = face["center"]
                # Draw center target circle
                cv2.circle(img, (cx, cy), 5, (0, 0, 255), cv2.FILLED)

            cv2.putText(
                img,
                f"Faces: {len(bboxs)}",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 200, 0),
                2,
            )
        else:
            cv2.putText(
                img,
                "No Face Detected",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2,
            )

        cv2.imshow("Real-time Face Detection", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Camera released. Exited cleanly.")


def main():
    parser = argparse.ArgumentParser(
        description="Face Detection CLI using OpenCV and cvzone (MediaPipe BlazeFace)"
    )
    parser.add_argument("--image", type=str, default=None, help="Path to static image file")
    parser.add_argument("--cam", type=int, default=0, help="Webcam device index (default: 0)")
    parser.add_argument(
        "--min-con",
        type=float,
        default=0.5,
        help="Minimum detection confidence threshold between 0.0 and 1.0 (default: 0.5)",
    )
    parser.add_argument(
        "--model-selection",
        type=int,
        choices=[0, 1],
        default=0,
        help="0 for short-range (<2m), 1 for full-range (<5m) (default: 0)",
    )

    args = parser.parse_args()

    if args.image:
        run_image_detection(args.image, min_con=args.min_con, model_selection=args.model_selection)
    else:
        run_webcam_detection(cam_index=args.cam, min_con=args.min_con, model_selection=args.model_selection)


if __name__ == "__main__":
    main()
