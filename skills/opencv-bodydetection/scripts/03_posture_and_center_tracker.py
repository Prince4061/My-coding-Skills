"""
03_posture_and_center_tracker.py
--------------------------------
Real-time Body Centroid, Posture Slouch/Lean Angle, and Distance Tracker using OpenCV and CVZone.
Analyzes spinal posture, horizontal position, and camera distance in real-time.

Controls:
  'q' - Quit application
  'c' - Calibrate neutral posture reference
"""

import math
import time
import cv2
from cvzone.PoseModule import PoseDetector

def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    detector = PoseDetector(detectionCon=0.6, trackCon=0.6)

    calibrated_lean = 0.0
    p_time = 0

    print("[INFO] Posture & Center Tracker started.")
    print("[INFO] Press 'c' to Calibrate upright posture | 'q' to Quit")

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.findPose(img, draw=True)
        lmList, bboxInfo = detector.findPosition(img, draw=True, bboxWithHands=False)

        h_img, w_img, _ = img.shape
        posture_status = "Waiting for body..."
        status_color = (150, 150, 150)

        if bboxInfo and len(lmList) >= 25:
            cx, cy = bboxInfo["center"]
            x, y, w, h = bboxInfo["bbox"]

            # Shoulder points: 11 (Left), 12 (Right)
            # Hip points: 23 (Left), 24 (Right)
            s_left, s_right = lmList[11][:2], lmList[12][:2]
            h_left, h_right = lmList[23][:2], lmList[24][:2]

            # Midpoints
            mid_shoulder = ((s_left[0] + s_right[0]) // 2, (s_left[1] + s_right[1]) // 2)
            mid_hip = ((h_left[0] + h_right[0]) // 2, (h_left[1] + h_right[1]) // 2)

            # Draw spine line
            cv2.line(img, mid_shoulder, mid_hip, (0, 255, 255), 3)
            cv2.circle(img, mid_shoulder, 6, (0, 255, 0), -1)
            cv2.circle(img, mid_hip, 6, (255, 0, 0), -1)

            # Shoulder width in pixels (proxy for distance from camera)
            shoulder_dist = math.hypot(s_right[0] - s_left[0], s_right[1] - s_left[1])

            # Spine lean angle (degrees from vertical)
            dx = mid_shoulder[0] - mid_hip[0]
            dy = mid_hip[1] - mid_shoulder[1]  # positive when shoulder is above hip
            lean_angle = math.degrees(math.atan2(dx, dy)) - calibrated_lean

            # Posture check
            if abs(lean_angle) < 8:
                posture_status = "Good Posture (Upright)"
                status_color = (0, 255, 0)
            elif lean_angle >= 8:
                posture_status = f"Leaning Right ({int(lean_angle)} deg)"
                status_color = (0, 0, 255)
            else:
                posture_status = f"Leaning Left ({int(abs(lean_angle))} deg)"
                status_color = (0, 0, 255)

            # Horizontal quadrant
            if cx < w_img * 0.35:
                pos_x = "Left Side"
            elif cx > w_img * 0.65:
                pos_x = "Right Side"
            else:
                pos_x = "Centered"

            # Overlay info card
            cv2.rectangle(img, (20, 20), (380, 160), (0, 0, 0), cv2.FILLED)
            cv2.putText(img, f"Posture: {posture_status}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)
            cv2.putText(img, f"Spine Lean: {lean_angle:+.1f} deg", (30, 85),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(img, f"Position: {pos_x} ({cx}, {cy})", (30, 115),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            cv2.putText(img, f"Shoulder Width: {int(shoulder_dist)}px", (30, 145),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        # FPS calculation
        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time
        cv2.putText(img, f"FPS: {int(fps)}", (w_img - 130, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        cv2.imshow("Posture & Center Tracker", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("c"):
            if bboxInfo and len(lmList) >= 25:
                dx = mid_shoulder[0] - mid_hip[0]
                dy = mid_hip[1] - mid_shoulder[1]
                calibrated_lean = math.degrees(math.atan2(dx, dy))
                print(f"[INFO] Calibrated neutral lean offset to: {calibrated_lean:.1f} deg")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
