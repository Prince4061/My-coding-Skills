# Pure OpenCV Color Detection & HSV Thresholding (Fallback Guide)

Ye guide explain karta hai ki bina kisi third-party helper library (cvzone) ke, pure OpenCV (cv2) aur NumPy ke through color detection, HSV masking, aur tracking kaise karein.

---

## 1. HSV Color Space kyun zaroori hai?

- **BGR / RGB:** Light ki brightness change hone par Red, Green, Blue teeno values drastic change ho jaati hain.
- **HSV (Hue, Saturation, Value):**
  - **Hue (H):** 0 se 179 tak color identity define karta hai (Red, Green, Blue etc.). Lighting change hone par bhi Hue stable rehta hai.
  - **Saturation (S):** 0 se 255 tak color ki depth/intensity.
  - **Value (V):** 0 se 255 tak brightness.

---

## 2. Standard HSV Ranges in OpenCV

OpenCV mein Hue ki range 0-179 hoti hai (8-bit representation ke liye 360 / 2 = 180):

| Color | Hue Range (H_min - H_max) | Saturation Range | Value Range |
|---|---|---|---|
| Red (Lower) | 0 - 10 | 100 - 255 | 100 - 255 |
| Red (Upper / Wrap) | 170 - 180 | 100 - 255 | 100 - 255 |
| Orange / Ball | 10 - 25 | 100 - 255 | 100 - 255 |
| Yellow | 20 - 35 | 100 - 255 | 100 - 255 |
| Green | 36 - 85 | 70 - 255 | 70 - 255 |
| Cyan / Sky Blue | 86 - 100 | 100 - 255 | 100 - 255 |
| Blue | 100 - 130 | 100 - 255 | 100 - 255 |
| Purple / Violet | 130 - 160 | 100 - 255 | 100 - 255 |

> **Note on Red Color:** Red color circular Hue spectrum ke dono ends (0 aur 180) par lie karta hai. Isliye pure Red ke liye do masks banakar cv2.bitwise_or(mask1, mask2) karna padta hai.

---

## 3. Pure OpenCV Implementation (No cvzone required)

```python
import cv2
import numpy as np

# 1. Capture/Read image
cap = cv2.VideoCapture(0)

# 2. Define HSV bounds (Example for Yellow/Orange)
lower_bound = np.array([20, 100, 100], dtype=np.uint8)
upper_bound = np.array([35, 255, 255], dtype=np.uint8)

while True:
    success, frame = cap.read()
    if not success:
        break

    # Step A: BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Step B: Create Mask with inRange
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Step C: Morphological operations (Noise reduction)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    # Step D: Bitwise AND to isolate color
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # Step E: Find Contours for Tracking
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:  # Noise threshold
            x, y, w, h = cv2.boundingRect(cnt)
            cx, cy = x + w // 2, y + h // 2

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv2.putText(frame, f'Center: ({cx},{cy})', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow('Original + Tracked', frame)
    cv2.imshow('Mask', mask)
    cv2.imshow('Isolated Color', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

---

## 4. Multi-Color Tracking

Agar ek sath Multiple colors track karne hain (e.g. Red marker + Blue marker):

```python
# Create masks for each color
mask_red1 = cv2.inRange(hsv, np.array([0, 100, 100]), np.array([10, 255, 255]))
mask_red2 = cv2.inRange(hsv, np.array([170, 100, 100]), np.array([180, 255, 255]))
mask_red = cv2.bitwise_or(mask_red1, mask_red2)

mask_blue = cv2.inRange(hsv, np.array([100, 100, 100]), np.array([130, 255, 255]))

# Find contours separately for each color
```
