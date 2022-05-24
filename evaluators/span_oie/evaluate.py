from evaluate_support import compare, lexical_match
from generalReader import read_predictions
from gold_relabel import read_annotations
from matcher import Matcher

predictions = read_predictions("metrics_e4re.json")
annotations = read_annotations("Re-OIE2016.json")
results = compare(
    predicted=predictions,
    annotations=annotations,
    matching_function=lexical_match
    )
