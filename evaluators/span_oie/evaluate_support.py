import string
import numpy as np
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import auc
import re
import logging
import sys
logging.basicConfig(level = logging.INFO)

from operator import itemgetter

def compare(predicted, annotations, matching_function):
    ''' Compare gold against predicted using a specified matching function.
        Outputs PR curve to "result.txt" '''

    y_true = []
    y_scores = []
    errors = []

    correctTotal = 0
    unmatchedCount = 0
    predicted = normalizeDict(predicted)
    annotations = normalizeDict(annotations)

    for sent, annotation_exctractions in annotations.items():
        if sent not in predicted:
            # The extractor didn't find any extractions for this sentence
            for annotation_extrction in annotation_exctractions:
                unmatchedCount += len(annotation_exctractions)
                correctTotal += len(annotation_exctractions)
            continue

        predictedExtractions = predicted[sent]

        for annotation_extrction in annotation_exctractions:
            correctTotal += 1
            found = False

            for predictedEx in predictedExtractions:
                if "result.txt" in predictedEx.matched:
                    # This predicted extraction was already matched against a gold extraction
                    # Don't allow to match it again
                    continue

                if matching_function(annotation_extrction,
                                predictedEx):

                    y_true.append(1)
                    y_scores.append(predictedEx.confidence)
                    predictedEx.matched.append("result.txt")
                    found = True
                    break

            if not found:
                errors.append(annotation_extrction.index)
                unmatchedCount += 1

        for predictedEx in [x for x in predictedExtractions if ("result.txt" not in x.matched)]:
            # Add false positives
            y_true.append(0)
            y_scores.append(predictedEx.confidence)

    y_true = y_true
    y_scores = y_scores

    # recall on y_true, y  (r')_scores computes |covered by extractor| / |True in what's covered by extractor|
    # to get to true recall we do:
    # r' * (|True in what's covered by extractor| / |True in gold|) = |true in what's covered| / |true in gold|
    (p, r), optimal = prCurve(np.array(y_true), np.array(y_scores),
                                        recallMultiplier = ((correctTotal - unmatchedCount)/float(correctTotal)))
    print("AUC: {}\n Optimal (precision, recall, F1, threshold): {}".format(auc(r, p),
                                                                                    optimal))

    # Write error log to file
    if "error.txt":
        logging.info("Writing {} error indices to {}".format(len(errors),
                                                                "error.txt"))
        with open("error.txt", 'w') as fout:
            fout.write('\n'.join([str(error)
                                    for error
                                    in errors]) + '\n')

    # write PR to file
    with open("result.txt", 'w') as fout:
        fout.write('{0}\t{1}\n'.format("Precision", "Recall"))
        for cur_p, cur_r in sorted(zip(p, r), key = lambda cur: cur[1]):
            fout.write('{0}\t{1}\n'.format(cur_p, cur_r))

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
def normalizeDict(d):
    return dict([(normalizeKey(k), v) for k, v in d.items()])

def normalizeKey(k):
    return removePunct(PTB_unescape(k.replace(' ','')))

def PTB_escape(s):
    for u, e in PTB_ESCAPES:
        s = s.replace(u, e)
    return s

def PTB_unescape(s):
    for u, e in PTB_ESCAPES:
        s = s.replace(e, u)
    return s

def removePunct(s):
    return regex.sub('', s)

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

def lexical_match(annotation_exctraction, prediction_extraction, LEXICAL_THRESHOLD=0.5):
        annotation_exctraction = annotation_exctraction.bow().split(' ')
        prediction_extraction = prediction_extraction.bow().split(' ')
        count = 0

        for w1 in annotation_exctraction:
            for w2 in prediction_extraction:
                if w1 == w2:
                    count += 1

        # We check how well does the extraction lexically cover the reference
        # Note: this is somewhat lenient as it doesn't penalize the extraction for
        #       being too long
        coverage = float(count) / len(annotation_exctraction)


        return coverage > LEXICAL_THRESHOLD