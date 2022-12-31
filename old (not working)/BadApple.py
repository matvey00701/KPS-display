import numpy as np
import pandas as pd

heightRes = 18

height = int(heightRes * 1.8888)
width = heightRes
gridStepX = 0.42
gridStepY = gridStepX * 0.706

initialPersistantId = 1

engineCfgfile = open('../craft_generating/emiting_parts/Illuinator_Mk2/RGB/lamp_main_for_color.txt', 'r')
engineCfg = engineCfgfile.read()

initialfile = open('../craft_generating/general_cfg_parts/01_craft_begin.txt', 'r')
initial = initialfile.read()

initial2file = open('../craft_generating/general_cfg_parts/02_links_end_probecore_end.txt', 'r')
initial2 = initial2file.read()

KALinitial1file = open('../craft_generating/general_cfg_parts/03_KAL_begin_actions.txt', 'r')
KALinitial1 = KALinitial1file.read()

KALinitial2file = open('../craft_generating/general_cfg_parts/05_KAL_end_actions.txt', 'r')
KALinitial2 = KALinitial2file.read()

frameCount = 6572