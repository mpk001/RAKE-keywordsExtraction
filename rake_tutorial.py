# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
import six
__author__ = 'a_medelyan'

import rake
import operator
import pandas as pd
import re
from bs4 import BeautifulSoup
from keras.preprocessing.text import Tokenizer
import io
import codecs

# EXAMPLE ONE - SIMPLE
stoppath = "SmartStoplist.txt"
MAX_NB_WORDS = 20000

# 1. initialize RAKE by providing a path to a stopwords file
rake_object = rake.Rake(stoppath, 5, 3, 4)

# # 2. run on RAKE on a given text
# sample_file = io.open("data/docs/fao_test/w2167e.txt", 'r',encoding="iso-8859-1")
# text = sample_file.read()
#
# keywords = rake_object.run(text)
#
# # 3. print results
# print("Keywords:", keywords)
#
# print("----------")
# # EXAMPLE TWO - BEHIND THE SCENES (from https://github.com/aneesha/RAKE/rake.py)
#
# # 1. initialize RAKE by providing a path to a stopwords file
# rake_object = rake.Rake(stoppath)

# text = "Compatibility of systems of linear constraints over the set of natural numbers. Criteria of compatibility " \
#        "of a system of linear Diophantine equations, strict inequations, and nonstrict inequations are considered. " \
#        "Upper bounds for components of a minimal set of solutions and algorithms of construction of minimal generating"\
#        " sets of solutions for all types of systems are given. These criteria and the corresponding algorithms " \
#        "for constructing a minimal supporting set of solutions can be used in solving all the considered types of " \
#        "systems and systems of mixed types."

def clean_str(string):
    """
    Tokenization/string cleaning for dataset
    Every dataset is lower cased except
    """
    # string = re.sub("['`,!\"\'\\.,;?\t\n]", "", string)
    string = re.sub("[?\t\n]", "", string)
    # string = re.sub("[\t\n]", "", string)
    sss = string.split()
    # for jj in sss:
    #     if str != ' ':
    #         string = jj + ' '
    string = ' '.join(str(jj) for jj in sss)
    # string = string[0:len(string)-1]
    return string

def clean_word(string):
    """
    Tokenization/string cleaning for dataset
    Every dataset is lower cased except
    """
    string = re.sub("^['\.`,/:()\-\[\]!\"\s\\;?\t\n]", "", string)
    string = re.sub("['\.`,/:()\-\[\]!\"\s\\;?\t\n]$", "", string)
    # string = string[0:len(string)-1]
    return string

def keyphrase_extract(text):
    stoppath = "SmartStoplist.txt"
    # generate candidate keywords
    sentenceList = []
    sentenceList.append(text)
    stopwordpattern = rake.build_stop_word_regex(stoppath)
    phraseList = rake.generate_candidate_keywords(sentenceList, stopwordpattern)
    # print("Phrases:", phraseList)

    # calculate individual word scores
    wordscores = rake.calculate_word_scores(phraseList)

    # generate candidate keyword scores
    keywordcandidates = rake.generate_candidate_keyword_scores(phraseList, wordscores)
    # for candidate in keywordcandidates.keys():
    #     print("Candidate: ", candidate, ", score: ", keywordcandidates.get(candidate))

    # sort candidates by score to determine top-scoring keywords
    sortedKeywords = sorted(six.iteritems(keywordcandidates), key=operator.itemgetter(1), reverse=True)
    return sortedKeywords
    # for example, you could just take the top third as the final keywords
    # if len(sortedKeywords) > 1:
    #     for keyword in sortedKeywords[0:3]:
    #         print("Keyword: ", keyword[0], ", score: ", keyword[1])

