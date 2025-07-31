# ADME Log Data Description

This directory contains log-transformed ADME property data. The data processing removes duplicates by grouping SMILES and taking mean values, then applies logarithmic transformation to specific parameters.

## Data Processing Steps

1. **Duplicate Removal**: Group by SMILES and take mean values for duplicate entries
2. **Log Transformation**: Apply log10 transformation to specific ADME parameters (see list below)
3. **Epsilon Handling**: Replace zero values with small epsilon before log transformation
4. **Format Conversion**: Convert values to string format with brackets for kmol compatibility

## How to Generate Log Data

To create the log-transformed data from raw ADME files, run the following script:

```bash
# Navigate to the all_data directory
cd /path/to/ADME_MTFT/dataset/all_train_data_2022/standardize-drug_list/ADME/all_data

# Run the log data creation script
python create_log_data.py
```

The script will:
- Read all CSV files in the current directory
- Process each file according to the transformation rules
- Save the processed files to the `log_data/` subdirectory

## Number of Data Points
- **clint**: 5256  
- **fe**: 343  
- **fubrain**: 587  
- **fup_human**: 3472  
- **fup_rat**: 536  
- **ner_human**: 446  
- **papp_caco2**: 5581  
- **papp_llc**: 462  
- **rb_rat**: 163  
- **sol**: 14392  

## Parameters with Log Transformation

The following parameters undergo log10 transformation:

- **clint** (intrinsic clearance) - epsilon: 1e-4
- **ner_human** (net efflux ratio, human) - epsilon: 1e-4  
- **papp_caco2** (apparent permeability, Caco-2) - epsilon: 1e-4
- **papp_llc** (apparent permeability, LLC-PK1) - epsilon: 1e-4
- **rb_rat** (blood-brain barrier ratio, rat) - epsilon: 1e-4
- **sol** (solubility) - epsilon: 1e-8

## Parameters without Log Transformation

The following parameters use original values:

- **fe** (fraction excreted)
- **fubrain** (fraction unbound, brain)
- **fup_human** (fraction unbound, human plasma)
- **fup_rat** (fraction unbound, rat plasma)

## Output Format

Each processed CSV file contains:
- `smiles`: SMILES string representation of the molecule
- `value`: Transformed value in bracketed string format (e.g., "[1.234]")
- `target_id`: Target identifier for the ADME parameter