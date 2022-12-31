# to launch the code you need to install required packages
# go to terminal then 'cd' to project folder
# then type 'pip install -r requirements.txt'
# 'cd' to 'craft_generating' folder and execute color.py or monochrome.py file

# resolution settings
horizontal_resolution = 25
aspect_ratio = 4/3

# project settings
path_to_video = '//BadApple.mp4'  # path to video
frame_count = 100  # how many frames will be written?

path_to_craft = 'C:/Games/KSP/KSP with expansion/Kerbal Space Program/saves/Color/Ships/VAB/'  # path to VAB/SPH folder
craft_name = 'display_mono'  # craft file name
# if you don't know how many frames in your video
# go to python console and type these commands:
# import cv2
# cap = cv2.VideoCapture('path/to/your/video.mp4')
# int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# and you will get the frame count


# ---------- ↓ Do not touch this ↓ -----------
import os

grid_step_x = 0.42
grid_step_y = grid_step_x * 0.706
px_aspect_ratio = grid_step_x / grid_step_y

height = int((horizontal_resolution / aspect_ratio) / 0.706)
width = horizontal_resolution

print(f'{width}×{height}')
print(os.getcwd())

# width = 25   # 24
# height = 14  # 18
#
# grid_step_x = 0.42
# grid_step_y = 0.42

craft_file = open(os.path.join(path_to_craft, craft_name + '.craft'), 'a')
lamp_main_color = open(os.getcwd() + '/emiting_parts/Illuinator_Mk2/RGB/lamp_main_for_color.txt', 'r').read()
lamp_main_mono = open(os.getcwd() + '/emiting_parts/Illuinator_Mk2/monochrome/lamp_main_for_mono.txt', 'r').read()
lamp_main_1 = open(os.getcwd() + '/emiting_parts/Illuinator_Mk2/kOS/lamp_main_1.txt', 'r').read()
lamp_main_2 = open(os.getcwd() + '/emiting_parts/Illuinator_Mk2/kOS/lamp_main_2.txt', 'r').read()
craft_begin = open(os.getcwd() + '/general_cfg_parts/01_craft_begin.txt', 'r').read()
links_end_probecore_end = open(os.getcwd() + '/general_cfg_parts/02_links_end_probecore_end.txt', 'r').read()
KAL_begin_actions = open(os.getcwd() + '/general_cfg_parts/03_KAL_begin_actions.txt', 'r').read()
KAL_end_actions = open(os.getcwd() + '/general_cfg_parts/05_KAL_end_actions.txt', 'r').read()
R = open(os.getcwd() + '/emiting_parts/Illuinator_Mk2/RGB/R.txt', 'r').read()
G = open(os.getcwd() + '/emiting_parts/Illuinator_Mk2/RGB/G.txt', 'r').read()
B = open(os.getcwd() + '/emiting_parts/Illuinator_Mk2/RGB/B.txt', 'r').read()
KAL_begin_axis = open(os.getcwd() + '/general_cfg_parts/04_KAL_begin_axis.txt', 'r').read()
KAL_end_axis = open(os.getcwd() + '/general_cfg_parts/06_KAL_end_axis.txt', 'r').read()

kos_craft_begin = open(os.getcwd() + '/general_cfg_parts/07_kOS_craft_begin.txt', 'r').read()
links_end_KAL_end = open(os.getcwd() + '/general_cfg_parts/08_kOS_links_end_KAL_end.txt', 'r').read()

frame_count = frame_count - 1
