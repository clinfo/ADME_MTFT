# ADME Multitask Training and Fine-Tuning

This README provides an overview of the environment setup and directory/configuration file organization required for multitask Graph Neural Network (GNN) training on ADME property prediction and subsequent fine-tuning, as employed in the paper **“Improving ADME Prediction with Multitask Graph Neural Networks and Assessing Explainability in Lead Optimization”** by Ito S. et al.  
By following this document, you will understand the essential requirements for data preparation and configuration placement. Detailed training and fine-tuning procedures are not covered here.

![ADME-MTFT: Fig1](./images/workflow_detail.png)

## Contact
- **Data Curator:** Shoma Ito  
- **Repository Manager:** Takuto Koyama (koyama.takuto.82j[at]st.kyoto-u.ac.jp)


## Table of Contents

- [ADME Multitask Training and Fine-Tuning](#adme-multitask-training-and-fine-tuning)
  - [Contact](#contact)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Directory Structure](#directory-structure)
    - [Key subdirectories](#key-subdirectories)
  - [Data Preparation](#data-preparation)
  - [Training and Prediction Procedures](#training-and-prediction-procedures)
    - [1. Multitask Training](#1-multitask-training)
    - [2. Fine-tuning](#2-fine-tuning)
    - [3. Prediction](#3-prediction)
    - [Notes](#notes)


## Prerequisites

- **kmol v1.1.7** ([GitHub](https://github.com/elix-tech/kmol.git)): the command-line tool for model training and evaluation

  Install required packages in a dedicated environment:

```bash
  git clone https://github.com/elix-tech/kmol.git
  cd kmol
  git checkout v1.1.7
  make create-env
  conda activate kmol
```

## Directory Structure

```
ADMET_MTFT/
├── dataset/
│   └── all_train_data_2022/
│       ├── standardize-drug_list/
│       │   └── ADME/
│       │       └── all_data/
│       │           └── log_data/           # per-target log-transformed values
│       └── multitask.csv                   # combined multitask labels and values
└── configs/
    └── accuracy_drug/
        └── adme/
            ├── multitask/                  # config files for GNN multitask training
            └── finetuning_learning_rate/  # config files for GNN fine-tuning

```

### Key subdirectories

- `dataset/all_train_data_2022`:
  - `standardize-drug_list/ADME/all_data/log_data`: per‑target log‑transformed values
  - `.../multitask.csv`: combined multitask labels and values

- `configs/accuracy_drug/adme`:
  - `multitask/`: config files for GNN multitask training
  - `finetunig_learning_rate/`: config files for GNN fine‑tuning


## Data Preparation

Before training, ensure your data is properly formatted:

1. **Individual target data**: Place log-transformed values in `dataset/all_train_data_2022/standardize-drug_list/ADME/all_data/log_data/`
2. **Multitask data**: Combine all targets into `dataset/all_train_data_2022/multitask.csv`
3. **Configuration**: Adjust paths in config files to match your directory structure

**For detailed data preprocessing steps** (including log transformation, duplicate removal, and epsilon handling), please refer to:
[`dataset/all_train_data_2022/standardize-drug_list/ADME/all_data/README.md`](dataset/all_train_data_2022/standardize-drug_list/ADME/all_data/README.md)

## Training and Prediction Procedures

### 1. Multitask Training

To perform multitask GNN training on ADME properties:

```bash
# Activate the kmol environment
conda activate kmol

# Run multitask training using the configuration files
kmol train /path/to/ADME_MTFT/configs/accuracy_drug/adme/multitask/train/itr1/config.json
```

The multitask training will use the combined dataset (`dataset/all_train_data_2022/standardize-drug_list/ADME/all_data/log_data/multitask.csv`) to train a single GNN model on multiple ADME properties simultaneously.

**Key configuration features for multitask training:**

- **Multitask loader configuration:**
```json
"loader": {
  "type": "multitask",
  "input_path": "multitask.csv",
  "task_column_name": "target_id",
  "max_num_tasks": 10
}
```

- **Target-specific standardization:** Each ADME property (target 0-9) has individual mean and standard deviation values for proper normalization:
```json
"transformers": [
  {
    "type": "standardize",
    "target": 0,
    "mean": 1.5067472653927056,
    "std": 0.6985528512457979
  },
  // ... for targets 1-9
]
```

- **Training parameters:**
  - `"is_finetuning": false` - Initial training from scratch
  - `"checkpoint_path": null` - No pre-trained model

### 2. Fine-tuning

After multitask training, fine-tune the model for specific ADME parameters:

```bash
# Run fine-tuning with the same command
kmol train /path/to/ADME_MTFT/configs/accuracy_drug/adme/finetuning_learning_rate/train/clint/itr1/config.json
```

**Key configuration features for fine-tuning:**

- **Single-target data:** Uses target-specific CSV files (e.g., `clint.csv` for intrinsic clearance)
```json
"loader": {
  "type": "multitask",
  "input_path": "clint.csv",
  "task_column_name": "target_id",
  "max_num_tasks": 10
}
```

- **Pre-trained model loading:**
```json
"is_finetuning": true,
"checkpoint_path": "../ADMET/configs/accuracy_drug/adme/multitask/train/itr1/checkpoint.best.pt"
```

### 3. Prediction

To make predictions on new compounds:

```bash
# Run prediction using the fine-tuned model
kmol predict /path/to/ADME_MTFT/configs/accuracy_drug/adme/finetuning_learning_rate/test/clint/itr1/config.json
```

**Key configuration features for prediction:**

- **Test data configuration:**
```json
"loader": {
  "input_path": "test/clint.csv"
},
"splitter": {
  "type": "index",
  "splits": {
    "test": 1.0
  }
}
```

- **Fine-tuned model loading:**
```json
"is_finetuning": true,
"checkpoint_path": "../ADMET/configs/accuracy_drug/adme/finetuning_learning_rate/train/clint/itr1/checkpoint.best.pt"
```

- **Same standardization parameters:** Uses identical transformers as training to ensure consistent data preprocessing

- **Evaluation metrics:** Configured to compute R², MAE, and RMSE on test split

### Notes

- Update the paths in the commands above to match your actual directory structure
- Ensure the kmol environment is activated before running any commands
- For detailed configuration options, refer to the [kmol documentation](https://github.com/elix-tech/kmol)
