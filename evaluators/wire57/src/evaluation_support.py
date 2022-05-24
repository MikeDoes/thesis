import json 
def eval_system(annotations, predictions):
    results = {}
    # Get a manytuples-to-manytuples match-score for each sentence,
    # then gather the scores across sentences and compute the weighted-average
    for sentence_id, annoted_tuples in annotations.items():
        predicted_tuples = predictions.get(sentence_id, [])
        results[sentence_id] = sentence_match(annoted_tuples, predicted_tuples)


    prec_num, prec_denom = 0,0
    rec_num, rec_denom = 0,0
    exactmatches_precnum, exactmatches_precdenom = 0,0
    exactmatches_recnum, exactmatches_recdenom = 0,0
    tot_prec_of_matches, tot_rec_of_matches = 0, 0

    for s in results.values():
        prec_num += s['precision'][0]
        prec_denom += s['precision'][1]
        rec_num += s['recall'][0]
        rec_denom += s['recall'][1]
        exactmatches_precnum += s['exact_match_precision'][0]
        exactmatches_precdenom += s['exact_match_precision'][1]
        exactmatches_recnum += s['exact_match_recall'][0]
        exactmatches_recdenom += s['exact_match_recall'][1]
        tot_prec_of_matches += sum(s['precision_of_matches'])
        tot_rec_of_matches += sum(s['recall_of_matches'])
    precision_scores = [v for s in results.values() for v in s['precision_of_matches']]
    recall_scores = [v for s in results.values() for v in s['recall_of_matches']]
    raw_match_scores = [precision_scores, recall_scores]
    matches = len(precision_scores)
    metrics = {
        'precision' : prec_num / prec_denom,
        'recall' : rec_num / rec_denom,
        # 'non-matches' : exactmatches_precdenom - matches,
        'matches' : matches,
        'precision_of_matches' : tot_prec_of_matches / matches,
        'recall_of_matches' : tot_rec_of_matches / matches,
        'exactmatches_precision' : [exactmatches_precnum, exactmatches_precdenom],
        'exactmatches_recall' : [exactmatches_recnum, exactmatches_recdenom]
    }
    return metrics, raw_match_scores


# TODO:
# - Implement half points for part-misplaced words.
# - Deal with prepositions possibly being the first token of an arg, especially for arg2.
# - Permutation of arg 2+
#   > It's fully ok for "any" prep to be last word of ref_rel or first_word of pred_arg


def avg(l):
    return sum(l)/len(l)
        
def f1(prec, rec):
    try:
        return 2*prec*rec / (prec+rec)
    except ZeroDivisionError:
        return 0

def empty_matrix(rows, columns):
    matrix = []
    for __ in range(rows):
        matrix += [[None for _ in range(columns)]]
    return matrix

def sentence_match(annotations, predicted):
    """For a given sentence, compute tuple-tuple matching scores, and gather them at the sentence level. Return metrics."""
    # score, maximum_score = 0, len(annotations)
    rows = len(annotations)
    columns = len(predicted)

    exact_match_matrix = empty_matrix(rows, columns)
    partial_match_matrix = empty_matrix(rows, columns)


    for i, annotation in enumerate(annotations):
        for j, prediction in enumerate(predicted):
            exact_match_matrix[i][j] = tuple_exact_match(prediction, annotation) #True false matrix
            partial_match_matrix[i][j] = tuple_match(prediction, annotation) # this is a pair [prec,rec] or False

            
    metrics = aggregate_scores_greedily(partial_match_matrix)
    exact_match_metrics = aggregate_exact_matches(exact_match_matrix)

    metrics['exact_match_precision'] = exact_match_metrics['precision']
    metrics['exact_match_recall'] = exact_match_metrics['recall']

    return  metrics


def aggregate_exact_matches(match_matrix):
    
    # For this agregation task, no predicted tuple can exact-match two annotations
    # ones, so it's easy, look at lines and columns looking for OR-total booleans.
    recall = [0, len(match_matrix)]
    for annotations_matches in match_matrix:
        recall[0] += sum([any(annotations_matches)])
    
    # removed the extra , 0
    # ^ this is [3,5] for "3 out of 5", to be lumped together later.
    number_of_predictions = len(match_matrix[0])
    if number_of_predictions == 0:
        precision = [0, 0] # N/A

    else:
        precision = [0, number_of_predictions]
        for i in range(number_of_predictions):
            precision[0] += sum([any([annotation[i] for annotation in match_matrix])])

    
    # f1 = 2 * precision * recall / (precision + recall)
    metrics = {'precision' : precision,
               'recall' : recall}
    return metrics

def aggregate_scores_greedily(partial_match_matrix):
    # Greedy match: pick the prediction/annotations match with the best f1 and exclude
    # them both, until nothing left matches. Each entry is [prec, rec]
    # Returns precision and recall as score-and-denominator pairs.
    matches = []

    while True:
        max_s = 0
        annotations, pred = None, None
        
        for i, _ in enumerate(partial_match_matrix):
            if i in [match[0] for match in matches]:
                # Already taken annotation
                continue

            for j, pred_s in enumerate(partial_match_matrix[i]):
                if j in [match[1] for match in matches]:
                    # Already taken prediction
                    continue


                # What's max_score. Not 0 if there are matches
                if pred_s and f1(*pred_s) > max_s:
                    max_s = f1(*pred_s)
                    annotations = i
                    pred = j

        if max_s == 0:
            # No good matches found. Therefore it must be over?
            break

        #Appends the best match to the matrix
        matches.append([annotations, pred])

    # Now that matches are determined, compute final scores.
    prec_scores = [partial_match_matrix[i][j][0] for i,j in matches]
    rec_scores = [partial_match_matrix[i][j][1] for i,j in matches]

    total_prec = sum(prec_scores)
    total_rec = sum(rec_scores)
    scoring_metrics = {"precision" : [total_prec, len(partial_match_matrix[0])],
                       "recall" : [total_rec, len(partial_match_matrix)],
                       "precision_of_matches" : prec_scores,
                       "recall_of_matches" : rec_scores
    }
    # print(scoring_metrics)
    return scoring_metrics



