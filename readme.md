# BAM File Pooling Script

## Overview
This script processes BAM files by mapping filenames to a standardized format and distributing reads into pools based on a matrix indexing system. The script ensures that the number of BAM samples provided is a perfect square and organizes the reads into pools.

## Features
- Ensures that the number of samples is a perfect square.
- Distributes reads into pools.
- Saves the processed BAM files into an output directory.

## Requirements
- Python 3
- `pysam` library
- `os`, `random`, `csv`, and `argparse` modules (included in standard Python library)

## Installation
Ensure `pysam` is installed using the following command:
```bash
pip install pysam
```

## Usage
Run the script using the command:
```bash
python main.py <input_bam_path> <output_bam_path> <number_of_samples>
```

### Parameters
- `<input_bam_path>`: Path to the directory containing input BAM files.
- `<output_bam_path>`: Path to the directory where output BAM files will be stored.
- `<number_of_samples>`: The total number of BAM files (must be a perfect square).

### Example
```bash
python main.py /path/to/input_bam /path/to/output_bam 64
```

## How It Works
1. The script first verifies that the number of samples is a perfect square.
2. It maps BAM filenames to a standard format and stores this mapping in `sample_name_mapping.csv`.
3. It creates pools based on pooling scheme.
4. Reads from each BAM file are randomly assigned to one of the pools.
5. The processed BAM files are saved in the specified output directory.

## Output
- A directory containing pooled BAM files.
- A `sample_name_mapping.csv` file containing the original-to-standardized filename mapping.

## Error Handling
- If the number of samples is not a perfect square, the script prints an error and exits.
- If input bam number(inside the input folder) doesn't match the number of files in input folder
- If the input directory does not exist or does not contain the expected number of BAM files, the script prints an error and exits.
- If the output directory already exists, the script prompts the user to delete it before running again.

