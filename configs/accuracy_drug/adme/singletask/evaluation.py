import os
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy.stats import pearsonr

def evaluation_score(file_path):
    df = pd.read_csv(file_path)
    ground_truth = df['value_ground_truth'].values
    predictions = df['value'].values
    
    # Calculate metrics
    r2 = r2_score(ground_truth, predictions)
    mae = mean_absolute_error(ground_truth, predictions)
    rmse = np.sqrt(mean_squared_error(ground_truth, predictions))
    
    # Calculate Pearson correlation coefficient
    pearson_corr, _ = pearsonr(ground_truth, predictions)
    
    return {'R2': r2, 'MAE': mae, 'RMSE': rmse, 'Pearson': pearson_corr}

# Replace 'your_directory_path' with the path to the directory containing the folders
adme_base_path = '/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/singletask/test/'
adme_list = ["clint","fe","fubrain","fup_human","fup_rat","ner_human","papp_caco2","papp_llc","rb_rat","sol"]
folders = ["itr1","itr2","itr3","itr4","itr5"]

results = []

# Iterate through each folder and process the evaluation file
for adme in adme_list:
    r2_values, mae_values, rmse_values, pearson_values = [], [], [], []
    for folder in folders:
        file_path = os.path.join(adme_base_path, adme, folder, 'predictions.csv')
        if os.path.exists(file_path):
            values = evaluation_score(file_path)
            r2_values.append(values['R2'])
            mae_values.append(values['MAE'])
            rmse_values.append(values['RMSE'])
            pearson_values.append(values['Pearson'])
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
            'std_pearson': std_pearson
        })

# Save results to a file
with open('/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/singletask/evaluation.txt', 'w') as file:
    for result in results:
        file.write(f"adme_parameter: {result['adme_parameter']}\n")
        file.write(f"R2: mean = {result['mean_r2']}, std = {result['std_r2']}\n")
        file.write(f"MAE: mean = {result['mean_mae']}, std = {result['std_mae']}\n")
        file.write(f"RMSE: mean = {result['mean_rmse']}, std = {result['std_rmse']}\n")
        file.write(f"Pearson: mean = {result['mean_pearson']}, std = {result['std_pearson']}\n\n")

# Save results to a csv file
df = pd.DataFrame(results)
df.to_csv('/data_st01/drug/itosho/ADMET/configs/accuracy_drug/adme/singletask/evaluation.csv', index=False)
