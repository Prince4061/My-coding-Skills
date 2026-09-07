"""Live Finger Counter with OpenCV + CVZone

Counts how many fingers are held up (0 to 5) in real-time.
Designed for school students learning Computer Vision.
"""

import cv2
from cvzone.HandTrackingModule import HandDetector

# 1. Camera start karo
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# 2. Hand detector initialize karo (max 1 hand for clean counting)
detector = HandDetector(maxHands=1, detectionCon=0.8)

print("Starting Finger Counter... Show your hand to the camera! Press 'q' to exit.")

# 3. Main video loop
while True:
    # 4. Camera se frame read karo
    success, img = cap.read()
    if not success:
        break

    # 5. Hand detect karo
    hands, img = detector.findHands(img)

    # 6. Finger count calculate karo
    if hands:
        hand1 = hands[0]
        # fingersUp() list deta hai: [Thumb, Index, Middle, Ring, Pinky]
        # 1 matlab ungli khuli hai, 0 matlab band hai
        fingers = detector.fingersUp(hand1)
        totalFingers = fingers.count(1)

        # Output box screen par draw karo
        cv2.rectangle(img, (20, 20), (220, 110), (0, 200, 0), cv2.FILLED)
        cv2.putText(
            img,
            f"Fingers: {totalFingers}",
            (30, 80),
            cv2.FONT_HERSHEY_PLAIN,
            3,
            (255, 255, 255),
            3,
        )

    # 7. Screen par display karo
    cv2.imshow("Finger Counter - CVZone", img)

    # 8. 'q' se exit karo
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
print("Finger Counter closed.")
