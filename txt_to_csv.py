import csv
from pathlib import Path

training_set = Path('C:/Users/BangoCs/Desktop/MyDocs Offline/year4/semester 2/FYP/datasets/flickr_logos_27_dataset/training_set.csv')
if training_set.is_file():
    print('training_set.csv already created')
else:
    with open('C:/Users/BangoCs/Desktop/MyDocs Offline/year4/semester 2/FYP/datasets/flickr_logos_27_dataset/flickr_logos_27_dataset_training_set_annotation.txt',
              'r') as training_as_txt_file:
       separated = (line.strip() for line in training_as_txt_file)
       lines = (line.split(" ") for line in separated if line)
       with open('C:/Users/BangoCs/Desktop/MyDocs Offline/year4/semester 2/FYP/datasets/flickr_logos_27_dataset/training_set.csv', 'w') as training_set:
            writer = csv.writer(training_set)
            writer.writerow(('im_filename', 'classname', 'training_subset_of_class','x_min','y_min','x_max','y_max'))
            writer.writerows(lines)


test_set = Path('C:/Users/BangoCs/Desktop/MyDocs Offline/year4/semester 2/FYP/datasets/flickr_logos_27_dataset/test_set.csv')
if test_set.is_file():
    print('test_set.csv already created')
else:
    with open('C:/Users/BangoCs/Desktop/MyDocs Offline/year4/semester 2/FYP/datasets/flickr_logos_27_dataset/flickr_logos_27_dataset_query_set_annotation.txt',
            'r') as test_as_txt_file:
        separated = (line.strip() for line in test_as_txt_file)
        lines = (line.split(" ") for line in separated if line)
        with open('C:/Users/BangoCs/Desktop/MyDocs Offline/year4/semester 2/FYP/datasets/flickr_logos_27_dataset/test_set.csv','w') as test_set:
            writer = csv.writer(test_set)
            writer.writerow(('im_filename', 'classname'))
            writer.writerows(lines)