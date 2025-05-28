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
    output_dir = os.path.join("output")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Define expected column names for each table (excluding Team and Round which are added later)
    batting_columns = ["#", "Name", "G", "PA", "AB", "R", "H", "HR", "TB", "RBI", 
                       "AVG", "BB", "SO", "HBP", "SB", "CS", "SCB", "SF", "SLG"]
    # Add OBP and OPS after SLG
    batting_columns.insert(batting_columns.index("SLG") + 1, "OBP")
    batting_columns.insert(batting_columns.index("OBP") + 1, "OPS")
    
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
                    # Add Team and Round columns before any reordering
                    df['Team'] = team_name
                    df['Round'] = round_name
                    # Calculate OBP and OPS before reordering
                    h = pd.to_numeric(df.get("H", 0), errors='coerce').fillna(0)
                    bb = pd.to_numeric(df.get("BB", 0), errors='coerce').fillna(0)
                    hbp = pd.to_numeric(df.get("HBP", 0), errors='coerce').fillna(0)
                    ab = pd.to_numeric(df.get("AB", 0), errors='coerce').fillna(0)
                    sf = pd.to_numeric(df.get("SF", 0), errors='coerce').fillna(0)
                    slg = pd.to_numeric(df.get("SLG", 0), errors='coerce').fillna(0)
                    obp_denom = ab + bb + hbp + sf
                    obp = (h + bb + hbp) / obp_denom.replace(0, np.nan)
                    df["OBP"] = obp.round(3)
                    df["OPS"] = (df["OBP"] + slg).round(3)
                    # Now, only select columns that are actually present
                    final_columns = [col for col in batting_columns if col in df.columns]
                    df = df[final_columns]
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
                    # Add Team and Round columns before any reordering
                    df['Team'] = team_name
                    df['Round'] = round_name
                    # Now, only select columns that are actually present
                    final_columns = [col for col in pitching_columns if col in df.columns]
                    df = df[final_columns]
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
                    # Add Team and Round columns before any reordering
                    df['Team'] = team_name
                    df['Round'] = round_name
                    # Now, only select columns that are actually present
                    final_columns = [col for col in fielding_columns if col in df.columns]
                    df = df[final_columns]
                    # Concatenate to the main DataFrame
                    fielding_df = pd.concat([fielding_df, df], ignore_index=True)
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    # --- NEW LOGIC: Convert cumulative to per-round and add TOTAL row ---
    def per_round_and_total(df, id_cols, stat_cols, derived_funcs, round_order=None):
        if df.empty:
            return df
        # Sort rounds if order is provided
        if round_order is not None:
            df['__round_order'] = df['Round'].map(lambda r: round_order.index(r) if r in round_order else 999)
            df = df.sort_values(['Team', 'Name', '__round_order'])
        else:
            df = df.sort_values(['Team', 'Name', 'Round'])
        result_rows = []
        for (team, name), group in df.groupby(['Team', 'Name'], sort=False):
            group = group.copy()
            group = group.sort_values('Round', key=lambda x: x.map(lambda r: round_order.index(r) if round_order and r in round_order else 999) if round_order else x)
            prev = None
            per_round_rows = []
            for idx, row in group.iterrows():
                base = row.copy()
                if prev is not None:
                    for col in stat_cols:
                        if pd.api.types.is_numeric_dtype(df[col]):
                            base[col] = row[col] - prev[col]
                        else:
                            try:
                                base[col] = pd.to_numeric(row[col], errors='coerce') - pd.to_numeric(prev[col], errors='coerce')
                            except Exception:
                                pass
                # Recalculate derived columns
                for col, func in derived_funcs.items():
                    base[col] = func(base)
                per_round_rows.append(base)
                prev = row
            # Add TOTAL row
            total = per_round_rows[0].copy()
            total['Round'] = 'TOTAL'
            for col in stat_cols:
                total[col] = sum([r[col] for r in per_round_rows])
            for col, func in derived_funcs.items():
                total[col] = func(total)
            result_rows.extend(per_round_rows)
            result_rows.append(total)
        result_df = pd.DataFrame(result_rows)
        # Remove helper column if present
        if '__round_order' in result_df.columns:
            result_df = result_df.drop(columns=['__round_order'])
        return result_df

    # Get round order from input directory structure
    def extract_round_number(r):
        if r is None:
            return float('inf')
        if r.upper() == 'TOTAL':
            return float('inf')
        match = re.search(r'(\d+)', r)
        return int(match.group(1)) if match else float('inf')

    round_dirs = sorted(
        {os.path.basename(os.path.dirname(f)) for f in excel_files},
        key=lambda r: (extract_round_number(r), r.upper() != 'TOTAL')
    )

    # Batting
    if not batting_df.empty:
        # Columns to diff (all except id columns and derived columns)
        id_cols = ['#', 'Name', 'Team', 'Round']
        derived_cols = ['AVG', 'OBP', 'OPS', 'SLG']
        stat_cols = [c for c in batting_columns if c not in id_cols + derived_cols]
        # Derived column functions
        def batting_avg(row):
            ab = pd.to_numeric(row.get('AB', 0), errors='coerce')
            h = pd.to_numeric(row.get('H', 0), errors='coerce')
            return round(h / ab, 3) if ab else 0.0
        def obp(row):
            h = pd.to_numeric(row.get('H', 0), errors='coerce')
            bb = pd.to_numeric(row.get('BB', 0), errors='coerce')
            hbp = pd.to_numeric(row.get('HBP', 0), errors='coerce')
            ab = pd.to_numeric(row.get('AB', 0), errors='coerce')
            sf = pd.to_numeric(row.get('SF', 0), errors='coerce')
            denom = ab + bb + hbp + sf
            return round((h + bb + hbp) / denom, 3) if denom else 0.0
        def ops(row):
            return round(row.get('OBP', 0) + row.get('SLG', 0), 3)
        derived_funcs = {'AVG': batting_avg, 'OBP': obp, 'OPS': ops}
        batting_df = per_round_and_total(batting_df, id_cols, stat_cols, derived_funcs, round_dirs)
        # Ensure columns are in the correct order
        batting_df = batting_df[[c for c in batting_columns if c in batting_df.columns]]
        batting_df.to_csv(os.path.join(output_dir, 'Batting.csv'), index=False)
        print(f"Saved Batting.csv with {len(batting_df)} records")

    # Pitching
    if not pitching_df.empty:
        id_cols = ['#', 'Name', 'Team', 'Round']
        derived_cols = ['ERA']
        stat_cols = [c for c in pitching_columns if c not in id_cols + derived_cols]
        def era(row):
            er = pd.to_numeric(row.get('ER', 0), errors='coerce')
            ip = pd.to_numeric(row.get('IP', 0), errors='coerce')
            return round((er * 9) / ip, 2) if ip else 0.0
        derived_funcs = {'ERA': era}
        pitching_df = per_round_and_total(pitching_df, id_cols, stat_cols, derived_funcs, round_dirs)
        pitching_df = pitching_df[[c for c in pitching_columns if c in pitching_df.columns]]
        pitching_df.to_csv(os.path.join(output_dir, 'Pitching.csv'), index=False)
        print(f"Saved Pitching.csv with {len(pitching_df)} records")

    # Fielding
    if not fielding_df.empty:
        id_cols = ['#', 'Name', 'Team', 'Round']
        derived_cols = ['FP', 'FP1', 'FP2', 'FP3', 'FP4', 'FP5', 'FP6', 'FP7', 'FP8', 'FP9']
        stat_cols = [c for c in fielding_columns if c not in id_cols + derived_cols]
        def fp(row):
            po = pd.to_numeric(row.get('PO', 0), errors='coerce')
            a = pd.to_numeric(row.get('A', 0), errors='coerce')
            err = pd.to_numeric(row.get('ERR', 0), errors='coerce')
            denom = po + a + err
            return round((po + a) / denom, 3) if denom else 0.0
        derived_funcs = {'FP': fp}
        # Add FP1-FP9 as passthrough (or recalc if needed)
        for i in range(1, 10):
            def make_fp_i(i):
                return lambda row: fp(row)  # Placeholder, can be improved
            derived_funcs[f'FP{i}'] = make_fp_i(i)
        fielding_df = per_round_and_total(fielding_df, id_cols, stat_cols, derived_funcs, round_dirs)
        fielding_df = fielding_df[[c for c in fielding_columns if c in fielding_df.columns]]
        fielding_df.to_csv(os.path.join(output_dir, 'Fielding.csv'), index=False)
        print(f"Saved Fielding.csv with {len(fielding_df)} records")
    print(f"Processing complete. Files saved to {output_dir}")


if __name__ == "__main__":
    process_excel_files()