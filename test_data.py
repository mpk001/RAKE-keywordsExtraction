from __future__ import absolute_import
__author__ = 'a_medelyan'
import os
import io

# class to hold our test instance (document plus its correct manual keywords)
class TestDoc:
    def __init__(self, name):
        self.name = name
        self.text = ''
        self.keywords = []


# reading documents and their keywords from a directory
def read_data(input_dir):

    test_set = {}

    for doc in os.listdir(input_dir):

        file_reader = io.open(os.path.join(input_dir,doc), 'r',encoding="iso-8859-1")
        file_name = doc[:-4]
        if file_name not in test_set:
            d = TestDoc(file_name)
        else:
            d = test_set[file_name]

        if not doc.endswith(".txt"):
            continue

        # get document text
        text = file_reader.read()
        d.text = text

        # get document keywords
        file_reader = open(os.path.join(input_dir,file_name + ".key"), 'r')
        manual_keywords = file_reader.read()
        for line in manual_keywords.split('\n'):
            line = line.rstrip().lower()
            if len(line) > 0:
                if '\t' in line:
                    d.keywords.append(line[0:line.find('\t')])
                else:
                    d.keywords.append(line)

        # add document to test set
        test_set[file_name] = d

    return test_set