def part_to_string(p):
    return " ".join(p['words'])
def annotations_to_text(annotated_tuple):
    text = " ; ".join([part_to_string(annotated_tuple['arg1']), part_to_string(annotated_tuple['rel']), part_to_string(gt['arg2'])])
    if gt['arg3+']:
        text += " ; " + " ; ".join(gt['arg3+'])
    return text
        

def tuple_exact_match(t, gt):
    """Without resolving coref and WITH the need to hallucinate humanly infered
words, does the tuple match the reference ? Returns a boolean."""
    for part in ['arg1', 'rel', 'arg2']:
        if not t[part] == ' '.join(gt[part]['words']):
            # This purposedly ignores that some of the gt words are 'inf'
            # print("Predicted '{}' is different from reference '{}'".format(t[part], ' '.join(gt[part]['words'])))
            return False
    if gt['arg3+']:
        if not t.get('arg3+', False):
            return False
        for i, p in enumerate(gt['arg3+']):
            if t['arg3+'][i] != ' '.join(p['words']):
                return False
    return True

"""
Wire57 tuples are built like so:
t = {"attrib/spec?" : attrib,
     "arg1" : {'text' : arg1, 'words': arg1_w, "words_indexes" : arg1_ind,
               'dc_text' : arg1dc, 'decorefed_words' : arg1dc_w, 'decorefed_indexes' : arg1dc_ind},
     "rel" : {'text' : rel, 'words': rel_w, "words_indexes" : rel_ind},
     "arg2" : {'text' : arg2, 'words': arg2_w, "words_indexes" : arg2_ind,
               'dc_text' : arg2dc, 'decorefed_words' : arg2dc_w, 'decorefed_indexes' : arg2dc_ind},
     "arg3+" : [{'text' : a,
                 'words' : arg3dat['raw_w'][i], 'words_indexes' : arg3dat['raw_ind'][i],
                 'decorefed_words' : arg3dat['dc_w'][i],
                 'decorefed_indexes' : arg3dat['dc_ind'][i]}
                for i,a in enumerate(arg3s)]}
"""
def tuple_match(t, gt):
    """t is a predicted tuple, gt is the gold tuple. How well do they match ?
Yields precision and recall scores, a pair of non-zero values, if it's a match, and False if it's not.
    """
    precision = [0, 0] # 0 out of 0 predicted words match
    recall = [0, 0] # 0 out of 0 reference words match
    # If, for each part, any word is the same as a reference word, then it's a match.
    for part in ['arg1', 'rel', 'arg2']:
        predicted_words = t[part].split()
        gold_words = gt[part]['words']
        gold_indexes = gt[part]['words_indexes']
        gold_num_realwords = sum([i != "inf" for i in gold_indexes], 0)
        gold_is_fully_inferred = all([i == "inf" for i in gold_indexes])
        if not predicted_words:
            if gold_words and not gold_is_fully_inferred:
                return False
            else: continue
        matching_words = sum(1 for w in predicted_words if w in gold_words)
        if matching_words == 0 and not gold_is_fully_inferred:
            return False # t <-> gt is not a match
        precision[0] += matching_words
        precision[1] += len(predicted_words)
        # Currently this slightly penalises systems when the reference
        # reformulates the sentence words, because the reformulation doesn't
        # match the predicted word. It's a one-wrong-word penalty to precision,
        # to all systems that correctly extracted the reformulated word.
        recall[0] += matching_words
        recall[1] += gold_num_realwords # len(gold_words) would include inferred words, unfairly to systems

    if gt['arg3+']:
        for i, a in enumerate(gt['arg3+']):
            gold_words = a['words']
            gold_num_realwords = sum([i != "inf" for i in a['words_indexes']], 0)
            assert gold_num_realwords <= len(gold_words)
            recall[1] += gold_num_realwords
            if t.get("arg3+", False) and len(t['arg3+'])>i:
                predicted_words = t['arg3+'][i].split()
                matching_words = sum(1 for w in predicted_words if w in gold_words)
                precision[0] += matching_words
                precision[1] += len(predicted_words)
                recall[0] += matching_words
            else:
                # 0 matching words and precision is unchanged
                pass
    prec = precision[0] / precision[1]
    rec = recall[0] / recall[1]
    return [prec, rec]

def split_tuples_by_extractor(gold, tuples):
    systems = sorted(list(set(t['extractor'] for st in tuples.values() for t in st)))
    predictions_by_OIE = {e : {} for e in systems}
    for s in gold:
        for t in tuples[s]:
            if s in predictions_by_OIE[t['extractor']]:
                predictions_by_OIE[t['extractor']][s].append(t)
            else:
                predictions_by_OIE[t['extractor']][s] = [t]
    return predictions_by_OIE




def load_WiRe_annotations():
    save_path = "../data/WiRe57_343-manual-oie.json"
    annotations = json.load(open(save_path))
    return annotations

def str_list(thing):
    return "\n".join([str(s) for s in thing])