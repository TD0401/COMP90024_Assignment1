from resource import getrusage as re_use, RUSAGE_SELF
from time import time as timestamp
import json
import re
from itertools import islice
from mpi4py import MPI

# init = time.perf_counter()
def time(function, args=tuple(), krg={}):
    init, init_re = timestamp(), re_use(RUSAGE_SELF)
    function(*args, **krg)
    end_re, end = re_use(RUSAGE_SELF),timestamp()

    return{
        'real': end - init,
        'sys' : end_re.ru_stime - init_re.ru_stime,
        'user': end_re.ru_utime - init_re.ru_utime
    }

def get_score(sentiment, tweet_line):
    temp_score = 0
    try:
        for i in sentiment.keys():
            patter = "(" + i + ")[!,.?'\"]*[\s]*"
            x = re.findall(patter, tweet_line.lower())
            if len(x) > 0:
                temp_score = temp_score + sentiment[i] * len(x)
    except:
        print("not working", i)
    return temp_score


def read_sentiment():
    raw_file = "AFINN.txt"
    word_store = {}

    with open(raw_file, "r") as file_in:
        for line in file_in:
            alist = line.split("\t")
            word_store[alist[0].lower()] = int(alist[1])
    return word_store


def melb_grid():
    grid_dict = {}
    with open("melbGrid2.json", "r") as json2py:
        obj = json.load(json2py)
        for item in obj['features']:
            id = item['properties']['id']
            grid_dict[id] = item['properties']
            grid_dict[id]['score'] = 0
            grid_dict[id]['count'] = 0

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


def read_files(map_grid, sentiment_dict, start_index, increment):
    try:
        file_name = "tempJson.json"
        with open(file_name, "r") as file:
            lines = list(islice(file, start_index, start_index + increment))
            num_lines = len(lines)
            count = 0
            for line in lines:
                count = count + 1
                try:
                    line = line.replace("\n", "").replace("\r", "")
                    # not reading first line
                    # not reading last line, parse all json in between
                    if not (start_index == 0 and count == 1) and not line == "]}":
                        parse_json(line, map_grid, sentiment_dict)
                except:
                    print("error in parsing particular line: ", line)


    except:
        print("Error in reading file and parsing data")


def parse_json(decoded_line, map_grid,sentiment_dict):
    if decoded_line.endswith(","):
        decoded_line = decoded_line[:-1]
    data = json.loads(decoded_line)
    tweet_lng = data["doc"]["coordinates"]["coordinates"][0]
    tweet_lat = data["doc"]["coordinates"]["coordinates"][1]
    tweet_text = data["doc"]["text"]
    cellId = find_cell_id(tweet_lat, tweet_lng, map_grid)
    #print("tweet_lat: " + str(tweet_lat) + ", tweet_lng: " + str(tweet_lng) + " , cellId:" + cellId)
    if cellId != '':
        score = get_score(sentiment_dict, tweet_text)
        map_grid[cellId]['score'] += score
        map_grid[cellId]['count'] += 1



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


def merge_final_map(recvd_data):
    final_map = {}
    for perArr in recvd_data:
        for key in perArr.keys():
            if key not in final_map:
                final_map[key] = perArr[key]
            else:
                final_map[key]['score'] += perArr[key]['score']
                final_map[key]['count'] += perArr[key]['count']
    print(final_map)

""" TODO: 1. open file and iterate until eof is found
          2. in read file set the seek to the starting offset, read the lines, parse into json and take out selective data 
          3. return the dict, current pointer index, 
          4. stop reading when file size has reached current pointer index
          5. while parsing ignore first and last line  -- write a parse json function
"""
def main():
    comm= MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    send_data = None
    process_data = None
    recv_data = None
    line_size = 250
    if rank == 0:
        sentiment_dict = read_sentiment()
        map_grid = melb_grid()
        send_data = {'melb_grid':map_grid , 'sentiment':sentiment_dict}

    send_data = comm.bcast(send_data, root=0)
    read_files(send_data['melb_grid'],send_data['sentiment'],  rank*line_size,line_size)
    process_data = send_data['melb_grid']
    recv_data = comm.gather(process_data, root=0)
    final_map= None
    if rank == 0:
        final_map = merge_final_map(recv_data)
    finalt = time.perf_counter()
    # print("real:", finalt-init)
    # print("sys:", )
    # print("user:", )

    print(time(main))



main()




