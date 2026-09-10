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
│   ├── langchain-model-load/
│   │   ├── SKILL.md                          # LangChain model loading & Hinglish teaching skill
│   │   ├── scripts/
│   │   │   ├── gemini_quickstart.py          # Single-turn prompt demo
│   │   │   ├── gemini_chat_memory.py         # Multi-turn chat loop with list memory
│   │   │   ├── gemini_streaming_chat.py      # Live streaming typing effect + persona
│   │   │   └── multi_provider_loader.py      # Gemini / Groq / OpenAI / Ollama loader
│   │   └── references/
│   │       ├── patterns.md                   # Canonical code patterns & board points
│   │       ├── model_providers.md            # Multi-provider reference guide
│   │       └── teaching_notes_template.md    # Hinglish lesson templates & board points
│   ├── langchain-prompts/
│   │   ├── SKILL.md                          # LangChain prompt templates & LCEL skill
│   │   ├── scripts/
│   │   │   ├── 01_prompt_template_basic.py   # PromptTemplate, variables & JSON escaping
│   │   │   ├── 02_chat_prompt_history.py     # ChatPromptTemplate & MessagesPlaceholder
│   │   │   ├── 03_few_shot_prompting.py      # Few-shot chat & text templates
│   │   │   ├── 04_lcel_chain_runner.py       # LCEL chain (prompt | model | parser)
│   │   │   └── 05_prompt_serialization.py    # Save/load prompt templates (JSON/YAML)
│   │   └── references/
│   │       ├── api-reference.md              # Technical reference & param details
│   │       └── hinglish-notes.md             # Hinglish explanations & board points
│   ├── langchain-structuredoutput/
│   │   ├── SKILL.md                          # LangChain structured output & Devesh's style
│   │   ├── scripts/
│   │   │   ├── 01_pydantic_structured_output.py    # Pydantic BaseModel validation demo
│   │   │   ├── 02_typeddict_structured_output.py   # Lightweight TypedDict demo
│   │   │   ├── 03_json_schema_structured_output.py # Pure JSON Schema dict demo
│   │   │   ├── 04_nested_models_and_lists.py       # Nested Pydantic models (Resume parser)
│   │   │   └── 05_include_raw_and_error_handling.py# include_raw=True & error handling
│   │   └── references/
│   │       ├── api-reference.md              # Technical API & config reference
│   │       ├── devesh-coding-style.md        # Complete Devesh Teaching Code Style guide
│   │       └── hinglish-notes.md             # Why -> What -> How -> Code classroom notes
│   ├── opencv-shape-detection/
│   │   ├── SKILL.md                          # Antigravity skill definition & triggers
│   │   ├── scripts/
│   │   │   └── detect_shapes.py              # Ready-to-use Python shape detection CLI
│   │   └── references/
│   │       └── manual_classification.md      # Pure OpenCV fallback guide
│   ├── opencv-face-detection/
│   │   ├── SKILL.md                          # Antigravity face detection skill
│   │   ├── scripts/
│   │   │   ├── face_detection_live.py        # Live webcam & image face detector CLI
│   │   │   └── face_blur_and_track.py        # Privacy face blurring & tracking vectors demo
│   │   └── references/
│   │       └── blazeface_mediapipe_guide.md  # BlazeFace deep learning architecture & Haar fallback
│   ├── opencv-color-detection/
│   │   ├── SKILL.md                          # Antigravity color detection skill
│   │   ├── scripts/
│   │   │   ├── find_color_trackbar.py        # Interactive HSV discovery tool
│   │   │   └── color_detection_template.py   # Production color detection & tracking template
│   │   └── references/
│   │       └── hsv_color_guide.md            # Pure OpenCV HSV guide & lookup tables
│   ├── opencv-bodydetection/
│   │   ├── SKILL.md                          # Body detection & 33 pose landmarks skill
│   │   ├── scripts/
│   │   │   ├── 01_body_detection_basic.py    # 6-step webcam body detection demo
│   │   │   ├── 02_exercise_rep_counter.py    # Workout rep counter (Curls & Squats)
│   │   │   └── 03_posture_and_center_tracker.py # Posture lean & centroid tracker
│   │   └── references/
│   │       ├── 33_landmarks_reference.md     # MediaPipe 33 landmark anatomical guide
│   │       └── hinglish_teaching_notes.md    # Hinglish lesson notes & classroom guide
│   └── opencv-handtracking/
│       ├── SKILL.md                          # Hand tracking & Hinglish student teaching skill
│       ├── scripts/
│       │   ├── hand_tracking_basic.py        # 8-step skeleton hand tracking demo
│       │   ├── finger_counter.py             # Real-time finger counting (0-5)
│       │   └── finger_distance_gesture.py    # Thumb-index distance & pinch gesture
│       └── references/
│           ├── code-style.md                 # Fixed beginner-friendly code style guide
│           └── notes-format.md               # Hinglish lesson notes format (Class 8-9)
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

