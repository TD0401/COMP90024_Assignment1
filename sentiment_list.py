# This code processes the file AFINN.txt into a funtion read_sentiment()
# Issue : 
# AFINN.txt file has multiple white spaces in b/w sentiment and score which throws --> ValueError for split()
# Solution:

# Steps                       *****CLEAN FILE*****
''' 1. Read File -> use split() default case  is " " jointly and replace with ','  generate --> clean
    2. Read clean to py dictionary word_file:
       map [key, value] as [sentiment, score]      
'''

'''                      
***********************************************************************************************************'''

def read_sentiment():

    raw_file = "AFINN.txt"
    word_store = {}
    
    with open(raw_file, "r") as file_in:
        for line in file_in:
            s = line.replace("\t","#^#")
            alist = s.split("#^#")
            word_store[alist[0]] = int(alist[1])
    return word_store


words = read_sentiment()
print(words)



