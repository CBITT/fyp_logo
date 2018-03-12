import csv
from pathlib import Path
from PIL import Image
import glob


dir_to_check = Path('path/training_set.csv')


set_imgs = []
image_list = []

with open(dir_to_check,'r') as t_set:
    col_reader = csv.DictReader(t_set)
    for row in col_reader:
        image = (row['im_filename'])
        set_imgs.append(image)
#print('\n'.join(set_imgs))


for image in glob.glob('path/flickr_logos_27_dataset_images/*.jpg'):
    im=Image.open(image)
    im_str = im.filename.split('\\')[-1]
    image_list.append(im_str)


checker=[]

for j in set_imgs:
    if j in image_list:
        checker.append('YES')
    else:
        checker.append('NO')

print(checker)