### 2. `opencv-face-detection`
- **Purpose**: Ultra-fast, real-time face detection, confidence scoring, centroid tracking, and privacy blurring with OpenCV and `cvzone` (MediaPipe BlazeFace backend).
- **Pipeline**: Initialize `FaceDetector` (BlazeFace TFLite) ➔ `findFaces(img)` ➔ Extract Bounding Box `(x, y, w, h)`, Centroid `(cx, cy)` & Confidence Score ➔ Apply Tracking / Blur.
- **Triggers**: Face detection, face detect karo, cvzone FaceDetector, FaceDetectionModule, blaze_face, live webcam face detection, face bounding box, face blur, face count, face tracking.

#### Quick Run
```bash
pip install opencv-python cvzone mediapipe

# 1. Run live webcam face detection with FPS & confidence metrics
python skills/opencv-face-detection/scripts/face_detection_live.py

# 2. Run face privacy blurring & tracking demo (interactive toggles: B, T, D)
python skills/opencv-face-detection/scripts/face_blur_and_track.py

# 3. Run on a static image
python skills/opencv-face-detection/scripts/face_detection_live.py --image path/to/photo.jpg
```

### 3. `opencv-color-detection`
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

### 4. `langchain-model-load`
- **Purpose**: Beginner-friendly LangChain model loading (Google Gemini, Groq, OpenAI, Ollama), conversational list memory, live streaming, and Hinglish teaching notes with 3-board-point summaries.
- **Pipeline**: Environment Setup (`.env`) ➔ Direct Model Load (`ChatGoogleGenerativeAI`, `ChatGroq`, etc.) ➔ Clean `llm.invoke()` or `llm.stream()` ➔ Plain List Memory (`HumanMessage`, `AIMessage`).
- **Triggers**: LangChain model load, Gemini chatbot, model load karne ka code, Hinglish teaching notes, live streaming chatbot, board points.

#### Quick Run
```bash
pip install langchain-google-genai langchain-core python-dotenv

# 1. Run single-turn quickstart
python skills/langchain-model-load/scripts/gemini_quickstart.py

# 2. Run terminal chatbot with memory
python skills/langchain-model-load/scripts/gemini_chat_memory.py

# 3. Run streaming chat with live typing effect
python skills/langchain-model-load/scripts/gemini_streaming_chat.py

# 4. Test multi-provider model loader
python skills/langchain-model-load/scripts/multi_provider_loader.py
```

### 5. `hand-tracking-cvzone` (`opencv-handtracking`)
- **Purpose**: Real-time hand tracking, 21 landmark detection, finger counting, gesture distance measurement, and Hinglish lesson notes for school students (Class 8–9).
- **Pipeline**: Initialize `HandDetector(maxHands=2, detectionCon=0.8)` ➔ `findHands(img)` ➔ Extract 21 `lmList`, `bbox`, `center`, and `type` ➔ Process gestures (`fingersUp()`, `findDistance()`).
- **Triggers**: Hand tracking, HandDetector, cvzone hands, finger counting, gesture control, virtual mouse, volume control with fingers, hand notes / explanation.

#### Quick Run
```bash
pip install opencv-python cvzone mediapipe

# 1. Run basic 8-step hand tracking demo
python skills/opencv-handtracking/scripts/hand_tracking_basic.py

# 2. Run real-time finger counter (0-5)
python skills/opencv-handtracking/scripts/finger_counter.py

# 3. Run finger distance & pinch gesture tracker
python skills/opencv-handtracking/scripts/finger_distance_gesture.py
```

