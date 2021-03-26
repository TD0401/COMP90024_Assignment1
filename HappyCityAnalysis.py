import json
import os

""" This functions reads the file from a start index byte to an offset defined so that number of lines in memory are restricted
    The readlines will read lines with total bytesize < size_byte
    Parameters
    ----------
    file_ptr : file object
        The file pointer because we will open the file once and iterate multiple times loading and parsing only selective bytes at time in memory
    file_size : file size
        The size of the file in bytes
    start_index : int, optional
        The starting byte number from which we should start reading (default is 0)
    size_byte : int, optional
        The number of bytes we should read from the starting line byte (default is 100000).      
"""


def read_files(file_ptr, file_size, start_index=0, size_byte=10000):
    try:
        file_ptr.seek(start_index)
        lines = file_ptr.readlines(size_byte)
        first_line = False
        num_lines = len(lines)
        count_lines = 0
        for line in lines:
            count_lines = count_lines + 1
            try:
                # not reading first line
                if start_index == 0 and not first_line:
                    first_line = True
                # not reading last line, parse all json in between
                elif file_ptr.tell() < file_size or count_lines < num_lines:
                    parse_json(line)
            except:
                print("error in parsing particular line")

    except:
        print("Error in reading file and parsing data")


def parse_json(line):
    decoded_line = line.decode("UTF-8").replace("\n", "").replace("\r","")
    if decoded_line.endswith(","):
        decoded_line = decoded_line[:-1]
    data = json.loads(decoded_line)
    tweet_id = data["id"]
    tweet_lat = data["doc"]["coordinates"]["coordinates"][0]
    tweet_lng = data["doc"]["coordinates"]["coordinates"][1]
    tweet_text = data["doc"]["text"]

    #cellId = getCellId(tweet_lat, tweet_lng)
    #score = getScore(text)
    #addDataToCellList(cellId, score)

    #CellVsScore -> dictionary where key -> cellid, value -> object (cellid, nelat, nelng, swlat,swlng score)
    print("id: " + str(tweet_id) + ", lat: " + str(tweet_lat) + ", lng: " + str(tweet_lng) + ", text: " + str(tweet_text))
    #parse and put into data structure when defined, data strucutre should be defined at global level or local is to be checked during parallelization


""" TODO: 1. open file and iterate until eof is found
          2. in read file set the seek to the starting offset, read the lines, parse into json and take out selective data 
          3. return the dict, current pointer index, 
          4. stop reading when file size has reached current pointer index
          5. while parsing ignore first and last line  -- write a parse json function
"""

with open("/Users/trinadey/tinyTwitter.json", "rb") as file:
    file_size = os.path.getsize("/Users/trinadey/tinyTwitter.json")
    curr_index = file.tell()
    while curr_index < file_size:
        #parallelize read files get output, reduce it
        read_files(file, file_size, curr_index)
        curr_index = file.tell()


