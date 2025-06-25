# Sekai: A Video Dataset towards World Exploration


<div align="center">



[![project page](https://img.shields.io/badge/Project-Page-2ea44f)](https://lixsp11.github.io/sekai-project/)&nbsp;
[![arXiv](https://img.shields.io/badge/arXiv%20paper-2506.15675-b31b1b.svg)](https://arxiv.org/abs/2506.15675)&nbsp;
[![demo](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Dataset-blue)](https://huggingface.co/datasets/Lixsp11/Sekai-Project)&nbsp;
[![YouTube](https://badges.aleen42.com/src/youtube.svg)](https://www.youtube.com/watch?v=5UQ0zAIZkSY)&nbsp;

</div>

This repo contains the dataset download and processing code used in

> [**Sekai: A Video Dataset towards World Exploration**](https://arxiv.org/abs/2506.15675)
>
> Zhen Li, Chuanhao Li, Xiaofeng Mao, Shaoheng Lin, Ming Li, Shitian Zhao, Zhaopan Xu,
> Xinyue Li, Yukang Feng, Jianwen Sun, Zizhen Li, Fanrui Zhang, Jiaxin Ai, Zhixiang Wang,
> Yuwei Wu, Tong He, Jiangmiao Pang, Yu Qiao, Yunde Jia, Kaipeng Zhang
>
> Shanghai AI Laboratory, Beijing Institute of Technology

## 🔥 Update

- [2025.06.25] Video download and clip extraction tools for Sekai-Real are now available!
- [2025.06.19] We have released our paper — discussions and feedback are warmly welcome!

## 🧠 Introduction

![pipeline](https://cdn.jsdelivr.net/gh/Lixsp11/sekai-project@0.3.0/static/images/figure2-compressed.png)

**TL;DR** We present Sekai (せかい, “world” in Japanese), a high-quality egocentric video dataset for immersive world exploration and generation. Sekai includes over 5000 hours of YouTube videos and game footage with rich annotations. It features:  

- 📹 Diverse, high-resolution videos (720p)
- 🌍 Coverage of 100+ countries and 750+ cities
- 🚶‍♂️ First-person and 🛸 drone perspectives
- 🕒 Long sequences (≥ 60s) for real-world continuity
- 🏷️ Detailed annotations: location, scene, weather, crowd, captions, and camera trajectories

Sekai supports tasks like video understanding, navigation, and video-audio co-generation.

## 🚀 Quick Start

The Sekai dataset includes **Sekai-Real** from YouTube videos and **Sekai-Game** from video game videos. The camera trajectories for both parts are represented using an intrinsic matrix and per-frame extrinsic matrices, all of which are normalized.

### Sekai-Real

We provide a comprehensive toolchain for [downloading original videos](#) and [extracting video clips](#).

| Split                  | Annotation                                                   | Camera Trajectories                                          | \# Source Videos | \# Samples | Video Duration | Storage Space |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ | ---------------- | ---------- | -------------- | ------------- |
| Sekai-Real-Walking     | [Huggingface](https://huggingface.co/datasets/Lixsp11/Sekai-Project/blob/main/train/sekai-real-walking.csv) | [Huggingface](https://huggingface.co/datasets/Lixsp11/Sekai-Project/blob/main/sekai-real-walking-hq.zip) | 6552             | 299173     | 7986h          | ~10TB         |
| Sekai-Real-Walking-HQ* | [Huggingface](https://huggingface.co/datasets/Lixsp11/Sekai-Project/blob/main/train/sekai-real-walking-hq.csv) | [Huggingface](https://huggingface.co/datasets/Lixsp11/Sekai-Project/blob/main/sekai-real-walking-hq.zip) | 3879             | 18208      | 304h           | ~600GB        |

\* denotes the best-of-the-best videos sampled in consideration of the computational resources for training.

### Sekai-Game

The videos and corresponding camera trajectory files of **Sekai-Game** is hosted on Hugging Face. Click the link to view and download.

| Split              | Annotation                                                   | Videos & Camera Trajectories                                 |
| ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Sekai-Game-Walking | [Huggingface](https://huggingface.co/datasets/Lixsp11/Sekai-Project/blob/main/train/sekai-game-walking.csv) | [part1](https://huggingface.co/datasets/Lixsp11/Sekai-Project/blob/main/sekai-game-walking.zip.part_aa) and [part2](https://huggingface.co/datasets/Lixsp11/Sekai-Project/blob/main/sekai-game-walking.zip.part_ab) |
| Sekai-Game-Drone   | [Huggingface](https://huggingface.co/datasets/Lixsp11/Sekai-Project/blob/main/train/sekai-game-drone.csv) | [here](https://huggingface.co/datasets/Lixsp11/Sekai-Project/blob/main/sekai-game-drone.zip) |

## 📦 Checklist

- [x] Tools for Sekai-Real video download and clip extraction.
- [ ] Modified MegaSam used in Sekai.


## 📄 License

See [license](https://github.com/Lixsp11/sekai-codebase/blob/main/LICENSE).

## 📖 Citation

If you find this project helpful, please consider citing:

```bibtex
@article{li2025sekai,
      title={Sekai: A Video Dataset towards World Exploration}, 
      author={Zhen Li and Chuanhao Li and Xiaofeng Mao and Shaoheng Lin and Ming Li and Shitian Zhao and Zhaopan Xu and Xinyue Li and Yukang Feng and Jianwen Sun and Zizhen Li and Fanrui Zhang and Jiaxin Ai and Zhixiang Wang and Yuwei Wu and Tong He and Jiangmiao Pang and Yu Qiao and Yunde Jia and Kaipeng Zhang},
      journal={arXiv preprint arXiv:2506.15675},
      year={2025}
}
```