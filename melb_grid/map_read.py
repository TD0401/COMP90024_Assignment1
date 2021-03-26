import json 

jd = "melbGrid.json"
def melbGrid ():
    with open("melbGrid2.json", "r") as json2py:
        obj = json.load(json2py)
        pretty_json = json.dumps(obj, indent=4)
    
        json_reload = json.loads(pretty_json)
    
        for item in json_reload['features']:
        
            id = item['properties']['id']
            #print(id) #[stores all values A1, A2, A3...]
            co_ord = item['geometry']['coordinates']
            #print(co_ord) #[stores all values lat-long]
            '''tring to merge both
            # grid_dict = dict(zip(id,co_ord))'''
            grid_dict = {}
            for key in id:
                for value in co_ord:
                    grid_dict[key] = value
                    co_ord.remove(value)
                    break

            print(str(grid_dict))


melbGrid()

# Issue --> 
# The key value is stored but
# Upon dictionary MERGE the numeric values of ID A1-A2...dissappers only A A A A B B B B....




        
  
