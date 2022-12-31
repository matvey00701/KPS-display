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
frames = create_images(path_to_video, frame_count)

# writing keyframes for each pixel in data frame
arr_bar = IncrementalBar(
    'Extracting pixel values',
    max=len(df),
    suffix='%(index)d/%(max)d [%(elapsed)d / %(eta_td)s]'
)
for i in range(len(df)):

    # creating list of values for current pixel
    values = []
    for frame in frames:
        coord_current = df.iloc[i]['pos_in_mtx']

        values.append(frame[coord_current[0], coord_current[1]])

    # creating list of keyframes for current pixel
    # writing time of moment of value change
    v_arr = []
    previous_value = 0
    for j, value in enumerate(values):
        if j == 0:
            previous_value = 0
        if value < previous_value:
            v_arr.append(map_range(j, 0, frame_count, 0, 1))
        if value > previous_value:
            v_arr.append(map_range(j, 0, frame_count, 0, 1))
        if value == previous_value:
            pass
        if j != 0:
            previous_value = value

    # writing list of keyframes to data frame
    df.at[i, 'v_arr'] = v_arr
    arr_bar.next()
arr_bar.finish()

# writing main part of craft file
craft_file.write(craft_begin)  # write first default part to craft file
write_links(craft_file, df)  # write links to lamps
craft_file.write(links_end_probecore_end)  # write end of probecore part
write_lamp(craft_file, df, color=False)  # writing lamps

# writing controller
wr_bar = IncrementalBar('writing craft file', max=len(df), suffix='%(percent)d%%')
craft_file.write(KAL_begin_actions)
for i in range(len(df)):
    craft_file.write('\t\t\tACTION\n\t\t\t{\n\t\t\t\tpersistentId = ' + str(df.iloc[i]['id']))
    craft_file.write(
        '\n\t\t\t\tmoduleId = 2512051409\n' +
        '\t\t\t\tpartNickName =\n' +
        '\t\t\t\trowIndex = 0\n' +
        '\t\t\t\tactionName = ToggleLightAction\n' +
        '\t\t\t\tTIMES\n' +
        '\t\t\t\t{\n'
    )
    for value in df.iloc[i]['v_arr']:
        craft_file.write(f'\t\t\t\t\ttime = {str(to_fixed(value, 4))}\n')
    craft_file.write('\t\t\t\t}\n\t\t\t}\n')
    wr_bar.next()
wr_bar.finish()

craft_file.write(KAL_end_actions)
