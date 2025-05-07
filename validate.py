#!/usr/bin/env python
"""
Validation script for baseball statistics data.
Validates the generated CSV files against the source Excel files.
"""
import os
import glob
import pandas as pd
import re


def validate_latest_output():
    """Validate the most recently created output files."""
    # Find the most recent output directory
    output_dirs = sorted(glob.glob("output/*"))
    if not output_dirs:
        print("No output directories found.")
        return False
    
    latest_output = output_dirs[-1]
    print(f"Validating output in {latest_output}")
    
    # Check if the output CSV files exist
    csv_files = [
        os.path.join(latest_output, "Batting.csv"),
        os.path.join(latest_output, "Pitching.csv"),
        os.path.join(latest_output, "Fielding.csv")
    ]
    
    missing_files = [f for f in csv_files if not os.path.exists(f)]
    if missing_files:
        print(f"Missing output files: {', '.join(missing_files)}")
        return False
    
    # Count the number of Excel files as a basic validation
    excel_files = glob.glob("input/**/*.xlsx", recursive=True)
    num_excel_files = len(excel_files)
    
    # Load the CSV files
    batting_df = pd.read_csv(os.path.join(latest_output, "Batting.csv"))
    pitching_df = pd.read_csv(os.path.join(latest_output, "Pitching.csv"))
    fielding_df = pd.read_csv(os.path.join(latest_output, "Fielding.csv"))
    
    # Validate Team and Round columns exist
    required_columns = ['Team', 'Round']
    
    for df_name, df in [('Batting', batting_df), ('Pitching', pitching_df), ('Fielding', fielding_df)]:
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"{df_name} is missing required columns: {', '.join(missing_cols)}")
            return False
    
    # Check if all teams are represented in each file
    team_names = set()
    for file_path in excel_files:
        base_filename = os.path.basename(file_path)
        base_name_no_ext = os.path.splitext(base_filename)[0]
        team_name = re.sub(r'^\d+', '', base_name_no_ext)
        team_names.add(team_name)
    
    for df_name, df in [('Batting', batting_df), ('Pitching', pitching_df), ('Fielding', fielding_df)]:
        if set(df['Team'].unique()) != team_names:
            print(f"Warning: Not all teams are represented in {df_name}")
    
    # Check if all rounds are represented
    round_names = {os.path.basename(os.path.dirname(file_path)) for file_path in excel_files}
    
    for df_name, df in [('Batting', batting_df), ('Pitching', pitching_df), ('Fielding', fielding_df)]:
        if set(df['Round'].unique()) != round_names:
            print(f"Warning: Not all rounds are represented in {df_name}")
    
    print("Validation complete!")
    return True


if __name__ == "__main__":
    validate_latest_output()