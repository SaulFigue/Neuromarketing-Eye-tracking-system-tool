# Screen Calibration Process and Data Collection for Personal Training

This project is intended to perform a screen calibration to return the rotation and translation matrices parameters needed for enhancing the accuracy of the DEMO branch. This is a complementary process for Figueroa S. university graduation project.
In addition, this repository can collect enought data information to perform a personal training process with images and annotation data for a single user. In other words you could built a customized gaze-estimation system. Moreover, this project is based on ["Efficiency in Real-Time Webcam Gaze Tracking"](https://arxiv.org/abs/2009.01270) [1]. In addition, the source code implementation is a modification of [pperle
Pascal repository](https://github.com/pperle/gaze-data-collection).

The output of this project is a folder with a CSV file containing the coordinates in pixels for the calibration points and the file name of the webcam captured image. At least 9 calibration images should be used for a decent performance, however is advisable to calibrate with more than 9 points.

## Instructions to run the calibration

1. `pip install -r requirements.txt`
2. Run the camera calibration process by the command: `python camera_calibration.py`, based on [OpenCV method](https://docs.opencv.org/4.5.3/dc/dbb/tutorial_py_calibration.html).
3. Step 2 had recorded a video with the checkboard calibration, comment the `record_video` function and split the video by running the `ffmpeg -i 2023-02-28_15:38:39.mp4 -f image2 frames/video_01-%07d.png` command (for linux system, Colab linux enviroment is an alternative for windows OS).
4. With all the frames splitted in the ```./frames``` folder, run the last command `calibration('./frames', 30, debug=True)`. This will return you a `calibration_matrix.yaml` file.
5. `python main.py --base_path=./data/p00`
6. At this point, a screen display will be shown in front of you. You need to look at each one of this point and press the corresponding arrow key settled in the `Target Orientation` class from ```utils.py``` script. In this case, (w-s-d-a) for (Up-Down-Right-Left). You might match the direction of the "E" letter with the key pressed. 
7. After 9 points, or even more points for better calibration, you can press "q" key to exit the calibration - data collection process.
8. You can visualize your 3D calibration model by running `python visualization.py --base_path=./data/p00`.

## Bibliography

[1] Gudi, A., Li, X., & van Gemert, J. (2020). Efficiency in real-time webcam gaze tracking. In Computer Vision–ECCV 2020 Workshops: Glasgow, UK, August 23–28, 2020, Proceedings, Part I 16 (pp. 529-543). Springer International Publishing.
