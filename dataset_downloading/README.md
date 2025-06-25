## Video Downloading

This section describes the steps for downloading the original videos of the **Sekai-Real** dataset.

### 🛠️ Prerequisites

- [yt-dlp](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#installation) video downloader
- python3

### 📝 Steps

Let's take the `sekai-real-walking-hq` split as an example, see all splits [here]((https://github.com/Lixsp11/sekai-codebase?tab=readme-ov-file#-quick-start)).

- Download annotation file `sekai-real-walking-hq.csv` from [here](https://github.com/Lixsp11/sekai-codebase?tab=readme-ov-file#-quick-start).

- Extract video URLs from the annotation file and save them to `sekai-real-walking-hq_urls.txt`.

  ```bash
  python csv_to_urls.py --input_file sekai-real-walking-hq.csv
  ```

- Download videos to `./videos` with yt-dlp.

  ```bash
  yt-dlp -N 10 -f 299+bestaudio -a sekai-real-walking-hq_urls.txt -o "./videos/%(id)s.%(ext)s"
  ```

  This command will download each video in 1080p at 60fps with the best available audio quality.

### ⚠️ Known Issues

| **Error Message**                                            | **Solution**                                                 |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| `WARNING: You have requested merging of multiple formats but ffmpeg is not installed. The formats won't be merged` | Refer to [this](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#strongly-recommended) for installing custom builds of FFmpeg for yt-dlp. |
| `Unable to download webpage: HTTP Error 403: Forbidden`      | Your IP got blocked. Change your IP for downloading. Refer [this issue](https://github.com/yt-dlp/yt-dlp/issues/8785) for more details. |



