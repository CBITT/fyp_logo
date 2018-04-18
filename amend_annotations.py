import os
from PIL import Image
import glob
import csv
from pathlib import Path
import pandas as pd
from more_itertools import unique_everseen

"""Create VOC style training csv from flick27 dataset"""

path_to_images = 'C:/path/to/flickr_logos_27_dataset/flickr_logos_27_dataset_images/'
partial_csv = Path('C://path/to/data/bin/partial.csv')
original_training_csv = Path('C:/path/to/data/bin/training_set.csv')
training_csv_cut = Path('C:/path/to/data/bin/training_cut.csv')
test_csv_no_sizes = Path('C://path/to/data/bin/test_set.csv')
merged_training_repetitive = Path('C:/path/to/data/bin/training_rep.csv')
merged_training_no_repeats = Path('C:/path/to/data/training.csv')
merged_test_repetitive = Path('C:/path/to/data/bin/test_rep.csv')
merged_test_no_repeats = Path('C:/path/to/data/test.csv')

#write partial_csv to contain all image sizes with corresponding im_filenames
try:
    if partial_csv.is_file():
        print('partial.csv already created')
    else:
        with open(partial_csv,  'w') as part:
            writer = csv.writer(part)
            writer.writerow(('im_filename', 'width', 'height'))

            for im_filename in glob.glob(path_to_images + '/*.jpg'):
                im = Image.open(im_filename)
                filename_cut = os.path.basename(im.filename)
                sizes = str(im.size).strip('()')
                width, height = sizes.split()
                writer = csv.writer(part)
                writer.writerow((filename_cut,width.strip(','),height))
except:
    print('Error in creating partial csv with all images and corresponding sizes.')
#remove unnecessary column, subclass_of_a_class
try:
    original = pd.read_csv(original_training_csv)
    keep = ['im_filename','classname','xmin','ymin','xmax','ymax']
    partial_file = original[keep]
    partial_file.to_csv(training_csv_cut, index=False)
except:
    print('Couldn\'t remove unnecessary column.')

#merge truncated csv file with all sizes
try:
    all_images_with_sizes = pd.read_csv(partial_csv)
    training_coords_no_sizes = pd.read_csv(training_csv_cut)
    merged_training = all_images_with_sizes.merge(training_coords_no_sizes, on='im_filename')
    merged_training.to_csv(merged_training_repetitive, index=False)

#add test file to merging
    test_csv = pd.read_csv(test_csv_no_sizes)
    merged_test = all_images_with_sizes.merge(test_csv, on='im_filename')
    merged_test.to_csv(merged_test_repetitive, index=False)

#remove replicates
    with open(merged_training_repetitive,'r') as x, open(merged_training_no_repeats,'w') as ready_training:
        ready_training.writelines(unique_everseen(x))
        print('training.csv created successfully')
    with open(merged_test_repetitive,'r') as y, open(merged_test_no_repeats,'w') as ready_test:
        ready_test.writelines(unique_everseen(y))
        print('test.csv created successfully')
except:
    print('Error in merging.')