parentdir="$(dirname "$(pwd)")"
dataset="/datasets/financial_alphabet_2021/"
dataset_dir=$parentdir$dataset
cp -r $dataset_dir unlabeled_data/financial_alphabet_2021/
flask run -h 0.0.0.0