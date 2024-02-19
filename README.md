IBLT with BCH Codes
===================
Article Summary 
-----------------
The article Lookup Tables (IBLTs) with BCH codes, which aim at improving memory efficiency and error correction. Here's a detailed explanation for each construction in simple English:

1.  **Construction 1**: This method uses a specific type of error-correcting code (BCH code) to create a more memory-efficient IBLT. It involves organizing data in such a way that errors can be corrected up to a certain limit, significantly reducing the amount of memory needed compared to traditional methods. This construction is particularly useful for applications where saving memory is crucial.
    
2.  **Construction 2**: Building on the first method, this construction splits the data into two parts (upper and lower halves) using the BCH parity-check matrix. This split is particularly effective when the number of errors to be corrected is an even number. It offers a more refined approach to organizing data, which can lead to further reductions in memory usage.
    
3.  **Construction 3**: Tailored specifically for situations where exactly four errors need to be corrected, this method modifies the approach of Construction 2 by removing the left-most column of the BCH parity-check matrix. This small adjustment leads to an even more compact representation of data, optimizing memory usage for this specific scenario.
    

Each of these constructions demonstrates innovative ways to leverage BCH codes within IBLTs, aiming at improving both the efficiency and effectiveness of data processing and error correction in computing applications
This Python script (`run.py`) implements three types of Invertible Bloom Lookup Tables (IBLTs) with BCH codes: `Construction1`, `Construction2`, and `Construction3`. These implementations are designed to demonstrate the integration of BCH error-correction codes with IBLTs.

Implmentation
-----------

The script supports the following types of IBLTs:

*   **bch_iblt_construction_1**: construction_1 implementation of IBLT with BCH coding.
*   **bch_iblt_construction_2**: construction_2 implementation of IBLT with BCH coding.
*   **bch_iblt_construction_3**: construction_13implementation of IBLT with BCH coding.

Each type can be selected via command-line arguments. The script allows for the insertion and deletion of data into the IBLT and supports a peeling process for data recovery.

Requirements
------------

*   Python 3.6 or higher
*   `numpy`, `argparse`, `hashlib` Python packages

To install the requirements:

shCopy code

`sh install_requirements.sh`

Usage
-----

Run the script from the command line by specifying the type of IBLT, the parameters `r` and `d` for BCH, and optionally, which function(s) to execute.

### Basic Usage

To specify the operation, type of BCH (1, 2, or 3), and the parameters `r` and `d`:

bashCopy code

`python run.py --function [FUNCTION] --type [TYPE] --r [R] --d [D]`

Where `[FUNCTION]` can be `encode_decode`, `insert`, `iblt`, or omitted to run all functions if `--all` is used.

### Running All Functions

To run all functions:

bashCopy code

`python run.py --all --type [TYPE]`

The script automatically uses recommended `r` and `d` values based on the type of BCH selected, but these can be overridden.

### Examples Commands

1.  Run the encode and decode test with BCH type 1:

bashCopy code

`python run.py --function encode_decode --type 1`

2.  Insert data using BCH type 2 and custom `r` and `d`:

bashCopy code

`python run.py --function insert --type 2 --r 12 --d 4`

3.  Run all tests for BCH type 3 with default parameters:

bashCopy code

`python run.py --all --type 3`

4.  Test the IBLT functionality with BCH type 1:

bashCopy code

`python run.py --function iblt --type 1`

5.  Run encode\_decode function with custom parameters for type 2:

bashCopy code

`python run.py --function encode_decode --type 2 --r 12 --d 4`

These example commands demonstrate how to run the script with different configurations, showcasing the flexibility of the testing framework for IBLTs with BCH codes.