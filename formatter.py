#Author Liang
"""Given dialog format [[u1,u2,u3],[u1,u2],[],...]
 Get format [{"history":[u1,u2,u3]}, {"history":[u1,u2]},...] in filename + \"_processed.json\""""
from typing import List
import json 

filename = "LCCC-base_test"
with open(filename + ".json", encoding="utf-8", mode='r') as f:
    set = json.load(f)

if type(set[0]) == type([]):
    for i in range(len(set)):
        set[i] = {"history":set[i]}

with open(filename + "_processed.json", encoding="utf-8", mode='w') as f:
    f.write(json.dumps(set, ensure_ascii=False, indent=2)) 