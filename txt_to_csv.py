#Code reference
#Author(s) name:OliverCollins
#Date: 04/12/2018
#Title of program/source code: TXTtoCSV.py
#Code version: 1
#Type: computer program
#Web address or publisher: https://github.com/OliverCollins/TXT-to-CSV/blob/master/TXTtoCSV.py
#Modified: Yes
#Modified lines: line 16-37 is added. not relevant to the referenced code
#                line 53 --> added code to remove last character from the end of lines


import csv
from pathlib import Path

#inintialise location for training and test sets
training_set = Path('path/to/data/bin/training_set.csv')
test_set = Path('path/to/data/bin/test_set.csv')
test_txt = Path('path/to/flickr_logos_27_dataset/flickr_logos_27_dataset_query_set_annotation.txt')
training_txt = Path('path/to/flickr_logos_27_dataset/flickr_logos_27_dataset_training_set_annotation.txt')

#create new csv from training set
try:
    if training_set.is_file():
        print('training_set.csv already created')
    else:
        with open(training_txt,'r') as training_as_txt_file:
           separated = (line.strip() for line in training_as_txt_file)
           lines = (line.split(' ') for line in separated if line)
           with open(training_set, 'w') as training:
                writer = csv.writer(training)
                writer.writerow(('im_filename', 'classname', 'training_subset_of_class','xmin','ymin','xmax','ymax'))
                writer.writerows(lines)
                print('training_set.csv with original content created')
except:
    print('Error in converting flickr_logos_27_dataset_training_set_annotation.txt to training_set.csv')

#create new csv from test set
try:
    if test_set.is_file():
        print('test_set.csv already created')
    else:
        with open(test_txt,'r') as txt_test:
            test = open(test_set, 'w')
            new_text = txt_test.readlines()
        features = []
        line_break = 0
        test_writer = csv.writer(test)
        test_writer.writerow(('im_filename', 'classname'))
        for i in range(0, len(new_text)):
            for feature in new_text[i].split():
                features.append(feature + ',')

        for i in range(0, len(features)):
            if (line_break == 2):
                test.write('\n')
                test.write(features[i])
                line_break = 1
            else:
                test.write(features[i][:-1])
                line_break += 1
        test.close()
        print('test_set.csv with original content created')
except:
    print('Error in converting flickr_logos_27_dataset_query_set_annotation.txt to test_set.csv')