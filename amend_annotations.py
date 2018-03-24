import os
from PIL import Image
import glob
import csv
from pathlib import Path

size_list = []
path = 'path/to/images/'
partial_csv = Path('path/to/partial.csv')



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

