#!/bin/bash

source ~/.bashrc
conda activate kmol

run_path="/data_st01/drug/itosho/kmol/"

cd $run_path

train_base_path="/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/singletask/train/*/*"
for folder in $train_base_path; do
    if [ -d "$folder" ]; then
        kmol train "$folder/config.json" > "$folder/train.txt" 2>&1
    fi
done

test_base_path="/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/singletask/test/*/*"
for folder in $test_base_path; do
    if [ -d "$folder" ]; then
        kmol predict "$folder/config.json" > "$folder/pred.txt" 2>&1
    fi
done

acc_path="/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/singletask/evaluation.py"
python $acc_path


