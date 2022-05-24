#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 19:24:30 2018

@author: longzhan
"""

import string
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc
import re
import logging
logging.basicConfig(level = logging.INFO)

from generalReader import read_predicted

from annotation_reader import AnnotationReader
from matcher import Matcher
from operator import itemgetter

class Benchmark:
    ''' Compare the gold OIE dataset against a predicted equivalent '''
    def __init__(self, gold_filename):
        ''' Load annotations for Open IE, this will serve to compare against using the compare function '''

        gr = AnnotationReader()
        gr.read(gold_filename)
        self.annotations = gr.oie

    def compare(self, predicted, matchingFunc, output_fn, error_file = None):
        ''' Compare annotated against predicted using a specified matching function.
            Outputs PR curve to output_fn '''

        y_true = []
        y_scores = []
        errors = []

        correctTotal = 0
        unmatchedCount = 0
        predicted = self.normalizeDict(predicted)
        annotations = self.normalizeDict(self.annotations)

        for sent, sentence_level_annotations in annotations.items():
            if sent not in predicted:
                # The extractor didn't find any extractions for this sentence. So this is the extractor of extractions. Couldn't be more forward than this.
                for _ in sentence_level_annotations:
                    unmatchedCount += len(sentence_level_annotations)
                    correctTotal += len(sentence_level_annotations)
                continue

            sentence_level_predictions = predicted[sent]

            for annotation in sentence_level_annotations:
                correctTotal += 1
                found = False

                for prediction in sentence_level_predictions:
                    if output_fn in prediction.matched:
                        # This predicted extraction was already matched against a gold extraction
                        # Don't allow to match it again
                        continue

                    if matchingFunc(annotation,
                                    prediction,
                                    ignoreStopwords = True,
                                    ignoreCase = True):

                        y_true.append(1)
                        y_scores.append(prediction.confidence)
                        prediction.matched.append(output_fn)
                        found = True
                        break

                if not found:
                    errors.append(annotation.index)
                    unmatchedCount += 1

            for prediction in [x for x in sentence_level_predictions if (output_fn not in x.matched)]:
                # Add false positives
                y_true.append(0)
                y_scores.append(prediction.confidence)
        # ???
        y_true = y_true
        y_scores = y_scores

        # recall on y_true, y  (r')_scores computes |covered by extractor| / |True in what's covered by extractor|
        # to get to true recall we do:
        # r' * (|True in what's covered by extractor| / |True in gold|) = |true in what's covered| / |true in gold|
        (p, r), optimal = Benchmark.prCurve(np.array(y_true), np.array(y_scores),
                                            recallMultiplier = ((correctTotal - unmatchedCount)/float(correctTotal)))
        print("AUC: {}\n Optimal (precision, recall, F1, threshold): {}".format(auc(r, p),
                                                                                       optimal))

        # Write error log to file
        if error_file:
            logging.info("Writing {} error indices to {}".format(len(errors),
                                                                 error_file))
            with open(error_file, 'w') as fout:
                fout.write('\n'.join([str(error)
                                     for error
                                      in errors]) + '\n')

        # write PR to file
        with open(output_fn, 'w') as fout:
            fout.write('{0}\t{1}\n'.format("Precision", "Recall"))
            for cur_p, cur_r in sorted(zip(p, r), key = lambda cur: cur[1]):
                fout.write('{0}\t{1}\n'.format(cur_p, cur_r))

    @staticmethod
    def prCurve(y_true, y_scores, recallMultiplier):
        # Recall multiplier - accounts for the percentage examples unreached
        # Return (precision [list], recall[list]), (Optimal F1, Optimal threshold)
        y_scores = [score \
                    if not (np.isnan(score) or (not np.isfinite(score))) \
                    else 0
                    for score in y_scores]
        
        precision_ls, recall_ls, thresholds = precision_recall_curve(y_true, y_scores)
        recall_ls = recall_ls * recallMultiplier
        optimal = max([(precision, recall, f_beta(precision, recall, beta = 1), threshold)
                       for ((precision, recall), threshold)
                       in zip(zip(precision_ls[:-1], recall_ls[:-1]),
                              thresholds)],
                      key = itemgetter(2))  # Sort by f1 score

        return ((precision_ls, recall_ls),
                optimal)

    # Helper functions:
    @staticmethod
    def normalizeDict(d):
        return dict([(Benchmark.normalizeKey(k), v) for k, v in d.items()])

    @staticmethod
    def normalizeKey(k):
        return Benchmark.removePunct(Benchmark.PTB_unescape(k.replace(' ','')))

    @staticmethod
    def PTB_escape(s):
        for u, e in Benchmark.PTB_ESCAPES:
            s = s.replace(u, e)
        return s

    @staticmethod
    def PTB_unescape(s):
        for u, e in Benchmark.PTB_ESCAPES:
            s = s.replace(e, u)
        return s

    @staticmethod
    def removePunct(s):
        return Benchmark.regex.sub('', s)

    # CONSTANTS
    regex = re.compile('[%s]' % re.escape(string.punctuation))

    # Penn treebank bracket escapes
    # Taken from: https://github.com/nlplab/brat/blob/master/server/src/gtbtokenize.py
    PTB_ESCAPES = [('(', '-LRB-'),
                   (')', '-RRB-'),
                   ('[', '-LSB-'),
                   (']', '-RSB-'),
                   ('{', '-LCB-'),
                   ('}', '-RCB-'),]


def f_beta(precision, recall, beta = 1):
    """
    Get F_beta score from precision and recall.
    """
    beta = float(beta) # Make sure that results are in float
    return (1 + pow(beta, 2)) * (precision * recall) / ((pow(beta, 2) * precision) + recall)


f1 = lambda precision, recall: f_beta(precision, recall, beta = 1)


if __name__ == '__main__':
    
    matchingFunc = Matcher.lexicalMatch
    error_fn = "error.txt"
    out_path = "results" # output file
    b = Benchmark("Re-OIE2016.json")  # to choose whether to use OIE2016 or Re-OIE2016
    predictions = read_predicted("metrics_e4re.json") # input file

    b.compare(predicted = predictions,
              matchingFunc = matchingFunc,
              output_fn = out_path,
              error_file = error_fn)
