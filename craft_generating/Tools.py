import cv2
import numpy as np
from PIL import Image, ImageOps
from progress.bar import IncrementalBar

from Settings import *


def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def to_fixed(num_obj, digits=0):
    return f"{num_obj:.{digits}f}"


def generate_pos_matrix(size, step_x, step_y):
    mtx = np.zeros((size[0], size[1]), dtype=object)
    iteration = 0
    for x in range(0, size[0]):
        for y in range(0, size[1]):
            mtx[x, y] = (float(to_fixed((step_x * x) - ((size[0] * step_x) // 2), 2)),
                         20,
                         float(to_fixed((step_y * y) - ((size[1] * step_y) // 2), 2)),
                         iteration + 1)
            iteration += 1
    return mtx


def grayscale(image):
    return ImageOps.grayscale(image)


def resize_image(image, width, height):
    return image.resize((width, height), Image.NEAREST)


def swap_rb(image):
    r, g, b = image.split()
    return Image.merge('RGB', (b, g, r))


def optimize(v_arr, quantize_depth=4):
    for i in range(3):
        values = []
        for j in range(len(v_arr)):
            values.append(v_arr[j][0][i])

        delta = 255 / quantize_depth
        for e, element in enumerate(values):
            values[e] = delta * np.floor((element / delta) + 0.5)

        for j in range(len(v_arr)):
            v_arr[j][0][i] = values[j]

    keys = []
    for i in range(3):
        vals = []
        for j, frame in enumerate(v_arr):
            if j == 0:
                pr = 0
            else:
                pr = v_arr[j - 1][0][i]
            if j != len(v_arr) - 1:
                ne = v_arr[j + 1][0][i]
            else:
                ne = 0

            current = frame[0][i]

            if pr != current or ne != current:
                vals.append(
                    [
                        to_fixed(map_range(current, 0, 255, 0, 1), 4),
                        to_fixed(frame[1], 4)
                    ]
                )
        keys.append(vals)

    return keys


def transpose(v_arr):
    keys = []
    for i in range(3):
        vals = []
        for frame in v_arr:
            vals.append([
                to_fixed(map_range(frame[0][i], 0, 255, 0, 1), 4),
                to_fixed(frame[1], 4)
            ])
        keys.append(vals)
    return keys


def create_images(video_path, number_of_frames=6500):
    bar_im = IncrementalBar('Images creation', max=number_of_frames+1, suffix='%(index)d/%(max)d')
    image_list = []
    video = cv2.VideoCapture(video_path)
    f_count = 0
    while True:
        ret, image_frame = video.read()
        if ret is False or f_count > number_of_frames:  # when we reach the end of the video
            break
        image = Image.fromarray(cv2.rotate(image_frame, cv2.ROTATE_90_COUNTERCLOCKWISE))
        # image = Image.fromarray(image_frame)
        image = resize_image(image, height, width)
        image = grayscale(image)
        image_list.append(image)
        f_count += 1
        bar_im.next()
        # print(f_count)
    video.release()
    bar_im.finish()

    image_arr = np.zeros((frame_count, width, height))
    for i in range(frame_count):
        image_arr[i] = np.asarray(image_list[i])

    for img in image_arr:
        for y in range(height):
            for x in range(width):
                if img[x, y] <= 128:
                    img[x, y] = 0
                if img[x, y] >= 128:
                    img[x, y] = 1

    return image_arr


def create_color_images(video_path, number_of_frames=6500):
    bar_im = IncrementalBar('Images creation', max=number_of_frames+1, suffix='%(index)d/%(max)d')
    image_list = []
    video = cv2.VideoCapture(video_path)
    f_count = 0

    while True:
        ret, image_frame = video.read()
        if ret is False or f_count > number_of_frames:
            break
        image_frame = cv2.flip(image_frame, 1)
        image = Image.fromarray(image_frame)
        image = resize_image(image, width, height)
        image = swap_rb(image)
        image_list.append(image)
        f_count += 1
        bar_im.next()

    video.release()
    bar_im.finish()
    return image_list


def write_links(cf, data_frame):
    for i in range(len(data_frame)):
        cf.write(f'\n\tlink = spotLight2.v2_{data_frame.iloc[i]["id"]}')


def write_lamp(cf, data_frame, color):
    for i in range(len(data_frame)):
        cf.write('\nPART\n{\n\tpart = spotLight2.v2_')
        cf.write(str(data_frame.iloc[i]['id']))
        cf.write(f'\n\tpartName = Part\n\tpersistentId = {data_frame.iloc[i]["id"]}')
        cf.write(
            f'\n\tpos = {data_frame.iloc[i]["pos"][0]},{data_frame.iloc[i]["pos"][1]},{data_frame.iloc[i]["pos"][2]}'
        )
        cf.write(
            f'\n\tattPos = {data_frame.iloc[i]["pos"][0]},{data_frame.iloc[i]["pos"][1]},{data_frame.iloc[i]["pos"][2]}'
        )
        cf.write(
            f'\n\tattPos0 = {data_frame.iloc[i]["pos"][0]},{data_frame.iloc[i]["pos"][1]},{data_frame.iloc[i]["pos"][2]}'
        )
        if color:
            cf.write(lamp_main_color)
        else:
            cf.write(lamp_main_mono)


def write_kos_lamp(cf, data_frame):
    for i in range(len(data_frame)):
        cf.write('\nPART\n{\n\tpart = spotLight2.v2_')
        cf.write(str(data_frame.iloc[i]['id']))
        cf.write(f'\n\tpartName = Part\n\tpersistentId = {data_frame.iloc[i]["id"]}')
        cf.write(
            f'\n\tpos = {data_frame.iloc[i]["pos"][0]},{data_frame.iloc[i]["pos"][1]},{data_frame.iloc[i]["pos"][2]}'
        )
        cf.write(
            f'\n\tattPos = {data_frame.iloc[i]["pos"][0]},{data_frame.iloc[i]["pos"][1]},{data_frame.iloc[i]["pos"][2]}'
        )
        cf.write(
            f'\n\tattPos0 = {data_frame.iloc[i]["pos"][0]},{data_frame.iloc[i]["pos"][1]},{data_frame.iloc[i]["pos"][2]}'
        )
        cf.write(lamp_main_1)
        cf.write(f'{data_frame.iloc[i]["pos_in_mtx"][0]}_{data_frame.iloc[i]["pos_in_mtx"][1]}')
        cf.write(lamp_main_2)
