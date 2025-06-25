# Clip Extracting

This section outlines the steps to extract video clips from the raw videos for the **Sekai-Real** dataset.

## 🛠️ Prerequisites

- NVIDIA GPU with NVENC support, see [Video Encode and Decode GPU Support Matrix](https://developer.nvidia.com/video-encode-and-decode-gpu-support-matrix-new).

- CUDA 11.8.

- FFmpeg for audio processing and remixing. Easily install with the following command in a Conda environment:

  ```bash
  conda install ffmpeg
  ```

- Python 3.10 with dependencies:

  ```bash
  pip install -r requirements.txt
  ```

## 📝 Steps

Let's take sekai-real-walking-hq as an example.

- Finish the [dataset downloading](https://github.com/Lixsp11/sekai-codebase/tree/main/dataset_downloading) step.

- Extract video clip metadata (start and end frame index of each video clip) to `sekai-real-walking-hq` dir.

  ```bash
  python 1_csv_to_clips.py --input_file sekai-real-walking-hq.csv
  ```

- Split the audio streams from raw videos and save them in FLAC format to the `./astreams` directory.

  > **You can skip this step if you're fine with mute videos.**

  ```bash
  python 2_split_audios.py --input_dir ./videos --output_dir ./astreams --num_workers 32
  ```

   `--num_workers` specifies the number of tasks to be processed in parallel. You can adjust it based on the number of CPU cores available. By default, it's set to one-fourth of the total CPU cores. On our machine, the above command runs at ~3.5 seconds per video.

- Split the video streams of individual clips from raw videos and save them in H265 format to the `./vstreams` directory.

  The pipeline is based on `PyNvVideoCodec` and generates all clips of each video in one pass. It runs at ~300 FPS on a RTX 4090 GPU.

  ```bash
  python 3_nvtranscoding.py --input_clip_dir sekai-real-walking-hq --input_video_dir ./videos --output_dir ./vstreams
  ```

  If you have multiple GPUs, you can use a specific one by setting `--device_id` (default is 0).

- Remix and package the processed video clips.

  ```bash
  python 4_remix_to_files.py --input_clip_dir sekai-real-walking-hq --input_astream_dir ./astreams --input_vstream_dir ./vstreams --output_dir ./files
  ```

  Add `--ignore_audio` if you're fine with mute videos.

## ⚠️ Known Issues

- You might encounter some warning in step 3 (`3_nvtranscoding.py`):

  ```bash
  [INFO ][18:48:46] Media format: Matroska / WebM (matroska,webm)
  [NULL @ 0x863db00] No codec provided to avcodec_open2()
  [WARN ][18:48:46] ChromaFormat not recognized. Assuming 420
  ```

  These messages appear because `PyNvVideoCodec` uses FFmpeg to probe the container format but handles decoding internally, without passing parameters to FFmpeg’s `avcodec_open2()`. They can be safely ignored.

