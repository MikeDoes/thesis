# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 21:05:15 2018

@author: win 10
"""

from oieReader import OieReader
from extraction import Extraction
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


# So this is a poor re-implementation or I don't understand this relation aspect
"""class GeneralReader(OieReader):
    
    def __init__(self):
        self.name = 'General'
    
    def read(self, fn):
        d = {}
        with open(fn) as fin:
            for line in fin:
                data = line.strip().split('\t')
                if len(data) >= 4:
                    arg1 = data[3]
                    rel = data[2]
                    arg_else = data[4:]
                    confidence = data[1]
                    text = data[0]
                    
                    curExtraction = Extraction(pred = rel, head_pred_index=-1, sent = text, confidence = float(confidence))
                    curExtraction.addArg(arg1)
                    for arg in arg_else:
                        curExtraction.addArg(arg)
                    d[text] = d.get(text, []) + [curExtraction]
        self.oie = d
        
if __name__ == "__main__":
    fn = "../data/other_systems/openie4_test.txt"
    reader = GeneralReader()
    reader.read(fn)
    for key in reader.oie:
        print(key)
        print(reader.oie[key][0].pred)
        print(reader.oie[key][0].args)
        print(reader.oie[key][0].confidence)
"""        