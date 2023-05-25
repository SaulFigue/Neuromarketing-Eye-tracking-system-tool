import random
import sys
import time
from datetime import datetime
from enum import Enum

import cv2
import numpy as np
from typing import Tuple, Union

from webcam import WebcamSource


def get_monitor_dimensions() -> Union[Tuple[Tuple[int, int], Tuple[int, int]], Tuple[None, None]]:
    """
    Get monitor dimension by using tkinter library
    :return: tuple of monitor width and height in mm and pixels or None
    """

    try:
        import tkinter as tk

        root = tk.Tk()
        root.withdraw()

        # h_mm = 203,  w_mm = 361
        h_mm = root.winfo_screenmmheight()
        w_mm = root.winfo_screenmmwidth()

        # h_px = 768,  w_px = 1366
        h_pixels = root.winfo_screenheight() 
        w_pixels = root.winfo_screenwidth()

        return (w_mm, h_mm), (w_pixels, h_pixels)

    except ModuleNotFoundError:
        return None, None

FONT = cv2.FONT_HERSHEY_SIMPLEX
TEXT_SCALE = 0.5
TEXT_THICKNESS = 2


class TargetOrientation(Enum):
    """
    Key arrows set (w-s-a-d)
    In the 7-bit ASCII character set (lowercase)
    Make sure to have the 'CapsLk' off
    """

    # /////////////////////
    UP = 119    # W
    DOWN = 115  # S
    LEFT = 97   # A
    RIGHT = 100 # D
    # /////////////////////

def create_image(monitor_pixels: Tuple[int, int], center=(0, 0), circle_scale=1., orientation=TargetOrientation.RIGHT, target='E') -> Tuple[np.ndarray, float, bool]:
    """
    Create image to display on screen.

    :param monitor_pixels: monitor dimensions in pixels
    :param center: center of the circle and the text
    :param circle_scale: scale of the circle
    :param orientation: orientation of the target
    :param target: char to write on image
    :return: created image, new smaller circle_scale and bool that indicated if it is th last frame in the animation
    """

    width, height = monitor_pixels

    if orientation == TargetOrientation.LEFT or orientation == TargetOrientation.RIGHT:
        img = np.zeros((height, width, 3), np.float32)

        if orientation == TargetOrientation.LEFT:
            center = (width - center[0], center[1])

        end_animation_loop = write_text_on_image(center, circle_scale, img, target)

        if orientation == TargetOrientation.LEFT:
            img = cv2.flip(img, 1)
    else:  # TargetOrientation.UP or TargetOrientation.DOWN
        img = np.zeros((width, height, 3), np.float32)
        center = (center[1], center[0])

        if orientation == TargetOrientation.UP:
            center = (height - center[0], center[1])

        end_animation_loop = write_text_on_image(center, circle_scale, img, target)

        if orientation == TargetOrientation.UP:
            img = cv2.flip(img, 1)

        img = img.transpose((1, 0, 2))

    return img / 255, circle_scale * 0.9, end_animation_loop


def write_text_on_image(center: Tuple[int, int], circle_scale: float, img: np.ndarray, target: str):
    """
    Write target on image and check if last frame of the animation.

    :param center: center of the circle and the text
    :param circle_scale: scale of the circle
    :param img: image to write data on
    :param target: char to write
    :return: True if last frame of the animation
    """

    text_size, _ = cv2.getTextSize(target, FONT, TEXT_SCALE, TEXT_THICKNESS)
    cv2.circle(img, center, int(text_size[0] * 5 * circle_scale), (32, 32, 32), -1)
    text_origin = (center[0] - text_size[0] // 2, center[1] + text_size[1] // 2)

    end_animation_loop = circle_scale < random.uniform(0.1, 0.5)
    if not end_animation_loop:
        cv2.putText(img, target, text_origin, FONT, TEXT_SCALE, (17, 112, 170), TEXT_THICKNESS, cv2.LINE_AA)
    else:
        cv2.putText(img, target, text_origin, FONT, TEXT_SCALE, (252, 125, 11), TEXT_THICKNESS, cv2.LINE_AA)

    return end_animation_loop


def get_random_position_on_screen(monitor_pixels: Tuple[int, int]) -> Tuple[int, int]:
    """
    Get random valid position on monitor.

    :param monitor_pixels: monitor dimensions in pixels
    :return: tuple of random valid x and y coordinated on monitor
    """

    return int(random.uniform(0, 1) * monitor_pixels[0]), int(random.uniform(0, 1) * monitor_pixels[1])


def show_point_on_screen(window_name: str, base_path: str, monitor_pixels: Tuple[int, int], source: WebcamSource) -> Tuple[str, Tuple[int, int], float]:
    """
    Show one target on screen, full animation cycle. Return collected data if data is valid

    :param window_name: name of the window to draw on
    :param base_path: path where to save the image to
    :param monitor_pixels: monitor dimensions in pixels
    :param source: webcam source
    :return: collected data otherwise None
    """
    
    circle_scale = 1.
    center = get_random_position_on_screen(monitor_pixels)
    end_animation_loop = False
    orientation = random.choice(list(TargetOrientation))

    file_name = None
    time_till_capture = None

    while not end_animation_loop:
        image, circle_scale, end_animation_loop = create_image(monitor_pixels, center, circle_scale, orientation)
        cv2.imshow(window_name, image)

        for _ in range(10):  # workaround to not speed up the animation when buttons are pressed
            if cv2.waitKey(50) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                sys.exit()

    if end_animation_loop:
        file_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # print(file_name)
        start_time_color_change = time.time()
        # print('time_till_capture = '+str(time.time())+' - '+str(start_time_color_change))

        while time.time() - start_time_color_change < 0.5:
            if cv2.waitKey(42) & 0xFF == orientation.value:
                source.clear_frame_buffer()
                cv2.imwrite(f'{base_path}/{file_name}.jpg', next(source))
                time_till_capture = time.time() - start_time_color_change
                break

    cv2.imshow(window_name, np.zeros((monitor_pixels[1], monitor_pixels[0], 3), np.float32))
    cv2.waitKey(500)

    return f'{file_name}.jpg', center, time_till_capture
