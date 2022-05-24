# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 21:05:15 2018

@author: win 10
"""

from oieReader import OieReader
from extraction import Extraction
import json

class GeneralReader(OieReader):
    
    def __init__(self):
        self.name = 'General'
    
    def read(self, fn):
        d = {}
        def load_dataset(path):
            with open(path) as f:
                data = json.load(f)
            return data
        
        train_data = load_dataset('datasets/supervised_oie/parsed/train_sequence_sequences.json')
        test_data = load_dataset('datasets/span_oie2016/parsed/test_sequence_sequences.json')
        
        with open(fn) as fin:
            for line in fin:
                data = line.strip().split('\t')
                if len(data) >= 4:
                    arg1 = data[3]
                    rel = data[2]
                    arg_else = data[4:]
                    confidence = 1
                    text = data[0]
                    
                    # Sentences need to be for 
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
        