### 6. `langchain-prompt-templates` (`langchain-prompts`)
- **Purpose**: Composable, reusable LangChain prompt templates (`PromptTemplate`, `ChatPromptTemplate`, `MessagesPlaceholder`, few-shot templates, serialization, LCEL chains).
- **Pipeline**: Decide Model Type (Text vs Chat) ➔ Add Memory / Placeholders (`MessagesPlaceholder`) ➔ Apply Few-Shot / Partials if needed ➔ Pipe in LCEL (`prompt | model | parser`).
- **Triggers**: LangChain prompt banao, PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, few-shot, chat_history, LCEL prompt, Hinglish prompt notes.

#### Quick Run
```bash
pip install langchain-core langchain-google-genai python-dotenv

# 1. Basic PromptTemplate & partials
python skills/langchain-prompts/scripts/01_prompt_template_basic.py

# 2. Multi-turn ChatPromptTemplate with chat history
python skills/langchain-prompts/scripts/02_chat_prompt_history.py

# 3. Few-shot chat & text classification
python skills/langchain-prompts/scripts/03_few_shot_prompting.py

# 4. End-to-end LCEL chain runner
python skills/langchain-prompts/scripts/04_lcel_chain_runner.py

# 5. Prompt serialization & loading (JSON/YAML)
python skills/langchain-prompts/scripts/05_prompt_serialization.py
```

### 7. `opencv-bodydetection` (`opencv-body-detection`)
- **Purpose**: Real-time human body & pose detection, 33 skeletal joint landmark tracking, exercise workout rep counting (curls, squats), posture slouch & lean analysis, and beginner-friendly Hinglish lesson notes for students using OpenCV and `cvzone.PoseModule`.
- **Pipeline**: Initialize `PoseDetector()` ➔ `findPose(img)` ➔ `findPosition(img)` ➔ Extract 33 `lmList` coords & `bboxInfo` (center & bbox) ➔ Angle / Fitness logic (`detector.findAngle`).
- **Triggers**: Body detection, pose detection, cvzone PoseDetector, PoseModule, 33 landmarks, body posture, skeleton tracking, fitness tracking pushups squats, body joints, pose estimation.

#### Quick Run
```bash
pip install opencv-python cvzone mediapipe

# 1. Run basic 6-step webcam body detection
python skills/opencv-bodydetection/scripts/01_body_detection_basic.py

# 2. Run workout rep counter (Bicep curls & Squats)
python skills/opencv-bodydetection/scripts/02_exercise_rep_counter.py

# 3. Run posture lean & centroid tracker
python skills/opencv-bodydetection/scripts/03_posture_and_center_tracker.py
```

### 8. `langchain-structured-output` (`langchain-structuredoutput`)
- **Purpose**: Extract structured, validated data from LLMs using LangChain's `with_structured_output()` (Pydantic BaseModel, TypedDict, JSON Schema) strictly following Devesh's "Why → What → How → Code" pedagogical pattern with Hinglish comments and `# 🔥 Yaad Rakho` summary blocks.
- **Pipeline**: Problem Statement (Why) ➔ One-Line Concept (What) ➔ Analogy & Flow Diagram (How) ➔ `with_structured_output()` Code ➔ Summary (Yaad Rakho).
- **Triggers**: Structured output, Pydantic LangChain, TypedDict schema, JSON schema extraction, with_structured_output, teaching notes, Devesh's coding style, class mein explain karna.

#### Quick Run
```bash
pip install langchain-core langchain-google-genai pydantic python-dotenv

# 1. Pydantic BaseModel structured output & validation
python skills/langchain-structuredoutput/scripts/01_pydantic_structured_output.py

# 2. TypedDict lightweight dictionary extraction
python skills/langchain-structuredoutput/scripts/02_typeddict_structured_output.py

# 3. Pure JSON Schema extraction
python skills/langchain-structuredoutput/scripts/03_json_schema_structured_output.py

# 4. Nested models & lists (Resume Parser)
python skills/langchain-structuredoutput/scripts/04_nested_models_and_lists.py

# 5. Production debugging with include_raw=True & error catching
python skills/langchain-structuredoutput/scripts/05_include_raw_and_error_handling.py
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
