# Baseball Statistics Processor

A Python-based tool for processing baseball team statistics from Excel files to consolidated CSV output.

## GitHub Pages Deployment

This project uses GitHub Actions to process the latest Excel files and publish the resulting CSVs and web app to GitHub Pages. The output CSV files (`Batting.csv`, `Pitching.csv`, `Fielding.csv`) are **not committed to the repository**; they are generated during the GitHub Actions workflow and published directly to GitHub Pages.

To deploy:

1. Push your changes to the repository.
2. Go to the Actions tab on GitHub and manually trigger the `pages-deploy` workflow ("Run workflow").
3. The workflow will:
   - Run the Python processing script to generate the latest CSVs in `output/`.
   - Publish `index.html`, `main.js`, and the three main CSVs (`Batting.csv`, `Pitching.csv`, `Fielding.csv`) to GitHub Pages.

The site will be available at the repository's GitHub Pages URL after the workflow completes.

## Overview

This project takes baseball statistics stored in Excel files (organized by team and round) and processes them into consolidated CSV files for batting, pitching, and fielding statistics.

## Features

- Processes Excel files containing baseball statistics
- Handles multiple teams and tournament rounds
- Extracts data from Batting, Pitching, and Fielding sheets
- Validates processed data against source files
- Generates timestamped output directories

## Requirements

- Python 3.8+
- pandas
- numpy
- openpyxl

## Installation

1. Clone this repository
2. Create a virtual environment (optional but recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required packages:
   ```
   pip install pandas numpy openpyxl
   ```

## Usage

### Input Data Structure

Place your Excel files in the `input` directory, organized by round:

```
input/
  ROUND-1/
    1TEAMNAME.xlsx
    2TEAMNAME.xlsx
    ...
  ROUND-2/
    ...
```

Each Excel file should contain sheets named "Batting", "Pitching", and "Fielding" with team statistics.

### Processing Data

Run the processing script:

```
python3 process.py
```

This will:

1. Process all Excel files in the input directory
2. Create a timestamped output directory
3. Generate three CSV files (Batting.csv, Pitching.csv, Fielding.csv)

### Validating Results

Validate the processed data:

```
python3 validate.py
```

This will:

1. Locate the most recent output directory
2. Validate the data against the source files
3. Report any inconsistencies or missing data

## Code Formatting and Linting

Format code:

```
black .
```

Lint code:

```
flake8
```

## License

[Your license information here]
