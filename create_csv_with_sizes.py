from pathlib import Path
import pandas as pd

original_csv = Path('path/training_set.csv')
partial_csv = Path('path/data/partial_set.csv')
new_csv = Path('path/data/training_set.csv')

original = pd.read_csv(original_csv)
keep_col = ['im_filename','classname','x_min','y_min','x_max','y_max']
partial_file = original[keep_col]
partial_file.to_csv(partial_csv, index=False)

new = pd.read_csv(partial_csv)
#TODO: insert correct values
new['width'] = 1
new['height'] = 2
cols = new.columns.tolist()


cols = cols[:1] + [cols[-2]] + [cols[-1]] + cols[1:6]
new = new[cols]
new.to_csv(new_csv, index=False)

