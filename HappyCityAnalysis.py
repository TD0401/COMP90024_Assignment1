import json
import os


def read_sentiment():
    raw_file = "AFINN.txt"
    word_store = {}

    with open(raw_file, "r") as file_in:
        for line in file_in:
            s = line.replace("\t", "#^#")
            alist = s.split("#^#")
            word_store[alist[0]] = int(alist[1])
    return word_store

def melb_grid():
    grid_dict = {}
    with open("melbGrid2.json", "r") as json2py:
        obj = json.load(json2py)
        for item in obj['features']:
            id = item['properties']['id']
            grid_dict[id] = item['properties']
            grid_dict[id]['score'] = 0

    return grid_dict


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


def read_files(file_ptr, file_size, map_grid,sentiment_dict, start_index=0, size_byte=10000 ):
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
                    parse_json(line, map_grid,sentiment_dict)
            except:
                print("error in parsing particular line")

    except:
        print("Error in reading file and parsing data")


def parse_json(line, map_grid,sentiment_dict):
    decoded_line = line.decode("UTF-8").replace("\n", "").replace("\r","")
    if decoded_line.endswith(","):
        decoded_line = decoded_line[:-1]
    data = json.loads(decoded_line)
    tweet_lng = data["doc"]["coordinates"]["coordinates"][0]
    tweet_lat = data["doc"]["coordinates"]["coordinates"][1]
    tweet_text = data["doc"]["text"]
    cellId = find_cell_id(tweet_lat, tweet_lng, map_grid)
    print("tweet_lat: " + str(tweet_lat) + ", tweet_lng: " + str(tweet_lng) + " , cellId:" + cellId)
    if cellId != '':
        print('write cell score here')
        #score = getScore(text)
        #addDataToCellList(cellId, score)


def find_cell_id(lat,lng, map_grid):
    cell_id = ''
    prev_ymin =''
    left_populated = False
    for coord in map_grid.values():
        #within cell
        if lng > coord['xmin'] and lng < coord['xmax'] and lat > coord['ymin']  and lat < coord['ymax']:
            cell_id = coord['id']
            return cell_id

        # on vertical bounds go left
        if lng == coord['xmax'] and lat >= coord['ymin']  and lat <= coord['ymax']:
            if prev_ymin == '' or prev_ymin < coord['ymin']:
                prev_ymin= coord['ymin']
                cell_id = coord['id']
                left_populated = True
        if lng == coord['xmin']  and lat >= coord['ymin'] and lat <= coord['ymax'] and not left_populated:
            cell_id = coord['id']
        # on horizontal bounds go bottom
        if lat == coord['ymin']  and lng >= coord['xmin'] and lng <= coord['xmax'] and not left_populated:
            cell_id = coord['id']
        if lat == coord['ymax']   and lng >= coord['xmin'] and lng <= coord['xmax'] and not left_populated:
            cell_id = coord['id']
    return cell_id



""" TODO: 1. open file and iterate until eof is found
          2. in read file set the seek to the starting offset, read the lines, parse into json and take out selective data 
          3. return the dict, current pointer index, 
          4. stop reading when file size has reached current pointer index
          5. while parsing ignore first and last line  -- write a parse json function
"""
def main():
    sentiment_dict = read_sentiment()
    map_grid = melb_grid()
    file_name= "tinyTwitter.json"
    with open(file_name, "rb") as file:
        file_size = os.path.getsize(file_name)
        curr_index = file.tell()
        while curr_index < file_size:
            #parallelize read files get output, reduce it
            read_files(file, file_size,  map_grid,sentiment_dict , curr_index)
            curr_index = file.tell()


main()