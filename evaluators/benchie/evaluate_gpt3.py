from src.benchie import Benchie
import json

# Define input files
gold_annotation_file = "evaluators/benchie/data/gold/benchie_gold_annotations_en.txt"
#gold_annotation_file = "evaluators/benchie/data/gold/benchie_gold_annotations_en_test.txt"

#clausie_extractions_file = "evaluators/benchie/data/oie_systems_explicit_extractions/clausie_explicit.txt"

# Load gold annotations to BenchIE
benchie = Benchie()
benchie.load_gold_annotations(filename=gold_annotation_file)

# Add OIE systems extractions
#benchie.add_oie_system_extractions(oie_system_name="clauseie", filename=clausie_extractions_file)



number_epoch = 3
for i in range(number_epoch):
    e1_extractions_file = f"evaluators/benchie/data/oie_systems_explicit_extractions/e4_explicit_choices_test_{i}.txt"
    benchie.add_oie_system_extractions(oie_system_name=f"gpt_runs_{i}", filename=e1_extractions_file)

#benchie.add_oie_system_extractions(oie_system_name=f"clause", filename='evaluators/benchie/data/oie_systems_explicit_extractions/e4_explicit_choices_re_bench_test.txt')


# Compute scores
benchie.add_oie_system_extractions(oie_system_name="openie6", filename='evaluators/benchie/data/oie_systems_explicit_extractions/openie6_explicit.txt')

benchie.compute_precision()

benchie.compute_recall()
benchie.compute_f1()
benchie.print_scores()

def load_dataset(path):
  with open(path) as f:
    data = json.load(f)
  return data

path = 'visualiser/model_results/gpt3_benchie_test_by_runs.json'
data = load_dataset(path)

for model in benchie.scores:
    for metric, value in benchie.scores[model].__dict__.items():
        data[model.split('_')[-1]][metric] = value


with open(path, 'w') as f:
    json.dump(data, f)