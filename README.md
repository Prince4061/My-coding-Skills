# My Coding Skills 🧠⚡

A curated collection of specialized, production-ready coding skills and procedural workflows for **Antigravity (AGY)** and AI coding assistants.

---

## 📂 Repository Structure

```text
.
├── .agent/
│   └── skills/
│       └── opencv-shape-detection/
│           ├── SKILL.md                          # Antigravity skill definition & triggers
│           ├── scripts/
│           │   └── detect_shapes.py              # Ready-to-use Python shape detection CLI
│           └── references/
│               └── manual_classification.md      # Pure OpenCV fallback guide
├── skills/
│   └── opencv-shape-detection/                   # Mirrored skill directory
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
python .agent/skills/opencv-shape-detection/scripts/detect_shapes.py --image path/to/image.png

# Run with live webcam feed
python .agent/skills/opencv-shape-detection/scripts/detect_shapes.py --webcam
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
