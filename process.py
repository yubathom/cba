#!/usr/bin/env python
"""
Excel to CSV data processor for baseball statistics.
Processes Excel files in input directory and outputs CSV files.
"""
import os
import glob
import pandas as pd
from datetime import datetime
import re
import numpy as np


def extract_team_name(filename):
    """Extract team name from filename by removing the number prefix."""
    # Extract just the filename without path
    base_filename = os.path.basename(filename)
    # Remove the file extension
    base_name_no_ext = os.path.splitext(base_filename)[0]
    # Remove any digits at the beginning
    team_name = re.sub(r'^\d+', '', base_name_no_ext)
    return team_name


def is_valid_player_row(row):
    """Check if row represents a valid player (not header, team stats, etc.)"""
    # Check if first column (player number) is a number or can be converted to one
    try:
        # Check if the value in the first column is a number or can be converted to one
        if pd.isna(row.iloc[0]) or row.iloc[0] == '' or str(row.iloc[0]).strip() == '':
            return False
            
        # Try to convert to float - valid player rows will have a number here
        float(str(row.iloc[0]).strip())
        
        # Additional check - if the name field (usually column 1) is empty, it's not a player
        if pd.isna(row.iloc[1]) or str(row.iloc[1]).strip() == '':
            return False
            
        # Check if this is a "Team Stats" row
        if isinstance(row.iloc[1], str) and "Team Stats" in row.iloc[1]:
            return False
            
        return True
    except (ValueError, TypeError):
        return False


def process_table(excel, sheet_name, team_name, round_name):
    """Process a specific sheet/table from an Excel file."""
    # First pass to identify the true header row (the one with "#" and "Name")
    header_row = None
    df_temp = pd.read_excel(excel, sheet_name, header=None)
    
    for idx, row in df_temp.iterrows():
        if row.iloc[0] == "#" and isinstance(row.iloc[1], str) and "Name" in row.iloc[1]:
            header_row = idx
            break
    
    if header_row is not None:
        # Read the Excel file using the identified header row
        df = pd.read_excel(excel, sheet_name, header=header_row)
        
        # Filter only valid player rows
        df = df[df.apply(is_valid_player_row, axis=1)]
        
        # Add Team and Round columns
        df['Team'] = team_name
        df['Round'] = round_name
        
        return df
    
    return pd.DataFrame()


