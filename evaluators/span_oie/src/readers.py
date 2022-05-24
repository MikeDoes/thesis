# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 21:05:15 2018

@author: win 10
"""

from .oieReader import OieReader
from .extraction import Extraction
import json


def read_predictions(file_path):
    d = {}
    with open(file_path) as f:
        data = json.load(f)

    for i, _ in enumerate(data['text']):
        for extraction in data['extraction']:
            
            # Prepare the data to be entered into span_oie_2016 object 
            head = extraction['head']
            rel = extraction['relation'] #Quite sure that this is a string of the words based of looking at data structures from supervised_oie
            tails = extraction['tails'] #[] 
            confidence = 1
            text = data['text'][i]
            args = [head] + tails
            
            #for some reason head_pred_index is always -1 in this implementation
            extraction = Extraction(pred=rel, head_pred_index=-1, sent=text, confidence = float(confidence), args = args)
            d[text] = d.get(text, []) + [extraction]
            
    return d

from .oieReader import OieReader
from .extraction import Extraction
from _collections import defaultdict
import json

def read_annotations(fn):
    d = defaultdict(lambda: [])
    with open(fn) as fin:
        data = json.load(fin)
    for sentence in data:
        tuples = data[sentence]
        for t in tuples:
            if t["pred"].strip() == "<be>":
                rel = "[is]"
            else:
                rel = t["pred"].replace("<be> ","")
            confidence = 1
            
            # Here head_pred_index is None
            curExtraction = Extraction(pred = rel,
                                        head_pred_index = None,
                                        sent = sentence,
                                        confidence = float(confidence),
                                        index = None)
            if t["arg0"] != "":
                curExtraction.addArg(t["arg0"])
            if t["arg1"] != "":
                curExtraction.addArg(t["arg1"])
            if t["arg2"] != "":
                curExtraction.addArg(t["arg2"])
            if t["arg3"] != "":
                curExtraction.addArg(t["arg3"])
            if t["temp"] != "":
                curExtraction.addArg(t["temp"])
            if t["loc"] != "":
                curExtraction.addArg(t["loc"])
                
            d[sentence].append(curExtraction)
    return d

