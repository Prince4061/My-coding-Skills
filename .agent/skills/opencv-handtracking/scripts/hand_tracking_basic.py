"""Basic Hand Tracking with OpenCV + CVZone (MediaPipe)

Beginner-friendly script for Class 8-9 students.
Detects up to 2 hands, 21 landmark points, left/right hand type, and bounding box.
"""

import cv2
from cvzone.HandTrackingModule import HandDetector

# 1. Camera start karo (0 = default webcam)
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Camera width
cap.set(4, 480)  # Camera height

# 2. Hand Detector initialize karo (80% confidence, max 2 hands)
detector = HandDetector(maxHands=2, detectionCon=0.8)

print("Starting Hand Tracking... Press 'q' to exit.")

# 3. Main video loop
while True:
    # 4. Camera se frame read karo
    success, img = cap.read()
    if not success:
        print("Camera nahi chal raha hai!")
        break

    # 5. Hands detect karo aur skeleton draw karo
    hands, img = detector.findHands(img)

    # 6. Agar koi haath mila toh data nikalo
    if hands:
        # Pehla haath
        hand1 = hands[0]
        lmList = hand1["lmList"]       # 21 Landmark points (x, y, z)
        bbox = hand1["bbox"]           # Bounding box (x, y, w, h)
        center = hand1["center"]       # Palm center (cx, cy)
        handType = hand1["type"]       # "Left" ya "Right"

        # Terminal par print karo (har 30 frames ya live)
        # print(f"Detected {handType} Hand at Center: {center}")

        # Dusra haath (agar dono haath camera ke samne ho)
        if len(hands) == 2:
            hand2 = hands[1]
            handType2 = hand2["type"]
            # Dono haath ke center ke beech ki line aur distance
            length, info, img = detector.findDistance(hand1["center"], hand2["center"], img)

    # 7. Screen par display karo
    cv2.imshow("Hand Tracking - CVZone", img)

    # 8. 'q' dabane par program band karo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("Hand Tracking program closed.")
