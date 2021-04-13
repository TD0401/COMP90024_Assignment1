import json
import pprint
import sys

str1 = '{"A1": {"id": "A1", "xmin": 144.7, "xmax": 144.85, "ymin": -37.65, "ymax": -37.5, "score": 770, "count": 2752}, "A2": {"id": "A2", "xmin": 144.85, "xmax": 145.0, "ymin": -37.65, "ymax": -37.5, "score": 4120, "count": 4904}, "A3": {"id": "A3", "xmin": 145.0, "xmax": 145.15, "ymin": -37.65, "ymax": -37.5, "score": 2687, "count": 5824}, "A4": {"id": "A4", "xmin": 145.15, "xmax": 145.3, "ymin": -37.65, "ymax": -37.5, "score": 57, "count": 381}, "B1": {"id": "B1", "xmin": 144.7, "xmax": 144.85, "ymin": -37.8, "ymax": -37.65, "score": 11667, "count": 21232}, "B2": {"id": "B2", "xmin": 144.85, "xmax": 145.0, "ymin": -37.8, "ymax": -37.65, "score": 32085, "count": 107386}, "B3": {"id": "B3", "xmin": 145.0, "xmax": 145.15, "ymin": -37.8, "ymax": -37.65, "score": 20230, "count": 34494}, "B4": {"id": "B4", "xmin": 145.15, "xmax": 145.3, "ymin": -37.8, "ymax": -37.65, "score": 5740, "count": 6643}, "C1": {"id": "C1", "xmin": 144.7, "xmax": 144.85, "ymin": -37.95, "ymax": -37.8, "score": 7672, "count": 10643}, "C2": {"id": "C2", "xmin": 144.85, "xmax": 145.0, "ymin": -37.95, "ymax": -37.8, "score": 191995, "count": 246925}, "C3": {"id": "C3", "xmin": 145.0, "xmax": 145.15, "ymin": -37.95, "ymax": -37.8, "score": 41429, "count": 69901}, "C4": {"id": "C4", "xmin": 145.15, "xmax": 145.3, "ymin": -37.95, "ymax": -37.8, "score": 19566, "count": 26097}, "C5": {"id": "C5", "xmin": 145.3, "xmax": 145.45, "ymin": -37.95, "ymax": -37.8, "score": 2656, "count": 5581}, "D3": {"id": "D3", "xmin": 145.0, "xmax": 145.15, "ymin": -38.1, "ymax": -37.95, "score": 7936, "count": 16318}, "D4": {"id": "D4", "xmin": 145.15, "xmax": 145.3, "ymin": -38.1, "ymax": -37.95, "score": 9566, "count": 16666}, "D5": {"id": "D5", "xmin": 145.3, "xmax": 145.45, "ymin": -38.1, "ymax": -37.95, "score": 3753, "count": 4705}}'
j = json.loads(str1)

for keys in j:
   j[keys]['perc'] = round(j[keys]['score'] * 100 / j[keys]['count'] ,2)


pprint.pprint(j)
