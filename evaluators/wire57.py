from wire57_support import *

def main():
    reference = load_WiRe_annotations() # googledoc_manual_OIE_loader.load_WiRe_annotations()
    # dict of documents, each doc a list of sents with a "tuples" attribute, which is the list of reference tuples
    gold = {s['id'] : s['tuples'] for doc in reference.values() for s in doc}
    # See the format of the reference in googledoc_manual_OIE_loader.py
    all_predictions = json.load(open("WiRe57_extractions_by_ollie_clausie_openie_stanford_minie_reverb_props-export.json"))
    predictions_by_OIE = split_tuples_by_extractor(gold.keys(), all_predictions)
    systems = predictions_by_OIE.keys()
    
    reports = {}
    for e in systems:
        report = ""
        metrics, raw_match_scores = eval_system(gold, predictions_by_OIE[e])
        with open("raw_scores/"+e+"_prec_scores.dat", "w") as f:
            f.write(str(raw_match_scores[0]))
        with open("raw_scores/"+e+"_rec_scores.dat", "w") as f:
            f.write(str(raw_match_scores[1]))
        prec, rec = metrics['precision'], metrics['recall']
        f1_score = f1(prec, rec)
        exactmatch_prec = metrics['exactmatches_precision'][0] / metrics['exactmatches_precision'][1]
        exactmatch_rec = metrics['exactmatches_recall'][0] / metrics['exactmatches_recall'][1]
        report += ("System {} prec/rec/f1: {:.1%} {:.1%} {:.3f}"
                   .format(e, prec, rec, f1_score))
        report += ("\nSystem {} prec/rec of matches only (non-matches): {:.0%} {:.0%} ({})"
                   .format(e, metrics['precision_of_matches'], metrics['recall_of_matches'], metrics['matches']))
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