if __name__ == '__main__':
    # data = pd.read_csv('F://workspace_mpk0//dataset//quora_duplicate_questions.tsv', sep='\t')
    # f0=file('F://workspace_mpk0//dataset//quora_duplicate_questions_keyphrase2.tsv',"a+")
    # # f0.writelines('id\tqid1\tqid2\tquestion1\tquestion2\tkeyphrase1\tkeyphrase2\tis_duplicate\n')
    data = pd.read_csv('F://workspace_mpk0//dataset//Quora_question_pair_partition//test.tsv', sep='\t')
    f0=file('F://workspace_mpk0//dataset//Quora_question_pair_partition//test_keyphrase_v3.tsv',"a+")
    f0.writelines('is_duplicate\tquestion1\tquestion2\tkeyphrase1\tkeyphrase2\tid\n')

    count = 0
    max_keynum1 = 0
    max_keynum2 = 0
    num1 = 0
    num2 = 0
    entity = []
    with open('F://workspace_mpk0//dataset//Quora_question_pair_partition//freebase_code_names.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            entity.append(line.split('>')[0].split('/')[6])


    for idx in range(data.id.shape[0]):
        res = ''
        text10 = BeautifulSoup(data.question1[idx], "lxml")
        text1 = clean_str(text10.get_text().encode('ascii', 'ignore'))
        # text1 = text10.get_text().encode('ascii', 'ignore')

        text20 = BeautifulSoup(data.question2[idx], "lxml")
        text2 = clean_str(text20.get_text().encode('ascii', 'ignore'))
        # text2 = text20.get_text().encode('ascii', 'ignore')

        if text1 and text2:
            t1 = text1.split('\t')
            t2 = text2.split('\t')
            entity1 = []
            entity2 = []
            temp1 = text1.split(' ')
            temp2 = text2.split(' ')
            for t in temp1:
                if t in entity:
                    entity1.append(t)
            for t in temp2:
                if t in entity:
                    entity2.append(t)
            if len(t1) == 1 and len(t2) == 1 and len(entity1) > 0 and len(entity2) > 0:
            # if len(t1) == 1 and len(t2) == 1:
                #提取关键词
                sortedKeywords1 = keyphrase_extract(text1)
                sortedKeywords2 = keyphrase_extract(text2)
                key1 = ''
                key2 = ''
                if len(sortedKeywords1) > 0 and len(sortedKeywords2) > 0:
                    count += 1
                    num1 += len(sortedKeywords1)
                    num2 += len(sortedKeywords2)
                    if max_keynum1 < len(sortedKeywords1): max_keynum1 = len(sortedKeywords1)
                    if max_keynum2 < len(sortedKeywords2): max_keynum2 = len(sortedKeywords2)
                    # for keyword in sortedKeywords1[0:3]:
                    for keyword in sortedKeywords1:
                        kkk = keyword[0].split()
                        kkk0 = ''
                        for i in range(len(kkk)):
                            ll = clean_word(str(kkk[i]))
                            if ll:
                                kkk0 += ll + '_'
                        key1 += kkk0[:len(kkk0)-1] + ' '
                    key1 = key1[0:len(key1)-1]
                    print (key1)
                    # for keyword in sortedKeywords2[0:3]:
                    for keyword in sortedKeywords2:
                        kkk = keyword[0].split()
                        kkk0 = ''
                        for i in range(len(kkk)):
                            ll = clean_word(str(kkk[i]))
                            if ll:
                                kkk0 += ll + '_'
                        key2 += kkk0[:len(kkk0)-1] + ' '
                    key2 = key2[0:len(key2)-1]
                    print (key2)

                    Entity1 = ''
                    for e in entity1:
                        Entity1 += e + '_'
                    Entity1 = Entity1[0:len(Entity1)-1]
                    Entity2 = ''
                    for e in entity2:
                        Entity2 += e + '_'
                    Entity2 = Entity2[0:len(Entity2)-1]
                    # res = str(int(data.is_duplicate[idx])) + '\t' + text1 + '\t' + text2 + '\t' + key1 + '\t' + key2 + '\t' + str(data.id[idx]) + '\n'
                    res = str(int(data.is_duplicate[idx])) + '\t' + data.question1[idx] + '\t' + data.question2[idx] + '\t' + key1 + '\t' + key2 + '\t' + Entity1 + '\t' + Entity2 + '\t' + str(data.id[idx]) + '\n'

                    # print (res)
                    print (count)
                    f0.writelines(str(res))

    f0.close()

    print (max_keynum1, max_keynum2)
    print (num1/count, num2/count)

    # text = "while alkalines are 1.5 V"
    # # sortedKeywords = keyphrase_extract(text)
    # # print (len(sortedKeywords))
    # # if len(sortedKeywords) > 0:
    # #     for keyword in sortedKeywords[0:3]:
    # #         print("Keyword: ", keyword[0], ", score: ", keyword[1])
    # text = clean_str(text)
    # print (text)


