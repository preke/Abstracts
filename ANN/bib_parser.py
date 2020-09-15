import pybtex
import pandas as pd
import json
import traceback
from pybtex.database.input import bibtex

bib_path = 'anthology+abstracts.bib'
#open a bibtex file
parser = bibtex.Parser()
bibdata = parser.parse_file(bib_path)

import scispacy
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

# jsonl
json_file = open('ann_abstract.jsonl', 'w')

index = 0
for bib_id in bibdata.entries:
    tmp_dict = {}
    b = bibdata.entries[bib_id].fields
    try:
        ab = b['abstract']
        tmp_dict['abstract_id'] = index
        tmp_dict['sentences'] = [str(i) for i in list(nlp(ab).sents) if len(str(i)) >= 3]
        tmp_dict['labels'] = ['0']*len(tmp_dict['sentences'])

        if len(tmp_dict['sentences']) >=3:
            json_str = json.dumps(tmp_dict)
            json_file.write(json_str + '\n')
        index += 1
    except:
        pass
json_file.close()

# tsv 

# data_frame = []
# for bib_id in bibdata.entries:
#     tmp_list = []
#     b = bibdata.entries[bib_id].fields
#     try:
#         tmp_list.append(b["title"])
#     except:
#     	tmp_list.append('N/A')

#     try:
#         tmp_list.append(b["year"])
#     except:
#     	tmp_list.append('N/A')
    
#     try:
#         tmp_list.append(b["booktitle"])
#     except:
#     	try:
#     		tmp_list.append(b["journal"])
#     	except:
#     		tmp_list.append('N/A')

#     try:
#         tmp_list.append(b["abstract"])
#     except:
#     	tmp_list.append('N/A')

#     data_frame.append(tmp_list)

# data_frame = pd.DataFrame(data_frame, columns = ['title', 'year', 'booktitle/journal', 'abstract'])
# data_frame.to_csv('ann.tsv', sep='\t', index=False)

