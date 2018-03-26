import os
from PIL import Image
import glob
import csv
from pathlib import Path
import pandas as pd
from more_itertools import unique_everseen

"""Create VOC style training csv from flick27 dataset"""

path = 'path/to/images/'
partial_csv = Path('path/to/partial.csv')
original_training_csv = Path('path/to/training_set.csv')
training_csv_cut = Path('path/to/training_cut.csv')
merged_output_repetitive = Path('path/to/training_rep.csv')
merged_output_no_repeats = Path('path/to/training.csv')

if partial_csv.is_file():
    print('partial.csv already created')
else:
    with open(partial_csv,  'w') as myfile:
        writer = csv.writer(myfile)
        writer.writerow(('im_filename', 'width', 'height'))

        for filename in glob.glob(path + '/*.jpg'):
            im=Image.open(filename)
            filename_cut = os.path.basename(im.filename)
            sizes = str(im.size).strip('()')
            width, height = sizes.split()
            writer = csv.writer(myfile)
            writer.writerow((filename_cut,width.strip(','),height))


original = pd.read_csv(original_training_csv)
keep_col = ['im_filename','classname','x_min','y_min','x_max','y_max']
partial_file = original[keep_col]
partial_file.to_csv(training_csv_cut, index=False)

all_images_with_sizes = pd.read_csv(partial_csv)
training_coords_no_sizes = pd.read_csv(training_csv_cut)
merged = all_images_with_sizes.merge(training_coords_no_sizes, on='im_filename')
merged.to_csv(merged_output_repetitive, index=False)


with open(merged_output_repetitive,'r') as f, open(merged_output_no_repeats,'w') as out_file:
    out_file.writelines(unique_everseen(f))