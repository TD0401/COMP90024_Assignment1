import os
from itertools import islice
from mpi4py import MPI
import json


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
print("printing receiving " , recv)




