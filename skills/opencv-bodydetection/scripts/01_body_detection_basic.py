"""
01_body_detection_basic.py
--------------------------
Standard 6-step Real-time Human Body / Pose Detection using OpenCV and CVZone.
Detects full body posture, draws 33 skeletal landmarks, and tracks centroid.

Controls:
  'q' - Quit application
  'd' - Toggle landmark drawing ON / OFF
"""

import time
import cv2
from cvzone.PoseModule import PoseDetector

def main():
    # 1. Webcam initialize karna
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # 2. Pose Detector object banana (detectionCon=0.5, trackCon=0.5)
    detector = PoseDetector(
        staticMode=False,
        modelComplexity=1,
        smoothLandmarks=True,
        enableSegmentation=False,
        smoothSegmentation=True,
        detectionCon=0.5,
        trackCon=0.5,
    )

    draw_skeleton = True
    p_time = 0

    print("[INFO] Starting Body Detection...")
    print("[INFO] Press 'q' to Quit | Press 'd' to toggle Drawing")

    while True:
        success, img = cap.read()
        if not success:
            print("[WARN] Camera frame read nahi ho paya!")
            break

        # 3. Body detect karna aur landmarks/skeleton draw karna
        img = detector.findPose(img, draw=draw_skeleton)

        # 4. Landmark list aur bounding box data extract karna
        # lmList: [[id, x, y, z], ...] (33 landmarks)
        # bboxInfo: {"bbox": (x, y, w, h), "center": (cx, cy)}
        lmList, bboxInfo = detector.findPosition(img, draw=draw_skeleton, bboxWithHands=False)

        # 5. Agar body detect hui hai
        if bboxInfo:
            # Body ka center point access karna
            center = bboxInfo["center"]
            x, y, w, h = bboxInfo["bbox"]

            # Draw center point on screen
            cv2.circle(img, center, 8, (0, 0, 255), cv2.FILLED)
            cv2.putText(
                img,
                f"Body Center: ({center[0]}, {center[1]})",
                (center[0] + 15, center[1]),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 255),
                2,
            )

            # Sample landmark: Landmark 0 is Nose tip
            if lmList and len(lmList) > 0:
                nose = lmList[0]  # [id, x, y, z] or [x, y, z]
                # Safely extract coordinates
                if len(nose) == 4:
                    _, nx, ny, _ = nose
                else:
                    nx, ny = nose[0], nose[1]
                cv2.circle(img, (int(nx), int(ny)), 6, (255, 0, 0), cv2.FILLED)

        # 6. FPS Counter calculate & overlay karna
        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time

        # Status HUD overlay
        cv2.rectangle(img, (20, 20), (320, 90), (0, 0, 0), cv2.FILLED)
        cv2.putText(
            img,
            f"FPS: {int(fps)}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
        )
        status_text = "Detected" if bboxInfo else "No Body"
        status_color = (0, 255, 0) if bboxInfo else (0, 0, 255)
        cv2.putText(
            img,
            f"Status: {status_text}",
            (30, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            status_color,
            2,
        )

        # 7. Output display karna
        cv2.imshow("CVZone Body Detection", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("d"):
            draw_skeleton = not draw_skeleton
            print(f"[INFO] Draw skeleton: {draw_skeleton}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
