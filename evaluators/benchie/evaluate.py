from src.benchie import Benchie

# Define input files
gold_annotation_file = "evaluators/benchie/data/gold/benchie_gold_annotations_en.txt"
e4_extractions_file = "evaluators/benchie/data/oie_systems_explicit_extractions/e4_explicit.txt"
clausie_extractions_file = "evaluators/benchie/data/oie_systems_explicit_extractions/clausie_explicit.txt"

# Load gold annotations to BenchIE
benchie = Benchie()
benchie.load_gold_annotations(filename=gold_annotation_file)

# Add OIE systems extractions
benchie.add_oie_system_extractions(oie_system_name="clauseie", filename=clausie_extractions_file)
#benchie.add_oie_system_extractions(oie_system_name="gpt3", filename=e4_extractions_file)

# Compute scores
benchie.compute_precision()
benchie.compute_recall()
benchie.compute_f1()
benchie.print_scores()