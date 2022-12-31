import cv2
import numpy as np
from PIL import Image
from progress.bar import IncrementalBar

from craft_generating.Settings import *

widthKAL = height
heightKAL = width

# frames = 2518

cfg = open('C:\Games\KSP\KSP with expansion\Kerbal Space Program\saves\Display\Ships\VAB\display.craft', 'a')
cfg.write(KAL_initial3)


def resize_image(image):
    return image.resize((widthKAL, heightKAL), Image.NEAREST)  # NEAREST to interpolate into solid pixels


def swap_rb(image):
    r, g, b = image.split()
    return Image.merge('RGB', (b, g, r))


def quantize(image):
    return image.quantize(8)


def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def map_range_int(x, in_min, in_max, out_min, out_max):
    return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def create_images(number_of_frames=2518):
    bar_im = IncrementalBar('Images creation', max=number_of_frames, suffix='%(percent)d%%')
    image_list = []
    video = cv2.VideoCapture("DragonMaid.mp4")
    frame_count = 0
    while True:
        ret, image_frame = video.read()
        if ret == False or frame_count > number_of_frames:  # when we reach the end of the video
            break
        image = Image.fromarray(image_frame)
        image = resize_image(image)
        image = swap_rb(image)
        image = quantize(image)
        image_list.append(image)
        frame_count += 1
        bar_im.next()
        # if frame_count % 100 == 0:
        #     print(f"finish frame {frame_count} out of {number_of_frames}")
    video.release()
    bar_im.finish()
    return image_list



def write_key(frame, value):
    cfg.write('\n\t\t\t\t\tkey = ')
    cfg.write(str(map_range(frame, 0, frameCount, 0, 1)))
    cfg.write(' ')
    cfg.write(str(map_range(value, 0, 255, 0, 1)))
    cfg.write(' 0 0')


def write_lamp(x, y, persID):
    values = np.zeros((frameCount, 3))
    for frame in range(frameCount):
        values[frame] = images[frame].getpixel((x, y))
    for i in range(3):
        if i == 0:
            cfg.write('\t\t\tAXIS\n')
            cfg.write('\t\t\t{\n')
            cfg.write('\t\t\t\tpersistentId = ')
            cfg.write(str(persID))
            cfg.write(KALR)
            prev = 0
            for frame in range(frameCount):
                if frame == (frameCount - 1):
                    next_val = 0
                else:
                    next_val = values[frame + 1]
                if frame == 0: prev = 0
                if (prev < values[frame][0]-1).any() or (prev > values[frame][0]+1).any():
                    write_key(frame, values[frame][0])
                elif (next_val < values[frame][0]-1).any() or (next_val > values[frame][0]+1).any():
                    write_key(frame, values[frame][0])
                else:
                    pass
                if frame != 0: prev = values[frame][0]
            cfg.write('\n\t\t\t\t}\n')
            cfg.write('\t\t\t}\n')
        elif i == 1:
            cfg.write('\t\t\tAXIS\n')
            cfg.write('\t\t\t{\n')
            cfg.write('\t\t\t\tpersistentId = ')
            cfg.write(str(persID))
            cfg.write(KALG)
            prev = 0
            for frame in range(frameCount):
                if frame == (frameCount - 1):
                    next_val = 0
                else:
                    next_val = values[frame + 1]
                if frame == 0: prev = 0
                if (prev < values[frame][0] - 1).any() or (prev > values[frame][0] + 1).any():
                    write_key(frame, values[frame][0])
                elif (next_val < values[frame][0] - 1).any() or (next_val > values[frame][0] + 1).any():
                    write_key(frame, values[frame][0])
                else:
                    pass
                if frame != 0: prev = values[frame][1]
            cfg.write('\n\t\t\t\t}\n')
            cfg.write('\t\t\t}\n')
        elif i == 2:
            cfg.write('\t\t\tAXIS\n')
            cfg.write('\t\t\t{\n')
            cfg.write('\t\t\t\tpersistentId = ')
            cfg.write(str(persID))
            cfg.write(KALB)
            prev = 0
            for frame in range(frameCount):
                if frame == (frameCount - 1):
                    next_val = 0
                else:
                    next_val = values[frame + 1]
                if frame == 0: prev = 0
                if (prev < values[frame][0] - 1).any() or (prev > values[frame][0] + 1).any():
                    write_key(frame, values[frame][0])
                elif (next_val < values[frame][0] - 1).any() or (next_val > values[frame][0] + 1).any():
                    write_key(frame, values[frame][0])
                else:
                    pass
                if frame != 0: prev = values[frame][2]
            cfg.write('\n\t\t\t\t}\n')
            cfg.write('\t\t\t}\n')


images = create_images(frameCount)

# plt.imshow(images[frameCount])
# plt.show()

# values = np.zeros(frameCount)
# for frame in range(frameCount):
#     pixel = images[frame].getpixel((5, 7))
#     values[frame] = pixel[0]
#
# prev = 0
# new_val = []
# for frame in range(frameCount):
#     if frame == (len(values) - 1):
#         next_val = 0
#     else: next_val = values[frame+1]
#     if frame == 0: prev = 0
#     if prev < values[frame]-1 or prev > values[frame]+1:
#         new_val.append(values[frame])
#     if next_val < values[frame]-1 or next_val > values[frame]+1:
#         new_val.append(values[frame])
#     else:
#         pass
#     print(f'prev:{prev}, current:{values[frame]}, next:{next_val}')
#     if frame != 0: prev = values[frame]
#
#
# plt.plot(new_val)
# plt.show()
# for frame in range(frameCount):
#     write_key(frame, values[frame])

# print(values)

persID = 1
bar = IncrementalBar('Keyframes writing', max=widthKAL*heightKAL, suffix='%(percent)d%%')
for y in range(heightKAL):
    for x in range(widthKAL):
        write_lamp(x, y, persID)
        persID += 1
        bar.next()
bar.finish()

cfg.write(KAL_initial4)
cfg.close()

print('\ndisplay.craft created!')

# plt.imshow(images[frames])
# plt.plot(values)
# plt.show()
