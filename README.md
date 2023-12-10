# IBLT with BCH Codes

This Python script (run.py) implements three types of Invertible Bloom Lookup Tables (IBLTs) with BCH codes: GeneralBCHIBLT, BCHIBLT, and IBLTIndel. These implementations are designed to demonstrate the integration of BCH error-correction codes with IBLTs.

## Description

The script supports the following types of IBLTs:
- GeneralBCHIBLT: A general implementation of IBLT with BCH coding.
- IBLT: An IBLT variant withoit BCH codes for error correction.
- IBLTIndel: An optimized IBLT that handles insertions and deletions efficiently.

Each type can be selected via command-line arguments. The script allows insertion and deletion of data into the IBLT and supports a peeling process for data recovery.

## Requirements

- Python 3.6 or higher
- bchlib, math, numpy, argparse, hashlib Python packages

## Usage

Run the script from the command line by specifying the type of IBLT, its size, BCH polynomial, BCH bits, and the data to insert or delete.

### Basic Usage
python run.py --type [TYPE] --size [SIZE] --bch_poly [POLY] --bch_bits [BITS] --data [DATA...]


### Additional Operations

- To insert additional data:

  python run.py  --insert [DATA...]

- To delete data:
  python run.py  --delete [DATA...]

- To query item:
    python run.py --query [DTA ..]
  
- To list entires:
  python run.py --list_entries

