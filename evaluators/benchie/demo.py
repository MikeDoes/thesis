from src.benchie import Benchie
import json

# Define input files
gold_annotation_file = "data/gold/2_annotators/benchie_gold_annotations_en.txt"
clausie_extractions_file = "data/oie_systems_explicit_extractions/clausie_explicit.txt"
minie_extractions_file = "data/oie_systems_explicit_extractions/minie_explicit.txt"
stanford_extractions_file = "data/oie_systems_explicit_extractions/stanford_explicit.txt"
openie6_extractions_file = "data/oie_systems_explicit_extractions/openie6_explicit.txt"
roie_t_extractions_file = "data/oie_systems_explicit_extractions/roi_t_explicit.txt"
roie_n_extractions_file = "data/oie_systems_explicit_extractions/roi_n_explicit.txt"
naive_extractions_file = "data/oie_systems_explicit_extractions/naive_oie_extractions.txt"
m2oie_extraction_file = "data/oie_systems_explicit_extractions/m2oie_en_explicit.txt"

# Load gold annotations to BenchIE
benchie = Benchie()
benchie.load_gold_annotations(filename=gold_annotation_file)

# Add OIE systems extractions
benchie.add_oie_system_extractions(oie_system_name="clausie", filename=clausie_extractions_file)
benchie.add_oie_system_extractions(oie_system_name="minie", filename=minie_extractions_file)
benchie.add_oie_system_extractions(oie_system_name="stanford", filename=stanford_extractions_file)
benchie.add_oie_system_extractions(oie_system_name="openie6", filename=openie6_extractions_file)
benchie.add_oie_system_extractions(oie_system_name="roie_t", filename=roie_t_extractions_file)
benchie.add_oie_system_extractions(oie_system_name="roie_n", filename=roie_n_extractions_file)
benchie.add_oie_system_extractions(oie_system_name="naive", filename=naive_extractions_file)
benchie.add_oie_system_extractions(oie_system_name="m2oie_en", filename=m2oie_extraction_file)

# Compute scores
benchie.compute_precision()
benchie.compute_recall()
benchie.compute_f1()

# Print scores
benchie.print_scores()