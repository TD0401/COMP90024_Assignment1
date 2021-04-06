import os
from itertools import islice
#from mpi4py import MPI
import json
import  sys
import  ijson


def read_sentiment():
    raw_file = "AFINN.txt"
    word_store = {}
    split_word_store={}

    with open(raw_file, "r") as file_in:
        for line in file_in:
            alist = line.split("\t")
            if len(alist[0].split())>1:
                split_word_store[alist[0].lower()] = int(alist[1])
            else:
                word_store[alist[0].lower()] = int(alist[1])
    #print(split_word_store)
    #print(word_store)
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


def main():
    comm = MPI.COMM_WORLD
    size = comm.Get_size()
    rank = comm.Get_rank()

    data = None
    sendBuf = None
    recv =None
    if rank == 0:
        grid_data = melb_grid()
        data = {'melGrid' : grid_data,
                'sentiment' : read_sentiment()
                }


    data = comm.bcast(data, root=0)
    print('Rank: ',rank,', data: ' , len(data['melGrid']) , ' , sentiment size: ' , len(data['sentiment']))

    sendBuf = len(data['melGrid']) + len(data['sentiment'])

    recv = comm.gather(sendBuf, root=0)
    print("printing receiving ", recv)

def read_via_json(line):
    data = json.loads(line)
    tweet_lng = data["doc"]["coordinates"]["coordinates"][0]
    tweet_lat = data["doc"]["coordinates"]["coordinates"][1]
    tweet_text = data["doc"]["text"]
    print("lat: ", tweet_lat , ", lng: ", tweet_lng , " ,text:" , tweet_text)


def read_via_ijson(line):
    coord = ijson.items(line, 'value.geometry.coordinates.item')
    text = ijson.items(line, 'value.properties.text')
    for a in text:
        print(a)
    for a in coord:
        print(a)

def read_json():
    #comm = MPI.COMM_WORLD
    #rank = comm.Get_rank()
    #size = comm.Get_size()
    send_data = None
    #line_size = int(int(sys.argv[2]) / size)
    #if int(sys.argv[2]) % size != 0:
    #    line_size += 1
    #if rank == 0:
    #    sentiment_dict = read_sentiment()
    #    map_grid = melb_grid()
    #    send_data = {'melb_grid': map_grid, 'sentiment': sentiment_dict}
    #send_data = comm.bcast(send_data, root=0)
    with open(sys.argv[1], "r") as file:
        lines = list(islice(file, 0,  30000))
        num_lines = len(lines)
        count = 0
        for line in lines:
            count = count + 1
            try:
                line = line.replace("\n", "").replace("\r", "")
                if line.endswith(","):
                    line = line[:-1]
                # not reading first line
                # not reading last line, parse all json in between
                if not (count == 1) and not line == "]}":
                    read_via_ijson(line)

            except:
                print("error in parsing particular line: ")







