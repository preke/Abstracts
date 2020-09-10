import pybtex
import pandas as pd
from pybtex.database.input import bibtex

bib_path = 'anthology+abstracts.bib'
#open a bibtex file
parser = bibtex.Parser()
bibdata = parser.parse_file(bib_path)

#loop through the individual references
data_frame = []
for bib_id in bibdata.entries:
    tmp_list = []
    b = bibdata.entries[bib_id].fields
    try:
        tmp_list.append(b["title"])
    except:
    	tmp_list.append('N/A')

    try:
        tmp_list.append(b["year"])
    except:
    	tmp_list.append('N/A')
    
    try:
        tmp_list.append(b["booktitle"])
    except:
    	try:
    		tmp_list.append(b["journal"])
    	except:
    		tmp_list.append('N/A')

    try:
        tmp_list.append(b["abstract"])
    except:
    	tmp_list.append('N/A')

    data_frame.append(tmp_list)

data_frame = pd.DataFrame(data_frame, columns = ['title', 'year', 'booktitle/journal', 'abstract'])
data_frame.to_csv('ann.tsv', sep='\t', index=False)

