# My Coding Skills 🧠⚡

A curated collection of specialized, production-ready coding skills and procedural workflows for **Antigravity (AGY)** and AI coding assistants.

---

## 📂 Repository Structure

```text
.
├── skills/
│   ├── deep-agent/
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   └── references/
│   ├── opencv-shape-detection/
│   │   ├── SKILL.md                          # Antigravity skill definition & triggers
│   │   ├── scripts/
│   │   │   └── detect_shapes.py              # Ready-to-use Python shape detection CLI
│   │   └── references/
│   │       └── manual_classification.md      # Pure OpenCV fallback guide
│   └── opencv-color-detection/
│       ├── SKILL.md                          # Antigravity color detection skill
│       ├── scripts/
│       │   ├── find_color_trackbar.py        # Interactive HSV discovery tool
│       │   └── color_detection_template.py   # Production color detection & tracking template
│       └── references/
│           └── hsv_color_guide.md            # Pure OpenCV HSV guide & lookup tables
└── README.md
```

---

## 🛠️ Included Skills

### 1. `opencv-shape-detection`
- **Purpose**: Fast, robust geometric shape detection and classification (Triangle, Square, Rectangle, Pentagon, Hexagon, Circle) using Python & OpenCV.
- **Pipeline**: Grayscale ➔ Canny Edge Detection ➔ Morphological Dilation ➔ Contour Finding ➔ Corner-Count Classification.
- **Triggers**: Shape detection in images, contour detection, OpenCV shape recognition, corner count classification.

#### Quick Run
```bash
pip install opencv-python numpy cvzone

# Run on an image
python skills/opencv-shape-detection/scripts/detect_shapes.py --image path/to/image.png

# Run with live webcam feed
python skills/opencv-shape-detection/scripts/detect_shapes.py --webcam
```

### 2. `opencv-color-detection`
- **Purpose**: Real-time color detection, HSV masking, and object tracking with OpenCV and `cvzone`.
- **Pipeline**: HSV Trackbar Calibration ➔ Value Locking ➔ `ColorFinder` Masking ➔ `findContours` Position Tracking.
- **Triggers**: Color detection, color tracking, HSV mask, find object by color.

#### Quick Run
```bash
pip install opencv-python cvzone

# 1. Discover HSV range with interactive trackbars
python skills/opencv-color-detection/scripts/find_color_trackbar.py

# 2. Run production color detection & tracking
python skills/opencv-color-detection/scripts/color_detection_template.py
```

---

## ⚙️ How to Use with Antigravity (AGY)

These skills are automatically detected by Antigravity:
1. **Workspace Level**: Place the skill in `.agent/skills/<skill-name>/` or `.agents/skills/<skill-name>/` in your project root.
2. **Global System Level**: Placed in `~/.gemini/antigravity-cli/skills/<skill-name>/` or `~/.gemini/config/skills/<skill-name>/` for system-wide availability across all projects.

---

## 🚀 Pushing & Updating Skills

```bash
git add .
git commit -m "Add and update skills"
git push origin main
```
