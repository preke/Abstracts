#!/usr/bin/env python
# encoding: utf-8
'''
@author: shuaiqi
@file: data_collator.py
@time: 2020/9/16 17:24
@desc:
'''
import os
import json
import pandas as pd
import numpy as np
import pyparsing as pp


def preprocess(filename):
    preprocessed_list = []
    nested_braces = pp.nestedExpr('[', ']')

    with open(filename) as f:
        for line in f:
            line_list = nested_braces.parseString(line).asList()[0]

            abs_dict={}
            abs_id = int(line_list[0][0:-1])
            abs_dict['abs_id'] = abs_id
            #sent_num = int(len(line_list[1]) / 2) + 1
            sent_list = []
            for i, sents in enumerate(line_list[1]):
                #index = int(i / 2) + 1
                if sents != ',':
                    sent_dict ={}
                    if len(sents)==3 and sents[1] == ',':
                        sent = sents[0][1:-1]
                        sent_label = sents[2][1:-1]
                        sent_dict['sent'] = sent
                        sent_dict['sent_label'] = sent_label
                        sent_list.append(sent_dict)
            abs_dict['sent_list'] = sent_list
            preprocessed_list.append(abs_dict)
    return preprocessed_list


def categories_statistics(input_list):
    statistics_data ={}

    abs_id_list=[]
    sent_num_list = []
    sent_order_list = []

    background_sent_list = []
    background_sent_num_list = []
    background_sent_index_list = []
    method_sent_list = []
    method_sent_num_list = []
    method_sent_index_list = []
    result_sent_list = []
    result_sent_num_list = []
    result_sent_index_list = []
    objective_sent_list = []
    objective_sent_num_list = []
    objective_sent_index_list = []
    other_sent_list = []
    other_sent_num_list = []
    other_sent_index_list = []

    for abs in input_list:
        abs_id_list.append(abs['abs_id'])
        sent_num_list.append(len(abs['sent_list']))

        sent_order = []
        background_sents = []
        background_sent_indexes = []
        method_sents = []
        method_sent_indexes = []
        result_sents = []
        result_sent_indexes = []
        objective_sents = []
        objective_sent_indexes = []
        other_sents = []
        other_sent_indexes = []

        background_sents_num = 0
        method_sents_num = 0
        result_sents_num = 0
        objective_sents_num = 0
        other_sents_num = 0

        for index,sent_dict in enumerate(abs['sent_list']):
            label = sent_dict['sent_label']
            sent = sent_dict['sent']

            sent_order.append(label)
            if label == 'background_label':
                background_sents_num += 1
                background_sents.append(sent)
                background_sent_indexes.append(index)
            elif label == 'objective_label':
                objective_sents_num += 1
                objective_sents.append(sent)
                objective_sent_indexes.append(index)
            elif label == 'method_label':
                method_sents_num += 1
                method_sents.append(sent)
                method_sent_indexes.append(index)
            elif label == 'result_label':
                result_sents_num += 1
                result_sents.append(sent)
                result_sent_indexes.append(index)
            elif label == 'other_label':
                other_sents_num += 1
                other_sents.append(sent)
                other_sent_indexes.append(index)

        sent_order_list.append(sent_order)
        background_sent_list.append(background_sents)
        background_sent_num_list.append(background_sents_num)
        background_sent_index_list.append(background_sent_indexes)
        method_sent_list.append(method_sents)
        method_sent_num_list.append(method_sents_num)
        method_sent_index_list.append(method_sent_indexes)
        result_sent_list.append(result_sents)
        result_sent_num_list.append(result_sents_num)
        result_sent_index_list.append(result_sent_indexes)
        objective_sent_list.append(objective_sents)
        objective_sent_num_list.append(objective_sents_num)
        objective_sent_index_list.append(objective_sent_indexes)
        other_sent_list.append(other_sents)
        other_sent_num_list.append(other_sents_num)
        other_sent_index_list.append(other_sent_indexes)

    statistics_data['abs_id'] = abs_id_list
    #statistics_data['sent_num'] = sent_num_list
    statistics_data['sent_order'] = sent_order_list


    statistics_data['background_sents'] = background_sent_list
    statistics_data['background_sent_num'] = background_sent_num_list
    statistics_data['background_sent_index'] = background_sent_index_list
    statistics_data['method_sents'] = method_sent_list
    statistics_data['method_sent_num'] = method_sent_num_list
    statistics_data['method_sent_index'] = method_sent_index_list
    statistics_data['result_sents'] = result_sent_list
    statistics_data['result_sent_num'] = result_sent_num_list
    statistics_data['result_sent_index'] = result_sent_index_list
    statistics_data['objective_sents'] = objective_sent_list
    statistics_data['objective_sent_num'] = objective_sent_num_list
    statistics_data['objective_sent_index'] = objective_sent_index_list
    statistics_data['other_sents'] = other_sent_list
    statistics_data['other_sent_num'] = other_sent_num_list
    statistics_data['other_sent_index'] = other_sent_index_list

    return statistics_data

'''
# csur
orginal_corpus = "data/csur_abstract.jsonl"
sent_label_file = "data/predict_result_csur.txt"
output_csv = "data/input.csv"
'''

# ann
orginal_corpus = "data/ann_abstract.jsonl"
sent_label_file = "data/predict_result_ann_abstract.txt"
output_csv = "data/input_ann.csv"

json_file_path = orginal_corpus

abs_id_list = []
abs_sents_list = []
abs_sents_num_list = []

# read_json_file (original file)
with open(json_file_path) as f:
    for line in f:
        json_dict = json.loads(line)
        abs_id = json_dict["abstract_id"]
        abs_sents = json_dict["sentences"]
        abs_id_list.append(abs_id)
        abs_sents_list.append(abs_sents)
        abs_sents_num_list.append(len(abs_sents))
abs_dict={'abs_id':abs_id_list,'abs_sents':abs_sents_list,'abs_sents_num':abs_sents_num_list}
abs_dataframe = pd.DataFrame(data=abs_dict)

# read_txt_file (sentence classification result)
preprocessed_list = preprocess(sent_label_file)
statistics_dict = categories_statistics(preprocessed_list)
statistics_dataframe = pd.DataFrame(data=statistics_dict)

result_dataframe = pd.merge(abs_dataframe,statistics_dataframe,on=['abs_id'],how='left')

# output CSV
result_dataframe.to_csv(output_csv, index=False, sep=',',float_format='%.5f')

pass