def process_excel_files():
    """Process all Excel files in input directory and subdirectories."""
    # Create timestamp for output directory
    timestamp = datetime.now().strftime("%Y-%m-%d_%Hh%M")
    output_dir = os.path.join("output", timestamp)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Define expected column names for each table (excluding Team and Round which are added later)
    batting_columns = ["#", "Name", "G", "PA", "AB", "R", "H", "HR", "TB", "RBI", 
                       "AVG", "BB", "SO", "HBP", "SB", "CS", "SCB", "SF", "SLG", "BA/RSP"]
    
    pitching_columns = ["#", "Name", "G", "W", "L", "SV", "HLD", "IP", "BF", "Ball", 
                        "Str", "R", "ER", "ERA", "K", "H", "BB", "IBB", "BK", "WP", "HR"]
    
    fielding_columns = ["#", "Name", "G", "ERR", "PO", "A", "SBA", "CS", "DP", "TP", 
                        "PB", "FP", "FP1", "FP2", "FP3", "FP4", "FP5", "FP6", "FP7", "FP8", "FP9", 
                        "IP", "PO1", "A1", "Et1", "Ef1", "AP1", "PO2", "A2", "Et2", "Ef2", "AP2", 
                        "PO3", "A3", "Et3", "Ef3", "AP3", "PO4", "A4", "Et4", "Ef4", "AP4", 
                        "PO5", "A5", "Et5", "Ef5", "AP5", "PO6", "A6", "Et6", "Ef6", "AP6", 
                        "PO7", "A7", "Et7", "Ef7", "AP7", "PO8", "A8", "Et8", "Ef8", "AP8", 
                        "PO9", "A9", "Et9", "Ef9", "AP9"]
    
    # Add Team and Round to all column lists
    batting_columns.extend(["Team", "Round"])
    pitching_columns.extend(["Team", "Round"])
    fielding_columns.extend(["Team", "Round"])
    
    # Initialize DataFrames for each table
    batting_df = pd.DataFrame(columns=batting_columns)
    pitching_df = pd.DataFrame(columns=pitching_columns)
    fielding_df = pd.DataFrame(columns=fielding_columns)
    
    # Find all xlsx files in input directory and subdirectories
    excel_files = glob.glob("input/**/*.xlsx", recursive=True)
    
    # Process each file
    for file_path in excel_files:
        # Get the directory name (round)
        round_name = os.path.basename(os.path.dirname(file_path))
        
        # Get team name
        team_name = extract_team_name(file_path)
        
        # Load the Excel file
        try:
            # Try to read the Excel file with all sheets
            excel = pd.ExcelFile(file_path)
            
            # Process Batting sheet if it exists
            if 'Batting' in excel.sheet_names:
                df = process_table(excel, 'Batting', team_name, round_name)
                
                if not df.empty:
                    # Standardize column names - map the first few columns to our standard names
                    column_mapping = {}
                    for i, col in enumerate(df.columns):
                        if i < len(batting_columns) - 2:  # -2 for Team and Round
                            column_mapping[col] = batting_columns[i]
                    
                    # Rename columns
                    for old_col, new_col in column_mapping.items():
                        if old_col in df.columns:
                            df = df.rename(columns={old_col: new_col})
                    
                    # Ensure only expected columns are included
                    available_columns = [col for col in batting_columns if col in df.columns]
                    df = df[available_columns]
                    
                    # Concatenate to the main DataFrame
                    batting_df = pd.concat([batting_df, df], ignore_index=True)
            
            # Process Pitching sheet if it exists
            if 'Pitching' in excel.sheet_names:
                df = process_table(excel, 'Pitching', team_name, round_name)
                
                if not df.empty:
                    # Standardize column names
                    column_mapping = {}
                    for i, col in enumerate(df.columns):
                        if i < len(pitching_columns) - 2:
                            column_mapping[col] = pitching_columns[i]
                    
                    # Rename columns
                    for old_col, new_col in column_mapping.items():
                        if old_col in df.columns:
                            df = df.rename(columns={old_col: new_col})
                    
                    # Ensure only expected columns are included
                    available_columns = [col for col in pitching_columns if col in df.columns]
                    df = df[available_columns]
                    
                    # Concatenate to the main DataFrame
                    pitching_df = pd.concat([pitching_df, df], ignore_index=True)
            
            # Process Fielding sheet if it exists
            if 'Fielding' in excel.sheet_names:
                df = process_table(excel, 'Fielding', team_name, round_name)
                
                if not df.empty:
                    # Standardize column names
                    column_mapping = {}
                    for i, col in enumerate(df.columns):
                        if i < len(fielding_columns) - 2:
                            column_mapping[col] = fielding_columns[i]
                    
                    # Rename columns
                    for old_col, new_col in column_mapping.items():
                        if old_col in df.columns:
                            df = df.rename(columns={old_col: new_col})
                    
                    # Ensure only expected columns are included
                    available_columns = [col for col in fielding_columns if col in df.columns]
                    df = df[available_columns]
                    
                    # Concatenate to the main DataFrame
                    fielding_df = pd.concat([fielding_df, df], ignore_index=True)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # Save each table to a separate CSV file
    if not batting_df.empty:
        # Save the clean data
        batting_df.to_csv(os.path.join(output_dir, 'Batting.csv'), index=False)
        print(f"Saved Batting.csv with {len(batting_df)} records")
    
    if not pitching_df.empty:
        # Save the clean data
        pitching_df.to_csv(os.path.join(output_dir, 'Pitching.csv'), index=False)
        print(f"Saved Pitching.csv with {len(pitching_df)} records")
    
    if not fielding_df.empty:
        # Save the clean data
        fielding_df.to_csv(os.path.join(output_dir, 'Fielding.csv'), index=False)
        print(f"Saved Fielding.csv with {len(fielding_df)} records")
    
    print(f"Processing complete. Files saved to {output_dir}")


if __name__ == "__main__":
    process_excel_files()