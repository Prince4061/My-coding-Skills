"""
02_exercise_rep_counter.py
--------------------------
Fitness Workout Rep Counter (Bicep Curl / Squat) using OpenCV and CVZone PoseDetector.
Calculates joint angles, maps them to a progress percentage bar, and increments reps.

Controls:
  'q' - Quit application
  'r' - Reset rep counter to 0
  'm' - Switch mode (Bicep Curl <-> Squats)
"""

import argparse
import time
import numpy as np
import cv2
from cvzone.PoseModule import PoseDetector

def main():
    parser = argparse.ArgumentParser(description="CVZone Pose Workout Rep Counter")
    parser.add_argument("--video", type=str, default=None, help="Path to video file (default: webcam 0)")
    args = parser.parse_args()

    video_source = args.video if args.video else 0
    cap = cv2.VideoCapture(video_source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    detector = PoseDetector(detectionCon=0.7, trackCon=0.7)

    # Counter states
    rep_count = 0
    direction = 0  # 0 = moving down/extending, 1 = moving up/curling
    current_mode = "CURL"  # "CURL" or "SQUAT"
    p_time = 0

    print("[INFO] Workout Rep Counter started.")
    print("[INFO] 'q': Quit | 'r': Reset Reps | 'm': Switch Mode (CURL / SQUAT)")

    while True:
        success, img = cap.read()
        if not success:
            if args.video:
                # Loop video for replay
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            break

        # 1. Pose detect karo
        img = detector.findPose(img, draw=False)
        lmList, bboxInfo = detector.findPosition(img, draw=False)

        percentage = 0
        bar_height = 400

        if lmList and len(lmList) >= 28:
            if current_mode == "CURL":
                # Right Arm: Shoulder (12), Elbow (14), Wrist (16)
                p1 = lmList[12][:2]
                p2 = lmList[14][:2]
                p3 = lmList[16][:2]

                angle, img = detector.findAngle(p1, p2, p3, img=img, color=(255, 0, 0), scale=7)

                # Normalize angle to interior angle (0-180)
                if angle > 180:
                    angle = 360 - angle

                # Bicep curl range: ~30 deg (curled) to ~160 deg (extended)
                percentage = np.interp(angle, (40, 160), (100, 0))
                bar_height = np.interp(angle, (40, 160), (150, 450))

                # Check Repetition Logic
                # Color feedback: green when rep valid
                if percentage >= 95:
                    if direction == 0:
                        rep_count += 0.5
                        direction = 1
                if percentage <= 10:
                    if direction == 1:
                        rep_count += 0.5
                        direction = 0

            elif current_mode == "SQUAT":
                # Right Leg: Hip (24), Knee (26), Ankle (28)
                p1 = lmList[24][:2]
                p2 = lmList[26][:2]
                p3 = lmList[28][:2]

                angle, img = detector.findAngle(p1, p2, p3, img=img, color=(0, 255, 255), scale=7)

                if angle > 180:
                    angle = 360 - angle

                # Squat range: ~70 deg (deep squat) to ~170 deg (standing straight)
                percentage = np.interp(angle, (70, 165), (100, 0))
                bar_height = np.interp(angle, (70, 165), (150, 450))

                if percentage >= 90:
                    if direction == 0:
                        rep_count += 0.5
                        direction = 1
                if percentage <= 15:
                    if direction == 1:
                        rep_count += 0.5
                        direction = 0

        # UI Visuals: Progress Bar
        bar_color = (0, 255, 0) if percentage > 90 else (0, 165, 255)
        cv2.rectangle(img, (50, 150), (85, 450), (200, 200, 200), 3)
        cv2.rectangle(img, (50, int(bar_height)), (85, 450), bar_color, cv2.FILLED)
        cv2.putText(
            img,
            f"{int(percentage)}%",
            (40, 490),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            bar_color,
            2,
        )

        # Rep Counter Card
        cv2.rectangle(img, (20, 20), (320, 120), (0, 0, 0), cv2.FILLED)
        cv2.putText(
            img,
            f"Mode: {current_mode}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2,
        )
        cv2.putText(
            img,
            f"Reps: {int(rep_count)}",
            (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.4,
            (0, 255, 0),
            3,
        )

        # FPS
        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time
        cv2.putText(
            img,
            f"FPS: {int(fps)}",
            (img.shape[1] - 120, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

        cv2.imshow("Pose Workout Rep Counter", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        elif key == ord("r"):
            rep_count = 0
            print("[INFO] Reps reset to 0.")
        elif key == ord("m"):
            current_mode = "SQUAT" if current_mode == "CURL" else "CURL"
            rep_count = 0
            direction = 0
            print(f"[INFO] Mode switched to: {current_mode}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
