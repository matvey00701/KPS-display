# imports
import pandas as pd

from Tools import *

# data frame creation
df = pd.DataFrame(columns=['id', 'pos', 'pos_in_mtx', 'v_arr'])

# matrix with indexes and coordinates
position_matrix = generate_pos_matrix((width, height), grid_step_x, grid_step_y)

# filling the data frame
for x in range(0, width):
    for y in range(0, height):
        df = df.append({
            'id': position_matrix[x, y][3],
            'pos': (position_matrix[x, y][:3]),
            'pos_in_mtx': (x, y)
        }, ignore_index=True)

# creating array of images from video
frames = create_color_images(path_to_video, frame_count)

# creating v_arr
arr_bar = IncrementalBar(
    'Extracting color values',
    max=len(df),
    suffix='%(index)d/%(max)d [%(elapsed)d / %(eta_td)s]'
)
for i in range(len(df)):
    v_arr = []
    v = []
    for t, frame in enumerate(frames):
        v_arr.append(
            [
                list(frame.getpixel((df.iloc[i]['pos_in_mtx'][0], df.iloc[i]['pos_in_mtx'][1]))),
                map_range(t, 0, frame_count, 0, 1)
            ]
        )

    df.at[i, 'v_arr'] = optimize(v_arr, 16)
    arr_bar.next()
arr_bar.finish()

# writing to file
craft_file.write(craft_begin)  # write first default part to craft file
write_links(craft_file, df)  # write links to lamps
craft_file.write(links_end_probecore_end)  # write end of probe core part
write_lamp(craft_file, df, color=True)  # writing lamps

# writing controller

wr_bar = IncrementalBar('writing craft file', max=len(df), suffix='%(percent)d%%')
craft_file.write(KAL_begin_axis)

for i, row in enumerate(df.values):
    px_id, pos, pos_in_mtx, colors = row
    for j in range(3):

        craft_file.write(
            '\t\t\tAXIS\n' +
            '\t\t\t{\n' +
            f'\t\t\t\tpersistentId = {px_id}'
        )
        if j == 0:
            craft_file.write(R)
        if j == 1:
            craft_file.write(G)
        if j == 2:
            craft_file.write(B)

        for value in colors[j]:
            craft_file.write(f'\t\t\t\t\tkey = {value[1]} {value[0]} 0 0\n')

        craft_file.write('\t\t\t\t}\n\t\t\t}\n')

    wr_bar.next()
wr_bar.finish()
craft_file.write(KAL_end_axis)
