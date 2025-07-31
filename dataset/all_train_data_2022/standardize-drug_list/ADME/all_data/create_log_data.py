#!/usr/bin/env python3
"""
ADME Log Data Processing Script

This script processes ADME property data by:
1. Reading individual ADME property CSV files
2. Applying log10 transformation to specified properties
3. Grouping by SMILES and taking mean values for duplicates
4. Saving processed data to log_data directory

Based on: adme_drug_log_duplicates.ipynb
"""

import pandas as pd
import numpy as np
import glob
import os
from pathlib import Path


def safe_log10(series, epsilon):
    """
    Apply log10 transformation with epsilon for zero values.
    
    Args:
        series: pandas Series to transform
        epsilon: small value to replace zeros
    
    Returns:
        log10 transformed series
    """
    # Replace 0 with small epsilon value
    series = series.replace(0, epsilon)
    return np.log10(series)


def process_adme_data(input_dir, output_dir):
    """
    Process ADME data files and create log-transformed versions.
    
    Args:
        input_dir: Directory containing input CSV files
        output_dir: Directory to save processed files
    """
    # Properties that need log10 transformation
    log_list = ["clint", "ner_human", "papp_caco2", "papp_llc", "rb_rat", "sol"]
    
    # Get all CSV files in input directory
    input_path = Path(input_dir)
    adme_paths = list(input_path.glob("*.csv"))
    adme_paths.sort()
    
    print(f"Found {len(adme_paths)} ADME property files:")
    for path in adme_paths:
        print(f"  - {path.name}")
    
    # Create output directory if it doesn't exist
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Process each file
    for path in adme_paths:
        property_name = path.stem  # filename without extension
        print(f"\nProcessing {property_name}...")
        
        # Read CSV file
        df = pd.read_csv(path)
        print(f"  Original data shape: {df.shape}")
        
        # Group by SMILES and take mean for duplicates
        df_grouped = df.groupby('smiles').agg({
            'value': 'mean',
            'target_id': 'first'
        }).reset_index()
        print(f"  After grouping: {df_grouped.shape}")
        
        # Apply log10 transformation if needed
        if property_name in log_list:
            print(f"  Applying log10 transformation...")
            if property_name == "sol":
                # Use smaller epsilon for solubility
                df_grouped["value"] = safe_log10(df_grouped["value"], 1e-8)
            else:
                # Use standard epsilon for other properties
                df_grouped["value"] = safe_log10(df_grouped["value"], 1e-4)
        
        # Format value column as string with brackets (for kmol compatibility)
        df_grouped["value"] = "[" + df_grouped["value"].astype(str) + "]"
        
        # Save processed file
        output_file = output_path / f"{property_name}.csv"
        df_grouped.to_csv(output_file, index=False)
        print(f"  Saved to: {output_file}")
    
    print(f"\nProcessing complete! All files saved to: {output_dir}")


def main():
    """Main function to process ADME data."""
    # Set up paths
    current_dir = Path(__file__).parent
    input_dir = current_dir
    output_dir = current_dir / "log_data"
    
    print("ADME Log Data Processing")
    print("=" * 40)
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Process the data
    process_adme_data(input_dir, output_dir)


if __name__ == "__main__":
    main()