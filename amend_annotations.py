from PIL import Image
import glob
import csv
from pathlib import Path

size_list = []
path = 'C:/Users/BangoCs/Desktop/MyDocs Offline/year4/semester 2/FYP/datasets/flickr_logos_27_dataset/flickr_logos_27_dataset_images/'
partial_csv = Path('C:/Users/BangoCs/Desktop/MyDocs Offline/year4/semester 2/FYP/datasets/flickr_logos_27_dataset/partial.csv')


if partial_csv.is_file():
    print('partial.csv already created')
else:

    with open(partial_csv,  'w') as myfile:
        writer = csv.writer(myfile)
        writer.writerow(('im_filename', 'width', 'height'))

        for filename in glob.glob(path + '/*.jpg'):
            im=Image.open(filename)
            filename_cut = filename.strip(path).strip('\\') + 'pg'

            sizes = str(im.size).strip('()')

            width, height = sizes.split()

            writer = csv.writer(myfile)

            writer.writerow((filename_cut,width.strip(','),height))

