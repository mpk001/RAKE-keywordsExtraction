from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
__author__ = 'a_medelyan'
import test_data
import rake
import sys

# reading a directory with test documents
input_dir = sys.argv[1]
# number of top ranked keywords to evaluate
top = int(sys.argv[2])

test_set = test_data.read_data(input_dir)

best_fmeasure = 0
best_vals = []

for min_char_length in range(3,8):
    for max_words_length in range(3,6):
        for min_keyword_frequency in range(1,7):

            rake_object = rake.Rake("SmartStoplist.txt", min_char_length, max_words_length, min_keyword_frequency)
            total_fmeasure = 0
            for test_doc in test_set.values():
                keywords = rake_object.run(test_doc.text)

                num_manual_keywords = len(test_doc.keywords)
                correct = 0
                try:
                    for i in range(0,min(top, len(keywords))):
                        if keywords[i][0] in set(test_doc.keywords):
                            correct += 1
                except IndexError:
                    print("Problem with evaluating ", keywords)

                precision = correct/float(top)
                recall = correct/float(num_manual_keywords)

                if precision > 0 and recall > 0:
                    total_fmeasure += 2*precision*recall/(precision + recall)


            avg_fmeasure = round(total_fmeasure*100/float(len(test_set)), 2)

            if avg_fmeasure > best_fmeasure:
                best_fmeasure = avg_fmeasure
                best_vals = [min_char_length, max_words_length, min_keyword_frequency]

            print(min_char_length, max_words_length, min_keyword_frequency, "\t", avg_fmeasure)

print("")
print("Best result at ", best_fmeasure)
print("with\tmin_char_length", best_vals[0])
print("\tmax_words_length", best_vals[1])
print("\tmin_keyword_frequency", best_vals[2])