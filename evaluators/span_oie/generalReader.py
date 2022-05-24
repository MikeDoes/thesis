# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 21:05:15 2018

@author: win 10
"""

from oieReader import OieReader
from extraction import Extraction
import json

def read_predicted(fn):
    d = {}
    with open(fn) as f:
        data = json.load(f)
    
    for i, _ in enumerate(data['text']):
        for extraction in data['extraction']:
            
            head = extraction['head']
            # Rel is the relation
            rel = extraction['relation']
            tails = extraction['tails'] #[] 
            confidence = 1
            text = data['text'][i]
            
            curExtraction = Extraction(pred = rel, head_pred_index=-1, sent = text, confidence = float(confidence))
            # This is the head?
            curExtraction.addArg(head)
            
            # These are the tails
            for tail in tails:
                curExtraction.addArg(tail)

            d[text] = d.get(text, []) + [curExtraction]
        
        
    return d
        
        