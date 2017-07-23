from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
__author__ = 'a_medelyan'
import rake
import test_data
import sys


# reading a directory with test documents
input_dir = sys.argv[1]

# number of top ranked keywords to evaluate
top = int(sys.argv[2])

test_set = test_data.read_data(input_dir)

# evaluating
rake_object = rake.Rake("SmartStoplist.txt", 5, 3, 4)
total_precision = 0
total_recall = 0

for test_doc in test_set.values():
    print('document', test_doc.name)
    print(len(test_doc.keywords), 'manual keywords: ', test_doc.keywords)

    keywords = rake_object.run(test_doc.text)[:top]
    print('RAKE keywords:', keywords)

    num_manual_keywords = len(test_doc.keywords)

    correct = 0
    for i in range(0,min(top, len(keywords))):
        if keywords[i][0] in set(test_doc.keywords):
            correct += 1
    total_precision += correct/float(len(keywords))
    total_recall += correct/float(num_manual_keywords)
    print('correct:', correct, 'out of', num_manual_keywords)

avg_precision = round(total_precision*100/float(len(test_set)), 2)
avg_recall = round(total_recall*100/float(len(test_set)), 2)

avg_fmeasure = round(2*avg_precision*avg_recall/(avg_precision + avg_recall), 2)

print("Precision", avg_precision, "Recall", avg_recall, "F-Measure", avg_fmeasure)