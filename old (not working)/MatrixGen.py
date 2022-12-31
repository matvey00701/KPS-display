import numpy as np
import pandas as pd

from craft_generating.Settings import *

df = pd.DataFrame(columns=['id', 'pos', 'persistentId'])

craft = open('C:/Games/KSP/KSP with expansion/Kerbal Space Program/saves/Display/Ships/VAB/display.craft', 'a')


def to_fixed(num_obj, digits=0):
    return f"{num_obj:.{digits}f}"


def generate_matrix():
    mtx = np.zeros((width, height), dtype=object)

    for x in range(0, width):
        for y in range(0, height):
            mtx[x, y] = (float(to_fixed((grid_step_x * x) - ((width * grid_step_x) // 2), 2)), 20,
                         float(to_fixed((grid_step_y * y) - ((height * grid_step_y) // 2), 2)))
    return mtx


def fill_df():
    px_id = 1
    persistent_id = 1
    for x in range(0, width):
        for y in range(0, height):
            df._set_value(index=px_id, col='id', value=px_id)
            df._set_value(index=px_id, col='pos', value=matrix[x, y])
            df._set_value(index=px_id, col='persistentId', value=persistent_id)
            px_id += 1
            persistent_id += 1


def create_pixel(px_id, pixel_pos, persistent_id):
    craft.write('\nPART\n{\n')
    craft.write('\tpart = spotLight2.v2_')
    craft.write(str(px_id + 1))
    craft.write('\n\tpartName = Part')
    craft.write('\n\tpersistentId = ')
    craft.write(str(persistent_id))
    craft.write('\n\tpos = ')
    craft.write(str(pixel_pos[0]))
    craft.write(',')
    craft.write(str(pixel_pos[1]))
    craft.write(',')
    craft.write(str(pixel_pos[2]))
    craft.write('\n\tattPos = ')
    craft.write(str(pixel_pos[0]))
    craft.write(',')
    craft.write(str(pixel_pos[1]))
    craft.write(',')
    craft.write(str(pixel_pos[2]))
    craft.write('\n\tattPos0 = ')
    craft.write(str(pixel_pos[0]))
    craft.write(',')
    craft.write(str(pixel_pos[1]))
    craft.write(',')
    craft.write(str(pixel_pos[2]))


matrix = generate_matrix()
fill_df()
craft.write(craft_begin)
for i in range(1, (width * height) + 1):
    craft.write('\n\tlink = spotLight2.v2_')
    craft.write(str(i))
craft.write(links_end_probecore_end)

for i in range(0, len(df)):
    pos = df.iloc[i]['pos']
    persID = df.iloc[i]['persistentId']
    create_pixel(i, pos, persID)
    craft.write(lamp_main)

craft.close()
