import json
import re
from itertools import islice
from mpi4py import MPI
import sys
import datetime

def get_score(sentiment, sentiment_space, tweet_line):
    temp_score = 0
    try:
        for i in sentiment_space.keys():
            patter = "(" + i + ")[!,.?'\"]*[\s]*"
            x = re.findall(patter, tweet_line.lower())
            if len(x) > 0:
                temp_score = temp_score + sentiment_space[x[0]] * len(x)

        words = tweet_line.lower().split()
        for i in words:
            word = re.sub("[!,.?'\"]*$","",i)
            if word in sentiment.keys():
                temp_score += sentiment[word]

    except:
        print("not able to get score for key:", i)
    return temp_score


def read_sentiment():
    raw_file = "AFINN.txt"
    word_store = {}
    split_word_store = {}

    with open(raw_file, "r") as file_in:
        for line in file_in:
            alist = line.split("\t")
            if len(alist[0].split()) > 1:
                split_word_store[alist[0].lower()] = int(alist[1])
            else:
                word_store[alist[0].lower()] = int(alist[1])
    return word_store, split_word_store


def melb_grid():
    grid_dict = {}
    with open("melbGrid.json", "r") as json2py:
        obj = json.load(json2py)
        for item in obj['features']:
            id = item['properties']['id']
            grid_dict[id] = item['properties']
            grid_dict[id]['score'] = 0
            grid_dict[id]['count'] = 0
    return grid_dict


def read_files(map_grid, sentiment_dict, sentiment_dict_space, start_index, increment):
    try:
        file_name = sys.argv[1]
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
                        parse_json(line, map_grid, sentiment_dict,sentiment_dict_space)
                except:
                    print("error in parsing particular line: ", str(start_index + count))
    except:
        print("Error in reading file and parsing data")


def parse_json(decoded_line, map_grid, sentiment_dict,sentiment_dict_space):
    if decoded_line.endswith(","):
        decoded_line = decoded_line[:-1]
    data = json.loads(decoded_line)
    tweet_lng = data["doc"]["coordinates"]["coordinates"][0]
    tweet_lat = data["doc"]["coordinates"]["coordinates"][1]
    tweet_text = data["doc"]["text"]
    cell_id = find_cell_id(tweet_lat, tweet_lng, map_grid)
    if cell_id != '':
        score = get_score(sentiment_dict, sentiment_dict_space, tweet_text)
        map_grid[cell_id]['score'] += score
        map_grid[cell_id]['count'] += 1


def find_cell_id(lat,lng, map_grid):
    cell_id = ''
    prev_ymin = ''
    left_populated = False
    for coord in map_grid.values():
        # within cell
        if coord['xmin'] < lng < coord['xmax'] and coord['ymin'] < lat < coord['ymax']:
            cell_id = coord['id']
            return cell_id

        # on vertical bounds go left
        if lng == coord['xmax'] and coord['ymin'] <= lat <= coord['ymax']:
            if prev_ymin == '' or prev_ymin < coord['ymin']:
                prev_ymin = coord['ymin']
                cell_id = coord['id']
                left_populated = True
        if lng == coord['xmin'] and coord['ymin'] <= lat <= coord['ymax'] and not left_populated:
            cell_id = coord['id']

        # on horizontal bounds go bottom
        if lat == coord['ymin'] and coord['xmin'] <= lng <= coord['xmax'] and not left_populated:
            cell_id = coord['id']
        if lat == coord['ymax'] and coord['xmin'] <= lng <= coord['xmax'] and not left_populated:
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
    return final_map


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    send_data = None
    process_data = None
    recv_data = None
    line_size = int(int(sys.argv[2])/size)
    if int(sys.argv[2]) % size != 0:
        line_size += 1
    if rank == 0:
        sentiment_dict, sentiment_dict_space = read_sentiment()
        map_grid = melb_grid()
        send_data = {'melb_grid': map_grid, 'sentiment': sentiment_dict, 'sentiment_space': sentiment_dict_space}
    send_data = comm.bcast(send_data, root=0)
    read_files(send_data['melb_grid'], send_data['sentiment'],send_data['sentiment_space'], rank*line_size, line_size)
    process_data = send_data['melb_grid']
    recv_data = comm.gather(process_data, root=0)
    if rank == 0:
        final_map = merge_final_map(recv_data)
        print(final_map)


main()





