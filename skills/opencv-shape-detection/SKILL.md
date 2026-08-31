---
name: opencv-shape-detection
description: Use this skill whenever the user wants to detect geometric shapes (triangle, square, rectangle, circle, or generic polygons) inside an image using OpenCV/Python. Trigger on requests like "shape detect karna hai", "triangle square circle detect karo", "contour detection", "OpenCV se shapes pehchano", "corner count se classify karo", or any mention of Canny edge detection + contours + cvzone findContours for shape recognition — even if the user doesn't say "skill" explicitly. This is the user's personal standard pipeline (Grayscale, Canny, Dilation, Contours, Classification, in that order) and should be reused as the default template for ANY future shape-detection task in OpenCV, rather than inventing a different approach from scratch.
---

# OpenCV Shape Detection Pipeline

Ye user ka standard/preferred pipeline hai geometric shapes (triangle, square, rectangle, circle) ko image mein detect karne ke liye. Jab bhi shape detection ka kaam aaye, isi 5-step pipeline ko base bana kar code likho — naya approach invent mat karo jab tak user specifically kuch alag na maange.

## Kyun ye pipeline?

Har step ek specific purpose solve karta hai, isliye order maintain karna zaroori hai:

1. **Grayscale** — color info (3 channels) hata kar computation lightweight banata hai, kyunki edge detection ko sirf intensity chahiye, color nahi.
2. **Canny edge detection** — intensity gradients se sharp boundaries dhoondta hai; yahi edges baad mein contours banenge.
3. **Dilation** — Canny se aane wali tooti-phooti/thin lines ko thick continuous bana deta hai, taaki `findContours` unhe ek complete closed shape ke roop mein pehchan sake (warna gaps ki wajah se contour detection unreliable ho jata hai).
4. **Contour finding** — dilated edge-map par contours nikalta hai, saath hi har contour ki geometry (center, area, bounding box) bhi milti hai.
5. **Classification** — approximated polygon ke corner-count se decide hota hai ki shape triangle hai, square/rectangle hai, ya circle.

## Standard code template

Ye template use karo as starting point, phir user ke specific requirement (image path, filter, thresholds) ke hisaab se customize karo:

```python
import cv2
import numpy as np
import cvzone
from cvzone.utilities import findContours

# 1. Load image
img = cv2.imread("shapes.png")

# 2. Grayscale conversion
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. Edge detection (Canny)
imgCanny = cv2.Canny(imgGray, 50, 150)

# 4. Dilation - thicken broken edges
kernel = np.ones((5, 5), np.uint8)
imgDilated = cv2.dilate(imgCanny, kernel, iterations=1)

# 5. Contour finding (also returns geometry: center, area, bbox)
imgContours, conFound = findContours(
    img, imgDilated, filter=None, drawContours=True
)

# Optional: visualize all stages together
imgStack = cvzone.stackImages(
    [img, imgGray, imgCanny, imgContours], cols=2, scale=0.5
)

cv2.imshow("Shape Detection", imgStack)
cv2.waitKey(0)
```

Iska ready-to-run, complete script jisme corner-count se classification, text annotations, aur image/webcam support hai:
- [`scripts/detect_shapes.py`](./scripts/detect_shapes.py)

Fallback manual method (pure OpenCV without `cvzone`):
- [`references/manual_classification.md`](./references/manual_classification.md)

## Dependencies

```bash
pip install opencv-python numpy cvzone
```

Agar `cvzone` install nahi ho pa raha ya network restricted hai, to fallback ke liye `references/manual_classification.md` wala pure OpenCV (`cv2.findContours` + `cv2.approxPolyDP`) use karo.

## Corner-count classification logic

`findContours` (ya manual `cv2.approxPolyDP`) se mile approximate corners count karke shape decide karo:

| Corners | Shape |
|---|---|
| 3 | Triangle |
| 4 | Square (agar width ≈ height) ya Rectangle (warna) |
| 5 | Pentagon |
| 6 | Hexagon |
| ~8+ (points) | Circle / Ellipse |

Square vs Rectangle decide karne ke liye bounding box ka `w` aur `h` compare karo:
```python
x, y, w, h = conFound[0]['bbox']
aspect_ratio = w / float(h)
shape_name = "Square" if 0.95 <= aspect_ratio <= 1.05 else "Rectangle"
```

## Useful fields from `conFound`

Har detected contour ek dict hai jisme ye milta hai:
- `conFound[i]['center']` — centroid `(x, y)`
- `conFound[i]['area']` — enclosed area (noise filter karne ke kaam aata hai, e.g. `[a for a in conFound if a['area'] > 500]`)
- `conFound[i]['bbox']` — `(x, y, w, h)` bounding box
- `conFound[i]['approx']` — approximated corner points

## Filtering specific shapes

Agar sirf kuch specific shapes chahiye (sab detect karke baad mein filter karne ke bajaye), `filter` parameter mein corner-count list pass karo:

```python
# sirf triangles
imgContours, conFound = findContours(img, imgDilated, filter=[3], drawContours=True)

# sirf square/rectangle
imgContours, conFound = findContours(img, imgDilated, filter=[4], drawContours=True)
```

## Customization points (task ke hisaab se adjust karo)

- **Canny thresholds `(50, 150)`** — agar edges bahut zyada noisy detect ho rahe hain to thresholds badhao; agar weak/faint edges miss ho rahe hain to ghatao.
- **Kernel size `(5, 5)` aur `iterations`** — chhoti/thin shapes ke liye kernel chhota rakho, warna shapes aapas mein merge ho sakti hain; bade gaps ke liye kernel ya iterations badhao.
- **Area-based noise filtering** — real-world images mein chhote dust/noise contours bhi mil jaate hain; `conFound[i]['area']` par minimum threshold laga kar unhe hata do (e.g. `minArea=1000`).
- **Live webcam feed** — same pipeline ko `cv2.VideoCapture(0)` loop ke andar daal kar real-time shape detection bhi ho sakta hai; sirf `img = cv2.imread(...)` ki jagah `success, img = cap.read()` use karo.

## Jab task complete ho

Agar user file input de (jaise image path), pipeline usi image par chalao aur result (annotated image + detected shapes ki list with center/area/bbox) dikhao. Agar sirf code chahiye (image nahi), to upar wala template hi customize karke do — extra boilerplate mat jodo.
