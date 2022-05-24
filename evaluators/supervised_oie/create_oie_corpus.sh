#!/bin/bash
set -e
clear
mkdir -p ./oie_corpus/newswire
mkdir -p ./oie_corpus/wiki
echo "Extracting from newswire..."
echo "dev..."
python ./qa_to_oie.py --in ./QASRL-full/newswire/propbank.dev.qa --out ./oie_corpus/newswire/propbank.dev.oie --conll=./oie_corpus/newswire/propbank.dev.oie.conll --dist=./question_distributions/dist_wh_sbj_obj1.json --oieinput=./raw_sentences/newswire/propbank.dev.txt
echo "train..."
python ./qa_to_oie.py --in ./QASRL-full/newswire/propbank.train.qa --out ./oie_corpus/newswire/propbank.train.oie --conll=./oie_corpus/newswire/propbank.train.oie.conll --dist=./question_distributions/dist_wh_sbj_obj1.json --oieinput=./raw_sentences/newswire/propbank.train.txt
echo "test..."
python ./qa_to_oie.py --in ./QASRL-full/newswire/propbank.test.qa --out ./oie_corpus/newswire/propbank.test.oie --conll=./oie_corpus/newswire/propbank.test.oie.conll --dist=./question_distributions/dist_wh_sbj_obj1.json --oieinput=./raw_sentences/newswire/propbank.test.txt
echo "Extracting from wiki..."
echo "dev..."
python ./qa_to_oie.py --in ./QASRL-full/wiki/wiki1.dev.qa --out ./oie_corpus/wiki/wiki1.dev.oie --conll=./oie_corpus/wiki/wiki1.dev.oie.conll --dist=./question_distributions/dist_wh_sbj_obj1.json --oieinput=./raw_sentences/wiki/wiki1.dev.txt
echo "train..."
python ./qa_to_oie.py --in ./QASRL-full/wiki/wiki1.train.qa --out ./oie_corpus/wiki/wiki1.train.oie --conll=./oie_corpus/wiki/wiki1.train.oie.conll --dist=./question_distributions/dist_wh_sbj_obj1.json --oieinput=./raw_sentences/wiki/wiki1.train.txt
echo "test..."
python ./qa_to_oie.py --in ./QASRL-full/wiki/wiki1.test.qa --out ./oie_corpus/wiki/wiki1.test.oie --conll=./oie_corpus/wiki/wiki1.test.oie.conll --dist=./question_distributions/dist_wh_sbj_obj1.json  --oieinput=./raw_sentences/wiki/wiki1.test.txt
echo "Concatenating global train/dev/test"
cat ./oie_corpus/newswire/propbank.dev.oie ./oie_corpus/wiki/wiki1.dev.oie > ./oie_corpus/dev.oie
cat ./oie_corpus/newswire/propbank.train.oie ./oie_corpus/wiki/wiki1.train.oie > ./oie_corpus/train.oie
cat ./oie_corpus/newswire/propbank.test.oie ./oie_corpus/wiki/wiki1.test.oie > ./oie_corpus/test.oie
cat ./oie_corpus/dev.oie ./oie_corpus/train.oie ./oie_corpus/test.oie > ./oie_corpus/all.oie

# Concatenating conlls
python ../src/common/concat_dfs.py \
       --df1=./oie_corpus/newswire/propbank.dev.oie.conll \
       --df2=./oie_corpus/wiki/wiki1.dev.oie.conll \
       --out=./oie_corpus/dev.oie.conll


python ../src/common/concat_dfs.py \
       --df1=./oie_corpus/newswire/propbank.train.oie.conll \
       --df2=./oie_corpus/wiki/wiki1.train.oie.conll \
       --out=./oie_corpus/train.oie.conll

python ../src/common/concat_dfs.py \
       --df1=./oie_corpus/newswire/propbank.test.oie.conll \
       --df2=./oie_corpus/wiki/wiki1.test.oie.conll \
       --out=./oie_corpus/test.oie.conll


python ../src/common/concat_dfs.py \
       --df1=./oie_corpus/dev.oie.conll \
       --df2=./oie_corpus/train.oie.conll \
       --out=./oie_corpus/all.oie.conll

python ../src/common/concat_dfs.py \
       --df2=./oie_corpus/all.oie.conll \
       --df1=./oie_corpus/test.oie.conll \
       --out=./oie_corpus/all.oie.conll

# Updating data folder
echo "Updating data folder with the new files"
cp -v ./oie_corpus/*.oie.conll ../data/
cp -v ./oie_corpus/newswire/*.oie.conll ../data/newswire/
cp -v ./oie_corpus/wiki/*.oie.conll ../data/wiki/

echo "DONE"
