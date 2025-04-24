#!/bin/bash

source /data_st01/drug/itosho/.bash_profile
pyenv shell miniconda3-latest/envs/kmol

train_base_path="/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/finetuning_learning_rate/train/fup_human/*"
run_path="/data_st01/drug/itosho/kmol/"

cd $run_path

for folder in $train_base_path; do
    if [ -d "$folder" ]; then
        kmol train "$folder/config.json" > "$folder/train.txt" 2>&1
    fi
done

train_base_path="/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/finetuning_learning_rate/train/fup_rat/*"
for folder in $train_base_path; do
    if [ -d "$folder" ]; then
        kmol train "$folder/config.json" > "$folder/train.txt" 2>&1
    fi
done

test_base_path="/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/finetuning_learning_rate/test/fup_human/*"

for folder in $test_base_path; do
    if [ -d "$folder" ]; then
        kmol predict "$folder/config.json" > "$folder/pred.txt" 2>&1
    fi
done

test_base_path="/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/finetuning_learning_rate/test/fup_rat/*"

for folder in $test_base_path; do
    if [ -d "$folder" ]; then
        kmol predict "$folder/config.json" > "$folder/pred.txt" 2>&1
    fi
done

acc_path="/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/finetuning_learning_rate/evaluation.py"
python $acc_path