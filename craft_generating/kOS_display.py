# imports
import pandas as pd
from craft_generating.Tools import *

# data frame creation
df = pd.DataFrame(columns=['id', 'pos', 'pos_in_mtx', 'tag'])
print('Creating data frame done')

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

print('Filling data frame done')

# writing main part of craft file
craft_file.write(kos_craft_begin)  # write first default part to craft file
write_links(craft_file, df)  # write links to lamps
craft_file.write(links_end_KAL_end)  # write end of probe core part
write_kos_lamp(craft_file, df)  # writing lamps
print('Finished')
