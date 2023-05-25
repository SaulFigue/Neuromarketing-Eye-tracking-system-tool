# Eye-tracking system DEMO

This repository provide an implementation code to replicate Figueroa S. university graduation project. This project is based on ["Efficiency in Real-Time Webcam Gaze Tracking"](https://arxiv.org/abs/2009.01270) [1]. In addition, the source code implementation is a modification of [pperle
Pascal repository](https://github.com/pperle/gaze-tracking) where an evaluation of a monocular eye tracking set-up work is performed.

### Python Environment

- Python version: 3.7.1
- Conda environment used
- 
## Updates
In this section, every update and important information about changes or improvements of this implementation will be posted here:

25/05/2023 - Demo system is provided with a limitation in the accuracy. An screen calibration process is needed.

Nothing new...

## Pretrained Models
To run the demo, you will need to download the respective Model_pxx.ckpt files: VGG-16 (Benchamark_p00.ckpt) or ResNet-50 (ResNet_p00.ckpt)model. Please download the [pretrained_models_VGG-16](https://drive.google.com/file/d/1woC68FJ026u-ujmA0NgMOsJyTryrKfhy/view?usp=sharing) or [pretrained_models_ResNet-50](https://drive.google.com/file/d/1r3WhLnI746uahDJBx1Wqm9t0LkVr-162/view?usp=sharing).


## Instruction to run the DEMO correctly

1. `pip install -r requirements.txt`
2. Run the camera calibration process by the command: `python camera_calibration.py`, based on [OpenCV method](https://docs.opencv.org/4.5.3/dc/dbb/tutorial_py_calibration.html).
2.1. Step 2 had recorded a video with the checkboard calibration, comment the `record_video` function and split the video by running the `ffmpeg -i 2023-02-28_15:38:39.mp4 -f image2 frames/video_01-%07d.png` command (for linux system, Colab linux enviroment is an alternative for windows OS).
2.2 With all the frames splitted in the ```./frames``` folder, run the last command `calibration('./frames', 30, debug=True)`. This will return you a `calibration_matrix.yaml` file.
3. Now you can run the DEMO, by using the command: `python main.py --visualize_3d=True --visualize_preprocessing=True --calibration_matrix_path=./calibration_matrix.yaml --model_path=./ResNet_p00.ckpt`. Thi will display a "red laser pointer" on the screen, preprocessed images (normalized face and eyes) and the head, screen, and the gaze vector in a 3D scene.

## Bibliography

[1] Gudi, A., Li, X., & van Gemert, J. (2020). Efficiency in real-time webcam gaze tracking. In Computer Vision–ECCV 2020 Workshops: Glasgow, UK, August 23–28, 2020, Proceedings, Part I 16 (pp. 529-543). Springer International Publishing.
