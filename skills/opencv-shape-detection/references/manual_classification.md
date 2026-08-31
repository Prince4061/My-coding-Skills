# Pure OpenCV Shape Detection & Classification (Fallback Guide)

Ye document explain karta hai ki bina kisi third-party helper library (`cvzone`) ke, pure OpenCV (`cv2`) aur NumPy ke through shape detection aur classification kaise karein.

---

## 1. 5-Step Core Pipeline (Pure OpenCV)

```python
import cv2
import numpy as np

# Step 1: Read image
img = cv2.imread("shapes.png")

# Step 2: Grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Step 3: Gaussian Blur + Canny Edge Detection
blur = cv2.GaussianBlur(gray, (5, 5), 1)
canny = cv2.Canny(blur, 50, 150)

# Step 4: Dilation (Bridge broken edge segments)
kernel = np.ones((5, 5), np.uint8)
dilated = cv2.dilate(canny, kernel, iterations=1)

# Step 5: Find Contours
contours, hierarchy = cv2.findContours(
    dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)
```

---

## 2. Polygon Approximation & Corner Counting

Har contour ke liye perimeter calculate karke `cv2.approxPolyDP` se simplify kiya jata hai:

```python
for cnt in contours:
    area = cv2.contourArea(cnt)
    
    # Noise filter: skip small dust particles
    if area < 500:
        continue
    
    # Perimeter
    peri = cv2.arcLength(cnt, closed=True)
    
    # Polygon approximation (epsilon typically 0.02 * perimeter)
    approx = cv2.approxPolyDP(cnt, 0.02 * peri, closed=True)
    num_corners = len(approx)
    
    # Bounding rectangle
    x, y, w, h = cv2.boundingRect(approx)
    
    # Shape Classification
    if num_corners == 3:
        shape_type = "Triangle"
    elif num_corners == 4:
        aspect_ratio = float(w) / float(h)
        if 0.95 <= aspect_ratio <= 1.05:
            shape_type = "Square"
        else:
            shape_type = "Rectangle"
    elif num_corners == 5:
        shape_type = "Pentagon"
    elif num_corners == 6:
        shape_type = "Hexagon"
    else:
        # Check circularity: 4 * pi * area / (perimeter^2)
        circularity = 4 * np.pi * (area / (peri * peri))
        if circularity > 0.7:
            shape_type = "Circle"
        else:
            shape_type = f"Polygon ({num_corners} pts)"

    # Draw result
    cv2.drawContours(img, [approx], -1, (0, 255, 0), 2)
    cv2.putText(img, shape_type, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
```

---

## 3. Best Practices & Troubleshooting

1. **Epsilon Parameter in `approxPolyDP`**:
   - `0.02 * peri` is the standard.
   - If shapes are noisy / corners are over-counted, increase to `0.03 * peri` or `0.04 * peri`.
   - If sharp corners are missed, decrease to `0.01 * peri`.

2. **Canny Thresholds**:
   - High contrast / clean images: `(50, 150)`
   - Dark / low contrast images: `(30, 100)`
   - Noisy background images: `(100, 200)`
