#!/usr/bin/env python
"""
Validation script for baseball statistics data.
Validates the generated CSV files in the output directory.
"""
import os
import pandas as pd

def validate_output():
    """Validate the output CSV files in the output/ directory."""
    output_dir = "output"
    csv_files = [
        os.path.join(output_dir, "Batting.csv"),
        os.path.join(output_dir, "Pitching.csv"),
        os.path.join(output_dir, "Fielding.csv")
    ]
    required_columns = ['Team', 'Round', "Name"]
    all_passed = True

    for csv_file in csv_files:
        print(f"\nChecking {csv_file}...")
        if not os.path.exists(csv_file):
            print(f"  ❌ File not found!")
            all_passed = False
            continue
        try:
            df = pd.read_csv(csv_file)
        except Exception as e:
            print(f"  ❌ Error reading file: {e}")
            all_passed = False
            continue
        # Check for required columns
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            print(f"  ❌ Missing required columns: {', '.join(missing_cols)}")
            all_passed = False
        else:
            print(f"  ✅ Required columns present.")
        # Check for non-empty file
        if df.empty:
            print(f"  ❌ File is empty!")
            all_passed = False
        else:
            print(f"  ✅ File is not empty.")
    if all_passed:
        print("\nAll validations passed!")
    else:
        print("\nSome validations failed. See above for details.")
    return all_passed

if __name__ == "__main__":
    validate_output()