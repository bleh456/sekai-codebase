import multiprocessing.dummy  # noqa: I001
import os
import shutil
import argparse
import logging
import shlex
import subprocess

import tqdm


def process_one_video(args, vid, clips, ignore_audio=False):
    os.makedirs(os.path.join(args.output_dir, vid), exist_ok=False)
    os.makedirs(os.path.join(args.output_dir, vid, "temp"), exist_ok=False)

    raw_astream_filename = os.path.join(args.input_astream_dir, f"{vid}.flac")

    vstream_filename = os.path.join(args.input_vstream_dir, vid, f"{vid}_{{:07d}}_{{:07d}}.hevc")
    astream_filename = os.path.join(args.output_dir, vid, "temp", f"{vid}_{{:07d}}_{{:07d}}.m4a")
    clip_filename = os.path.join(args.output_dir, vid, f"{vid}_{{:07d}}_{{:07d}}.mp4")

    files = []
    for sframe, eframe in clips:
        stime, etime = round(sframe / 30.0, 6), round(eframe / 30.0, 6)
        _vstream_filename = vstream_filename.format(sframe, eframe)
        _astream_filename = astream_filename.format(sframe, eframe)
        _clip_filename = clip_filename.format(sframe, eframe)

        if not ignore_audio:
            subprocess.run(
                shlex.split(
                    "ffmpeg -i {} -ss {} -to {} -c:a aac -ar 48000 -ac 2 -b:a 192k -loglevel error {}".format(
                        raw_astream_filename, stime, etime, _astream_filename
                    )
                ),
                check=True,
            )
            subprocess.run(
                shlex.split(
                    "ffmpeg -i {} -i {} -map 0:v -map 1:a -c copy -t 60 -movflags +faststart -vtag hvc1 "
                    "-loglevel error {}".format(_vstream_filename, _astream_filename, _clip_filename),
                ),
                check=True,
            )
        else:
            subprocess.run(
                shlex.split(
                    "ffmpeg -i {} -map 0:v -c copy -t 60 -movflags +faststart -vtag hvc1 -loglevel error {}".format(
                        _vstream_filename, _clip_filename
                    ),
                ),
                check=True,
            )

        files.append(os.path.basename(_clip_filename))

    shutil.rmtree(os.path.join(args.output_dir, vid, "temp"))
    logging.info(f"Finish process video '{vid}', generate {len(files)} video clips.")


def process_one_video_wrapper(kargs):
    result = process_one_video(*kargs)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_clip_dir", type=str)
    parser.add_argument("--input_astream_dir", type=str)
    parser.add_argument("--input_vstream_dir", type=str)
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--ignore_audio", action="store_true", help="Ignore audio stream during processing.")
    parser.add_argument("--num_workers", type=int, default=os.cpu_count() // 4)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    if args.output_dir is None:
        args.output_dir = args.input_clip_dir + "_clips"

    os.makedirs(args.output_dir, exist_ok=False)

    vids = sorted([os.path.splitext(vid)[0] for vid in os.listdir(args.input_clip_dir)])
    logging.info(f"Start process {len(vids)} videos.")

    kargs = []
    for vid in vids:
        with open(os.path.join(args.input_clip_dir, f"{vid}.txt"), "r") as f:
            clips = [tuple(map(int, line.strip().split(" "))) for line in f]

        # process_one_video(vid, clips)
        kargs.append((args, vid, clips, args.ignore_audio))

    with multiprocessing.dummy.Pool(processes=args.num_workers) as pool:
        results = pool.imap_unordered(process_one_video_wrapper, kargs)
        for _ in tqdm.tqdm(results, total=len(kargs), mininterval=120):
            pass
