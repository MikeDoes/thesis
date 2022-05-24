from src.benchie import Benchie

# Define input files
gold_annotation_file = "evaluators/benchie/data/gold/2_annotators/benchie_gold_annotations_en.txt"
clausie_extractions_file = "data/oie_systems_explicit_extractions/clausie_explicit.txt"

# Load gold annotations to BenchIE
benchie = Benchie()
benchie.load_gold_annotations(filename=gold_annotation_file)

# Add OIE systems extractions
benchie.add_oie_system_extractions(oie_system_name="gpt3", filename=clausie_extractions_file)

# Compute scores
benchie.compute_precision()
benchie.compute_recall()
benchie.compute_f1()
benchie.print_scores()