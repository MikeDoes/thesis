from src.benchie import Benchie
import json

# Define input files
gold_annotation_file = "evaluators/benchie/data/gold/benchie_gold_annotations_en.txt"
clausie_extractions_file = "evaluators/benchie/data/oie_systems_explicit_extractions/clausie_explicit.txt"

# Load gold annotations to BenchIE
benchie = Benchie()
benchie.load_gold_annotations(filename=gold_annotation_file)

# Add OIE systems extractions
#benchie.add_oie_system_extractions(oie_system_name="clauseie", filename=clausie_extractions_file)

number_epoch = 5
number_choices = 4

for i in range(number_choices):
  for j in range(number_epoch):
    e1_extractions_file = f"evaluators/benchie/data/oie_systems_explicit_extractions/e1_grid/e1_explicit_{i}_{j}.txt"
    benchie.add_oie_system_extractions(oie_system_name=f"t5_runs_{i}_{j}", filename=e1_extractions_file)

# Compute scores

benchie.compute_precision()

benchie.compute_recall()
benchie.compute_f1()
benchie.print_scores()

def load_dataset(path):
  with open(path) as f:
    data = json.load(f)
  return data


for metric in ['recall', 'precision', 'f1']:
  array = []
  path = f'visualiser/model_results/t_5_grid_{metric}.json'
  
  for i in range(number_choices):
    array += [[]]
    for j in range(number_epoch):
      model = f"t5_runs_{i}_{j}"
      array[i] += [str(benchie.scores[model].__dict__[metric])]

  with open(path, 'w') as f:
      json.dump(array, f)