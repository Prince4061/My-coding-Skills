"""Finger Distance & Pinch Gesture with OpenCV + CVZone

Measures real-time distance between Thumb Tip (point 4) and Index Tip (point 8).
Foundation project for Pinch-to-Zoom, Virtual Mouse Clicks, and Volume Control!
"""

import cv2
from cvzone.HandTrackingModule import HandDetector

# 1. Camera start karo
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# 2. Hand detector initialize karo
detector = HandDetector(maxHands=1, detectionCon=0.8)

print("Starting Finger Distance Tracker... Press 'q' to exit.")

# 3. Main video loop
while True:
    # 4. Frame read karo
    success, img = cap.read()
    if not success:
        break

    # 5. Hand detect karo
    hands, img = detector.findHands(img)

    # 6. Agar haath detect ho, thumb aur index tip ke beech distance nikalo
    if hands:
        hand1 = hands[0]
        lmList = hand1["lmList"]

        # Point 4 = Thumb Tip, Point 8 = Index Tip
        point4 = lmList[4][0:2]  # (x, y)
        point8 = lmList[8][0:2]  # (x, y)

        # findDistance() line draw karta hai aur length (distance in pixels) deta hai
        length, info, img = detector.findDistance(point4, point8, img)

        # Pinch detection check (agar dono ungliyan paas hain)
        status = "PINCH!" if length < 35 else "OPEN"
        color = (0, 0, 255) if length < 35 else (0, 255, 0)

        # Screen par distance aur status show karo
        cv2.putText(
            img,
            f"Dist: {int(length)} px",
            (20, 50),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            (255, 255, 0),
            2,
        )
        cv2.putText(
            img,
            f"Gesture: {status}",
            (20, 90),
            cv2.FONT_HERSHEY_PLAIN,
            2,
            color,
            2,
        )

    # 7. Screen par display karo
    cv2.imshow("Finger Distance & Pinch - CVZone", img)

    # 8. 'q' key dabakar exit karo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("Finger Distance program closed.")
