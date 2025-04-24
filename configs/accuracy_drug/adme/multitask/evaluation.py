import os
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy.stats import pearsonr
import glob

def evaluation_score(file_path, target, ground_truth_path):
    df = pd.read_csv(file_path)
    ground_truth_df = pd.read_csv(ground_truth_path)
    ground_truth = ground_truth_df["value"].str.strip('[]').astype(float)[:len(df)].values
    predictions = df[f'{target}'].values
    
    # Calculate metrics
    r2 = r2_score(ground_truth, predictions)
    mae = mean_absolute_error(ground_truth, predictions)
    rmse = np.sqrt(mean_squared_error(ground_truth, predictions))
    
    # Calculate Pearson correlation coefficient
    pearson_corr, _ = pearsonr(ground_truth, predictions)
    
    return {'R2': r2, 'MAE': mae, 'RMSE': rmse, 'Pearson': pearson_corr}

# Replace 'your_directory_path' with the path to the directory containing the folders
adme_list = ["clint","fe","fubrain","fup_human","fup_rat","ner_human","papp_caco2","papp_llc","rb_rat","sol"]
adme_base_path = '/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/multitask/test/'
gt_base_path = "/data_st01/drug/itosho/ADMET/dataset/all_train_data_2022/standardize-drug_list/ADME/five_fold"
folders = ["itr1","itr2","itr3","itr4","itr5"]

results = []

for i, adme in enumerate(adme_list):
    r2_values, mae_values, rmse_values, pearson_values, length_list = [], [], [], [], []
    for folder in folders:
        file_path = os.path.join(adme_base_path, adme, folder, 'predictions.csv')
        gt_path = os.path.join(gt_base_path, folder, 'test', f'{adme}.csv')
        if os.path.exists(file_path):
            values = evaluation_score(file_path, i, gt_path)
            r2_values.append(values['R2'])
            mae_values.append(values['MAE'])
            rmse_values.append(values['RMSE'])
            pearson_values.append(values['Pearson'])
            df = pd.read_csv(file_path)
            length = len(df)
            length_list.append(length)
        else:
            print(f"File not found: {file_path}")
    if r2_values and mae_values and rmse_values and pearson_values:
        mean_r2, std_r2 = np.mean(r2_values), np.std(r2_values)
        mean_mae, std_mae = np.mean(mae_values), np.std(mae_values)
        mean_rmse, std_rmse = np.mean(rmse_values), np.std(rmse_values)
        mean_pearson, std_pearson = np.mean(pearson_values), np.std(pearson_values)
        results.append({
            'adme_parameter': adme,
            'mean_r2': mean_r2,
            'std_r2': std_r2,
            'mean_mae': mean_mae,
            'std_mae': std_mae,
            'mean_rmse': mean_rmse,
            'std_rmse': std_rmse,
            'mean_pearson': mean_pearson,
            'std_pearson': std_pearson,
            'length': length_list
        })

# Save results to a file
with open('/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/multitask/evaluation.txt', 'w') as file:
    for result in results:
        file.write(f"Path: {result['adme_parameter']}\n")
        file.write(f"R2: mean = {result['mean_r2']}, std = {result['std_r2']}\n")
        file.write(f"MAE: mean = {result['mean_mae']}, std = {result['std_mae']}\n")
        file.write(f"RMSE: mean = {result['mean_rmse']}, std = {result['std_rmse']}\n")
        file.write(f"Pearson: mean = {result['mean_pearson']}, std = {result['std_pearson']}\n\n")
        file.write(f"data size: {result['length']}\n\n")

# Save results to a csv file
df = pd.DataFrame(results)
df.to_csv('/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/multitask/evaluation.csv', index=False)
