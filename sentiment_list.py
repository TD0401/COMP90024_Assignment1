# This code processes the file AFINN.txt
# Issue : 
# AFINN.txt file has multiple white spaces in b/w sentiment and score which throws --> ValueError for split()
# Solution:

# Steps                       *****CLEAN FILE*****
''' 1. use split() default case  is " " jointly and replace with ','  generate --> clean.txt
    2. Read clean.txt to py dictionary word_file:
       map [key, value] as [sentiment, score]      
'''
# AFINN.txt -----> clean.txt ------> python dictionary                    constraint: 
'''                      
********************************************************************************************************************************'''

# Step 1 Clean the file from multiple spaces

import re

def read_sentiment():

    raw_file = "AFINN.txt"
    word_store = {}

    with open(raw_file, "rt") as file_in:
    # clean_File = open("clean.txt", "wt")  
        pattern = '([a-zA-Z])\s([a-zA-Z])'


        for line in file_in:
            # clean_File.write(' '.join(line.split())+'\n')
            s = (' '.join(line.split()))
            s = re.sub(pattern,"-",s)
            s = s.strip()
            alist = s.split()
            word_store[alist[0]] = alist[1]

    print(word_store)
    return word_store
    





