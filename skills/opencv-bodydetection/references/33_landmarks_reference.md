# MediaPipe 33 Pose Landmarks Reference Guide

This document provides a comprehensive technical reference for the 33 anatomical body joints tracked by Google MediaPipe Pose and `cvzone.PoseModule`.

---

## 1. Landmark Topology & Anatomical Map

```text
                         0 [Nose]
                   1 [L Eye Inner]    4 [R Eye Inner]
                   2 [L Eye]          5 [R Eye]
                   3 [L Eye Outer]    6 [R Eye Outer]
                   7 [L Ear]          8 [R Ear]
                   9 [Mouth Left]    10 [Mouth Right]
                          │          │
           [L Shoulder] 11────────────12 [R Shoulder]
                       / │            │ \
              [L Elbow] 13 │            │ 14 [R Elbow]
                     /   │            │   \
            [L Wrist] 15  │            │    16 [R Wrist]
     [L Pinky] 17 ──┐    │            │    ┌── 18 [R Pinky]
     [L Index] 19 ──┼────┘            └────┼── 20 [R Index]
     [L Thumb] 21 ──┘                      └── 22 [R Thumb]
                        23────────────24 [R Hip]
                   [L Hip]│            │
                          │            │
                 [L Knee] 25            26 [R Knee]
                          │            │
                [L Ankle] 27            28 [R Ankle]
                 [L Heel] 29            30 [R Heel]
           [L Foot Index] 31            32 [R Foot Index]
```

---

## 2. Complete 33 Landmark Points Table

| Landmark ID | Anatomical Name | Body Part | Description & Common Use Cases |
| :---: | :--- | :--- | :--- |
| **0** | `NOSE` | Head / Face | Head position, facial orientation |
| **1** | `LEFT_EYE_INNER` | Head / Face | Eye gaze, facial tilt |
| **2** | `LEFT_EYE` | Head / Face | Eye blinking & head orientation |
| **3** | `LEFT_EYE_OUTER` | Head / Face | Facial boundary |
| **4** | `RIGHT_EYE_INNER` | Head / Face | Eye gaze, facial tilt |
| **5** | `RIGHT_EYE` | Head / Face | Eye blinking & head orientation |
| **6** | `RIGHT_EYE_OUTER` | Head / Face | Facial boundary |
| **7** | `LEFT_EAR` | Head / Face | Head turn & yaw rotation |
| **8** | `RIGHT_EAR` | Head / Face | Head turn & yaw rotation |
| **9** | `MOUTH_LEFT` | Head / Face | Smile / mouth movement |
| **10** | `MOUTH_RIGHT` | Head / Face | Smile / mouth movement |
| **11** | `LEFT_SHOULDER` | Upper Body | Shoulder press, posture slouch, pushups |
| **12** | `RIGHT_SHOULDER` | Upper Body | Shoulder press, posture slouch, pushups |
| **13** | `LEFT_ELBOW` | Arm | Bicep curl, push-up angle, boxing punch |
| **14** | `RIGHT_ELBOW` | Arm | Bicep curl, push-up angle, boxing punch |
| **15** | `LEFT_WRIST` | Arm | Hand raising, punching, reaching |
| **16** | `RIGHT_WRIST` | Arm | Hand raising, punching, reaching |
| **17** | `LEFT_PINKY` | Hand | Grip estimation, hand boundary |
| **18** | `RIGHT_PINKY` | Hand | Grip estimation, hand boundary |
| **19** | `LEFT_INDEX` | Hand | Hand gesture, pointing, clapping |
| **20** | `RIGHT_INDEX` | Hand | Hand gesture, pointing, clapping |
| **21** | `LEFT_THUMB` | Hand | Thumb orientation |
| **22** | `RIGHT_THUMB` | Hand | Thumb orientation |
| **23** | `LEFT_HIP` | Torso / Pelvis | Squats, jumping jacks, hip rotation |
| **24** | `RIGHT_HIP` | Torso / Pelvis | Squats, jumping jacks, hip rotation |
| **25** | `LEFT_KNEE` | Leg | Squat depth, lunges, running strides |
| **26** | `RIGHT_KNEE` | Leg | Squat depth, lunges, running strides |
| **27** | `LEFT_ANKLE` | Leg / Foot | Foot placement, balance, jump height |
| **28** | `RIGHT_ANKLE` | Leg / Foot | Foot placement, balance, jump height |
| **29** | `LEFT_HEEL` | Foot | Heel strike detection during walking |
| **30** | `RIGHT_HEEL` | Foot | Heel strike detection during walking |
| **31** | `LEFT_FOOT_INDEX` | Foot / Toes | Toe tap, running cadence, dance games |
| **32** | `RIGHT_FOOT_INDEX` | Foot / Toes | Toe tap, running cadence, dance games |

---

## 3. Coordinate System & Values

Each landmark point extracted via `detector.findPosition(img)` provides:
1. **$x$ coordinate:** Pixel location along horizontal width of image (`0` to `image_width`).
2. **$y$ coordinate:** Pixel location along vertical height of image (`0` to `image_height`).
3. **$z$ coordinate:** Relative depth metric (roughly scaled to pixel space by `cvzone`). Landmarks closer to the camera have negative/smaller $z$ values, while landmarks farther have larger $z$ values. The coordinate frame origin is roughly centered between the hips.

---

## 4. Key Landmark Groups & Triangles for Angle Calculation

To measure joint angles with `detector.findAngle(p1, p2, p3, img)`:

| Exercise / Movement | Joint Vertex (`p2`) | Anchor 1 (`p1`) | Anchor 2 (`p3`) | Landmark IDs `(p1, p2, p3)` |
| :--- | :--- | :--- | :--- | :--- |
| **Left Bicep Curl** | Left Elbow | Left Shoulder | Left Wrist | `(11, 13, 15)` |
| **Right Bicep Curl** | Right Elbow | Right Shoulder | Right Wrist | `(12, 14, 16)` |
| **Left Squat** | Left Knee | Left Hip | Left Ankle | `(23, 25, 27)` |
| **Right Squat** | Right Knee | Right Hip | Right Ankle | `(24, 26, 28)` |
| **Push-ups (Arm Angle)**| Elbow | Shoulder | Wrist | `(11, 13, 15)` / `(12, 14, 16)` |
| **Spine Lean / Slouch** | Hip Center | Shoulder Center | Vertical Ref | Midpoints `(11, 12)` vs `(23, 24)` |

---

## 5. Performance Optimization Tips

1. **Static vs Video Mode:**
   - Always keep `staticMode=False` for video/webcam. In video mode, the detector uses fast tracking instead of heavy re-detection on every frame.
2. **Resolution Scaling:**
   - Running at `640x480` or `1280x720` provides 30–60 FPS on standard CPUs.
3. **Model Complexity (`modelComplexity`):**
   - `0` (Lite): Best for Raspberry Pi or low-end laptops.
   - `1` (Full): Ideal balance of speed and accuracy for webcam desktop apps.
   - `2` (Heavy): Best for precision medical posture analysis or offline video rendering.
