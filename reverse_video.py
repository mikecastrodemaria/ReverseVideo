"""
reverse_video_gradio.py - Gradio and CLI application to reverse one or more videos frame by frame.

Features:
- Gradio UI to upload one or multiple videos, preview the reversed version, and download the results.
- Displays original video preview.
- Option to keep and view extracted frames.
- CLI support via --video for batch processing.
- --video-loop option to concatenate original + reversed video (ab or ba).

Requirements: moviepy, gradio, argparse, tempfile
"""

import os
import gradio as gr
import argparse
from moviepy.editor import VideoFileClip, ImageSequenceClip, concatenate_videoclips

def extract_and_reverse(video_path, keep_frames=False, output_name=None):
    """
    Extracts frames from a video, reverses them, and saves the reversed video.
    Parameters:
        video_path (str): Path to the input video file.
        keep_frames (bool): Whether to keep the extracted frames.
        output_name (str): Custom name for the reversed video output.
    Returns:
        (str, list): Path to the reversed video, and list of frame paths if kept.
    """
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    frames_folder = os.path.join(os.path.dirname(__file__), "extracted_frames", base_name)
    os.makedirs(frames_folder, exist_ok=True)

    clip = VideoFileClip(video_path)
    fps = clip.fps
    frames = []

    for i, t in enumerate([t / fps for t in range(int(clip.duration * fps))]):
        frame_path = os.path.join(frames_folder, f"frame_{i:05d}.jpg")
        clip.save_frame(frame_path, t)
        frames.append(frame_path)

    reversed_frames = sorted(frames, reverse=True)
    reversed_clip = ImageSequenceClip(reversed_frames, fps=fps)

    if output_name is None:
        output_name = f"{base_name}_reversed.mp4"

    output_video_dir = os.path.join(os.path.dirname(__file__), "reversed_videos")
    os.makedirs(output_video_dir, exist_ok=True)
    output_path = os.path.join(output_video_dir, output_name)
    reversed_clip.write_videofile(output_path, codec='libx264', audio=False)

    return output_path, frames if keep_frames else []

def combine_clips(original_path, reversed_path, order='ab'):
    """
    Concatenates the original and reversed videos in the specified order.
    Parameters:
        original_path (str): Path to original video.
        reversed_path (str): Path to reversed video.
        order (str): 'ab' or 'ba' for order of combination.
    Returns:
        str: Path to the combined video.
    """
    original = VideoFileClip(original_path)
    reversed_ = VideoFileClip(reversed_path)
    clips = [original, reversed_] if order == 'ab' else [reversed_, original]
    final = concatenate_videoclips(clips)
    combined_path = reversed_path.replace("_reversed", f"_combo_{order}")
    final.write_videofile(combined_path, codec='libx264', audio=False)
    return combined_path

def process_video(file, keep_frames):
    """
    Gradio process function to handle file input and trigger video reversal.
    Parameters:
        file: Uploaded video file.
        keep_frames (bool): Whether to keep extracted frames.
    Returns:
        Tuple containing status message, original path, reversed video path, and frame list.
    """
    if file is None:
        return "Aucune vidéo chargée.", None, None, None

    orig_name = os.path.basename(file.name)
    base_name = os.path.splitext(orig_name)[0]
    output_name = f"{base_name}_reversed.mp4"

    output_path, frame_list = extract_and_reverse(
        video_path=file.name,
        keep_frames=keep_frames,
        output_name=output_name
    )

    return "✅ Vidéo inversée avec succès !", file.name, output_path, frame_list

def gradio_app():
    """
    Launches the Gradio app UI for the reverse video tool.
    """
    with gr.Blocks() as demo:
        gr.Markdown("""
        ## Reverse Video Tool 🎞️
        Upload a video, reverse it, and preview the result. 
        Check the box to keep extracted frames.
        """)

        with gr.Row():
            with gr.Column(scale=1):
                video_input = gr.File(label="📂 Load a video", file_types=[".mp4", ".mov", ".avi"], file_count="multiple")
                keep_frames = gr.Checkbox(label="🗂️ Keep extracted frames")
                loop_mode = gr.Radio(
                    choices=["none", "ab", "ba"],
                    value="none",
                    label="🔁 Combine original and reversed video",
                    info="Choose how to concatenate original and reversed videos (or not)"
                )
                with gr.Row():
                    clear_btn = gr.Button("Clear")
                    submit_btn = gr.Button("Submit", variant="primary")
                original_preview = gr.Video(label="📼 Original Video")

            with gr.Column(scale=1):
                status_output = gr.Textbox(label="🔁 Processing status")
                video_output = gr.Video(label="🎥 Reversed Video (preview & download)")
                frames_output = gr.Gallery(label="🖼️ Extracted frames (if kept)", show_label=True, columns=6, object_fit="contain")

        def gr_process(files, keep_frames, loop_mode):
            if not files:
                return "No video selected.", None, None, None
            paths = []
            all_frames = []
            reversed_path = None
            for file in files:
                reversed_path, frames = extract_and_reverse(file.name, keep_frames=keep_frames)
                paths.append(reversed_path)
                all_frames.extend(frames)

                if loop_mode in ["ab", "ba"]:
                    combine_clips(file.name, reversed_path, order=loop_mode)

            return "✅ All videos reversed!", files[0].name, reversed_path, all_frames

        submit_btn.click(fn=gr_process, inputs=[video_input, keep_frames, loop_mode], outputs=[status_output, original_preview, video_output, frames_output])
        clear_btn.click(fn=lambda: ("", None, None, None, "none"), outputs=[status_output, original_preview, video_output, frames_output, loop_mode])

    demo.launch()

def shell_mode(paths, keep_frames=False, loop_mode=None):
    """
    CLI mode handler to reverse one or more videos and optionally combine with original.
    Parameters:
        paths (list): List of video paths.
        keep_frames (bool): Whether to keep extracted frames.
        loop_mode (str): 'ab' or 'ba' for combining original and reversed.
    """
    for path in paths:
        print(f"[INFO] Processing: {path}")
        output_path, _ = extract_and_reverse(path, keep_frames=keep_frames)
        print(f"[SUCCESS] Reversed video saved at: {output_path}")

        if loop_mode in ["ab", "ba"]:
            combined = combine_clips(path, output_path, order=loop_mode)
            print(f"[INFO] Combined video saved at: {combined}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", nargs='+', help="Path(s) to the video(s) to reverse")
    parser.add_argument("--keep-frames", action="store_true", help="Keep extracted frames")
    parser.add_argument("--video-loop", choices=["ab", "ba"], help="Concatenate original and reversed video in ab or ba order")
    args = parser.parse_args()

    if args.video:
        shell_mode(args.video, keep_frames=args.keep_frames, loop_mode=args.video_loop)
    else:
        gradio_app()
