# Reverse Video Tool 🎞️

A Python-based video utility that reverses one or more videos frame by frame. Use it via the command line or an intuitive web interface powered by Gradio.

## ✨ Features

- ✅ Reverse videos frame by frame with accurate timing.
- 📂 Upload one or several videos at once (batch support).
- 🎥 Preview the original and reversed versions directly in the interface.
- 🖼️ Optionally extract and display individual frames.
- 🔁 Combine original and reversed videos (`ab` or `ba` mode).
- 🖥️ Dual-mode: Gradio Web UI **or** Command-Line Interface.
- 🗂️ Output video files saved in `reversed_videos/`.
- 🗂️ Extracted frames saved in `extracted_frames/`.


https://youtu.be/MuEo06nxnBU
https://youtu.be/M1lhnVqsVqo
https://youtu.be/cCmkSdizXeg

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-user/ReverseVideoTool.git
cd ReverseVideoTool
```

### 2. Launch via `run.bat` (Windows)

Double-click or run in terminal:

```bat
run.bat
```

This will:
- Set up a virtual environment (`venv`)
- Install all dependencies (`requirements.txt`)
- Launch either the CLI or the Gradio app

---

## 🖥️ Usage: Command-Line

```bash
python reverse_video.py --video myclip.mp4 anotherclip.mp4 --keep-frames --video-loop ab
```

### Options:

| Option              | Description                                              |
|---------------------|----------------------------------------------------------|
| `--video`           | One or more paths to video files to reverse              |
| `--keep-frames`     | Store the extracted frames in `extracted_frames/`        |
| `--video-loop`      | `ab` = original+reverse, `ba` = reverse+original         |

### Example:

```bash
python reverse_video.py --video input.mp4 --keep-frames --video-loop ba
```

---

## 🌐 Usage: Web Interface (Gradio)

To launch:

```bash
python reverse_video.py
```

### Interface Features:
- Upload multiple videos
- Checkbox to retain frames
- Radio button to choose video combination: none / `ab` / `ba`
- Visual previews for both input and output
- Frame gallery display (if enabled)

---

## 📁 Folder Structure

```text
📂 reversed_videos/
    └── myvideo_reversed.mp4
    └── myvideo_combo_ab.mp4

📂 extracted_frames/
    └── myvideo/
        └── frame_00001.jpg
        └── ...
```

---

## 🛠 Requirements

Install them manually (if needed):

```bash
pip install -r requirements.txt
```

### Main dependencies:

- `moviepy`
- `gradio`
- `argparse`

---

## 🤖 Technical Notes

- All videos are processed frame-by-frame, avoiding timing drift.
- Video previews in Gradio are rendered using temporary files.
- Output names follow the pattern:
  - `basename_reversed.mp4`
  - `basename_combo_ab.mp4` or `basename_combo_ba.mp4`

---

## 🧠 Author

Mike Castro de Maria - [Supersonique Studio](https://supersonique.studio)

---

## 📜 License

MIT License
