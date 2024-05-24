import argparse
import galois
from bch_iblt_construction_1 import BchIbltConstruction1
from bch_iblt_construction_2 import BchIbltConstruction2
from bch_iblt_construction_3 import BchIbltConstruction3

def test_encode_decode(bch_iblt, data_to_insert):
# Test data to encode and decode
    for test_data in data_to_insert:
        encoded_data = bch_iblt.encode_data(test_data)

        decoded_data = bch_iblt.decode_data(encoded_data)

        # Output original, encoded, and decoded data
        print(f"Original Data: {test_data}")
        print(f"Encoded Data: {encoded_data}")
        print(f"Decoded Data: {decoded_data}")


def test_insert(bch_iblt, data_to_insert):
    for data in data_to_insert:
        print(f"inserting {data}")
        bch_iblt.insert(data)
        for i, cell in enumerate(bch_iblt.table):
            print(f"Cell {i}: {cell}")
        # bch_iblt.insert("world")
        # for i, cell in enumerate(bch_iblt.table):
            # print(f"Cell {i}: {cell}")
        # bch_iblt.insert("love")
        # bch_iblt.insert("like")

    # Show the updated table
    #     print("Updated table:")
    #     for i, cell in enumerate(bch_iblt.table):
    #         print(f"Cell {i}: {cell}")
    # bch_iblt.delete("love")
    # for i, cell in enumerate(bch_iblt.table):
    #     print(f"Cell {i}: {cell}")

def attempt_decode_data(encoded_data, bch_code):
    try:
        # Ensure encoded_data is 1-D and the correct size
        if len(encoded_data) > bch_code.n:
            encoded_data = encoded_data[:bch_code.n]

        decoded_data_gf = bch_code.decode(encoded_data)
        decoded_data_binary = decoded_data_gf.tolist()
        decoded_data_bytes = bytes(
            int(''.join(map(str, decoded_data_binary[i:i+8])), 2)
            for i in range(0, len(decoded_data_binary), 8)
        )
        return decoded_data_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
    except Exception as e:  # Catch-all exception handling
        print(f"Decoding error: {e}")
        return "Undecodable or no data"

# Function to print table data with an attempt to decode each cell
def print_table_with_decoding(table, bch_code):
    for i, cell in enumerate(table):
        decoded_word = attempt_decode_data(cell, bch_code)
        print(f"Cell {i}: {cell} - Decoded Word: '{decoded_word}'")
def test_iblt(bch, data_to_insert):
    # Insert each string into the IBLT
    for data in data_to_insert:
        bch.insert(data)
        print(f"Inserted: {data}")

    # Print the table after all insertions
    print("\nTable after all insertions:")
    print_table_with_decoding(bch.table, bch.bch)

    # Attempt to list entries from the IBLT
    print("\nAttempting to list entries from the IBLT:")
    listed_entries = bch.list_entries()
    print(f"List entries result is  {listed_entries}")

    # Delete each string from the IBLT and print the table after each deletion
    for data in test_data_list[::-1]:
        bch.delete(data)
        print(f"\nTable after deleting '{data}':")
        print_table_with_decoding(bch.table, bch.bch)


if __name__ == '__main__':
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Test BCH IBLT Constructions")

    # Add arguments
    parser.add_argument("--function", type=str,
                        help="Function to run: encode_decode, insert, iblt. Ignored if --all is set.", default="all")
    parser.add_argument("--type", type=int, choices=[1, 2, 3],
                        help="Type of BCH (1, 2, or 3). Hint: For type 1 use r=5, d=2; for type 2 use r=12, d=4; for type 3 use r=11, d=4",
                        required=True)
    parser.add_argument("--r", type=int, help="Parameter r for BCH", default=0)
    parser.add_argument("--d", type=int, help="Parameter d for BCH", default=0)
    parser.add_argument("--all", action="store_true", help="Run all functions")

    # Parse arguments
    args = parser.parse_args()

    # List of test data strings
    test_data_list = ["hello", "world", "test", "data", "iblt"]

    if args.all:
        # For each test function, create a new instance of the BCH IBLT
        for test_function in [test_encode_decode, test_insert, test_iblt]:
            print(f"Running {test_function}")

            # Adjust r and d based on type if not explicitly set
            if args.r == 0 or args.d == 0:
                if args.type == 1:
                    args.r, args.d = 12, 4
                elif args.type == 2:
                    args.r, args.d = 12, 4
                elif args.type == 3:
                    args.r, args.d = 11, 4

            # Reinitialize the appropriate BCH IBLT based on the argument for each test
            if args.type == 1:
                bch_iblt_instance = BchIbltConstruction1(args.r, args.d)
            elif args.type == 2:
                bch_iblt_instance = BchIbltConstruction2(args.r, args.d)
            else:  # args.type == 3
                bch_iblt_instance = BchIbltConstruction3(args.r, args.d)

            # Run the test function with a fresh instance
            test_function(bch_iblt_instance, test_data_list)
            print("\n")
    else:
        if args.r == 0 or args.d == 0:
            if args.type == 1:
                args.r, args.d = 10, 5
            elif args.type == 2:
                args.r, args.d = 12, 4
            elif args.type == 3:
                args.r, args.d = 11, 4
        # Initialize once if not running all tests
        if args.type == 1:
            bch_iblt = BchIbltConstruction1(args.r, args.d)
        elif args.type == 2:
            bch_iblt = BchIbltConstruction2(args.r, args.d)
        else:  # args.type == 3
            bch_iblt = BchIbltConstruction3(args.r, args.d)

        # Decide on which function to run
        if args.function == "encode_decode":
            test_encode_decode(bch_iblt, test_data_list)
        elif args.function == "insert":
            test_insert(bch_iblt, test_data_list)
        elif args.function == "iblt":
            test_iblt(bch_iblt)


