import cv2
import numpy as np
from PIL import Image, ImageOps
from progress.bar import IncrementalBar

from craft_generating.Settings import *

widthKAL = height
heightKAL = width

cfg = open('C:/Games/KSP/KSP with expansion/Kerbal Space Program/saves/Display/Ships/VAB/display.craft', 'a')
cfg.write(KAL_begin_actions)


def map_range(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# helper functions
def grayscale(image):
    return ImageOps.grayscale(image)


def resize_image(image):
    return image.resize((widthKAL, heightKAL), Image.NEAREST)  # NEAREST to interpolate into solid pixels


def create_images(number_of_frames=6500):
    bar_im = IncrementalBar('Images creation', max=number_of_frames, suffix='%(percent)d%%')
    image_list = []
    video = cv2.VideoCapture("BadApple.mp4")
    frame_count = 0
    while True:
        ret, image_frame = video.read()
        if ret is False or frame_count > number_of_frames:  # when we reach the end of the video
            break
        image = Image.fromarray(image_frame)
        image = resize_image(image)
        image = grayscale(image)
        image_list.append(image)
        frame_count += 1
        bar_im.next()
        # if frame_count % 100 == 0:
        #     print(f"finish frame {frame_count} out of {number_of_frames}")
    video.release()
    bar_im.finish()
    return image_list


def vals2keyframes(values):
    prev_val = 0
    keys = []
    for i in range(frame_count):
        if i == 0:
            prev_val = 0

        if values[i] < prev_val:
            keys.append(map_range(i, 0, frame_count, 0, 1))

        if values[i] > prev_val:
            keys.append(map_range(i, 0, frame_count, 0, 1))

        if values[i] == prev_val:
            pass

        if i != 0:
            prev_val = values[i]

    return keys


def keys2cfg(keys, pers_id):
    if not keys:
        cfg.write('')
        return False
    else:
        cfg.write('\t\t\t}\n\t\t\tACTION\n\t\t\t{\n\t\t\t\tpersistentId = ' + str(pers_id))
        pers_id += 1
        cfg.write(
            '\n\t\t\t\tmoduleId = 2512051409\n\t\t\t\tpartNickName =\n\t\t\t\trowIndex = 0\n\t\t\t\tactionName = ToggleLightAction\n\t\t\t\tTIMES\n\t\t\t\t{\n'
        )
        for i in range(len(keys)):
            cfg.write(f'\t\t\t\t\ttime = {str(keys[i])}\n')
        cfg.write('\t\t\t\t}\n')


images = create_images(frame_count)

imageArray = np.zeros((frame_count, heightKAL, widthKAL), dtype='int')

for i in range(frame_count):
    imageArray[i] = np.asarray(images[i])

bar_q = IncrementalBar('Quantization of images', max=widthKAL * heightKAL * frame_count, suffix='%(percent)d%%')
for i in range(frame_count):
    for y in range(heightKAL):
        for x in range(widthKAL):
            if imageArray[i][y][x] <= 128:
                imageArray[i][y][x] = 0
            if imageArray[i][y][x] > 128:
                imageArray[i][y][x] = 1
            bar_q.next()
bar_q.finish()


bar = IncrementalBar('Keyframes writing', max=widthKAL * heightKAL, suffix='%(percent)d%%')
persID = 1
for y in range(heightKAL):
    for x in range(widthKAL):
        values = np.zeros(frame_count)
        for frame in range(frame_count):
            values[frame] = imageArray[frame][y][x]
        keys2cfg(vals2keyframes(values), persID)
        persID += 1
        if not np.nonzero(values):
            cfg.write('\n\t\t\t}\n')
        else:
            cfg.write('\n')
        bar.next()
bar.finish()

cfg.write(KAL_end_actions)
cfg.close()
