import json 


def melb_grid():
    with open("melbGrid2.json", "r") as json2py:
        obj = json.load(json2py)
        grid_dict = {}
        for item in obj['features']:
            id = item['properties']['id']
            co_ord = item['geometry']['coordinates']
            for value in co_ord:
                grid_dict[id] = {'id': id, 'coordinates': value, 'score': 0 }
        print(str(grid_dict))


melb_grid()