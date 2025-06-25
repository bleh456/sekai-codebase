import multiprocessing.dummy  # noqa: I001
import os
import logging
import argparse
import shlex
import subprocess

import tqdm


def extract_astream(video_filename, astream_filename):
    subprocess.run(
        shlex.split(
            "ffmpeg -y -i {} -map 0:a:0 -c:a flac -ar 48000 -ac 2 -sample_fmt s16 -loglevel error {}".format(
                video_filename, astream_filename
            )
        ),
        check=True,
    )
    logging.info(f"Finish process video '{os.path.splitext(os.path.basename(video_filename))[0]}'.")


def extract_astream_wrapper(kargs):
    return extract_astream(*kargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str)
    parser.add_argument("--output_dir", type=str, default=None)
    parser.add_argument("--num_workers", type=int, default=os.cpu_count() // 4)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    if args.output_dir is None:
        args.output_dir = args.input_file + "_astreams"

    os.makedirs(args.output_dir, exist_ok=False)

    vids = sorted([os.path.splitext(vid)[0] for vid in os.listdir(args.input_dir)])
    logging.info(f"Start process {len(vids)} videos.")

    kargs = []
    for vid in vids:
        kargs.append((os.path.join(args.input_dir, f"{vid}.mkv"), os.path.join(args.output_dir, f"{vid}.flac")))

    with multiprocessing.dummy.Pool(processes=args.num_workers) as pool:
        results = pool.imap_unordered(extract_astream_wrapper, kargs)
        for _ in tqdm.tqdm(results, total=len(kargs), mininterval=10):
            pass
