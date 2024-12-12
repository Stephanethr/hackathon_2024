# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:31:14 2024

@author: PC
"""
from collections import Counter
import json

with open('test.json') as f:
    d = json.load(f)
    print(d)

    
def returnSite(typeList:list)->dict:
    count = Counter(typeList)
    print(count)
    
returnSite([1,1,1,2,2,4,4,4,4,4,4,3,5,5,5,5])