from src.evaluate_support import compare, lexical_match
from src.readers import read_predictions, read_annotations

predictions = read_predictions("../data/metrics_e4re.json")
annotations = read_annotations("../data/Re-OIE2016.json")
results = compare(
    predicted=predictions,
    annotations=annotations,
    matching_function=lexical_match
    )
