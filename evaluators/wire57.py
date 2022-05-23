from wire57_support import *

def main():
    
    
    reference = load_WiRe_annotations() # googledoc_manual_OIE_loader.load_WiRe_annotations()
    # dict of documents, each doc a list of sentences with a "tuples" attribute, which is the list of reference tuples
    # creates a dictionary here of key being id linking to tuples representing triplets
    # "TO 2" -> 2nd sentence
    # doc -> paragraph

    annotations = {}
    for doc in reference.value():
         for sentence in doc:
            annotations = {sentence['id'] : sentence['tuples'] }

    # Tuples is a triplet list (a bit more than triplets sometimes...) for each unique head and relation 

    # See the format of the reference in googledoc_manual_OIE_loader.py





    all_predictions = json.load(open("WiRe57_extractions_by_ollie_clausie_openie_stanford_minie_reverb_props-export.json"))
    # Dictionary which has sentence ids as keys
    # Values are predictions with "arg1", "rel", "arg2", "extractor", "score", "arg3+"

    #
    # The sentence is passed as an argument
    #annotations.keys -> TO 1, FI 12, 

    predictions_by_extractors = split_tuples_by_extractor(annotations.keys(), all_predictions)

    # Sorting the predictions by extractor name and into ordered sentences



    extractors = predictions_by_extractors.keys()
    
    reports = {}

    for extractor in extractors:
        extractor_predictions = predictions_by_extractors[extractor]
        report = ""
        
        metrics, raw_match_scores = eval_system(annotations, extractor_predictions)


        with open("raw_scores/"+extractor+"_prec_scores.dat", "w") as f:
            f.write(str(raw_match_scores[0]))
        with open("raw_scores/"+extractor+"_rec_scores.dat", "w") as f:
            f.write(str(raw_match_scores[1]))
        # Don't they have to index the 0th ? They do.
        prec, rec = metrics['precision'], metrics['recall']
        f1_score = f1(prec, rec)
        exactmatch_prec = metrics['exactmatches_precision'][0] / metrics['exactmatches_precision'][1]
        exactmatch_rec = metrics['exactmatches_recall'][0] / metrics['exactmatches_recall'][1]
        report += ("System {} prec/rec/f1: {:.1%} {:.1%} {:.3f}"
                   .format(extractor, prec, rec, f1_score))
        report += ("\nSystem {} prec/rec of matches only (non-matches): {:.0%} {:.0%} ({})"
                   .format(extractor, metrics['precision_of_matches'], metrics['recall_of_matches'], metrics['matches']))
        report += ("\n{} were exactly correct, out of {} predicted / the reference {}."
                   .format(metrics['exactmatches_precision'][0],
                           metrics['exactmatches_precision'][1], metrics['exactmatches_recall'][1]))
        report += ("\nExact-match prec/rec/f1: {:.1%} {:.1%} {:.3f}"
                   .format(exactmatch_prec, exactmatch_rec, f1(exactmatch_prec, exactmatch_rec)))
        reports[f1_score] = report
    sorted_reports = [a[1] for a in sorted(reports.items(), reverse = True)]
    print("\n"+"\n\n".join(sorted_reports))


if __name__ == "__main__":
    main()