import argparse
import cmd
from bch_iblt_construction_1 import BchIbltConstruction1
from bch_iblt_construction_2 import BchIbltConstruction2
from bch_iblt_construction_3 import BchIbltConstruction3

def attempt_decode_data(encoded_data, bch):
    try:
        decoded_data_gf = bch.decode_data(encoded_data)
        return decoded_data_gf
    except Exception as e:  # Catch-all exception handling
        print(f"Decoding error: {e}")
        return ""

# Function to print table data with an attempt to decode each cell
def print_table_with_decoding(table, bch):
    for i, cell in enumerate(table):
        decoded_word = attempt_decode_data(cell, bch)
        print(f"Cell {i}: {cell} - Decoded Word: '{decoded_word}'")

class BCHIBLTShell(cmd.Cmd):
    intro = 'Welcome to the BCH IBLT shell. Type help or ? to list commands.\n'
    prompt = '(BCH IBLT) '

    def __init__(self, bch_iblt):
        super().__init__()
        self.bch_iblt = bch_iblt

    def do_insert(self, arg):
        'Insert data: INSERT data'
        data = arg.strip()
        if data:
            self.bch_iblt.insert(data)
            print(f"Inserted: {data}")
            print_table_with_decoding(self.bch_iblt.table, self.bch_iblt)
        else:
            print("No data provided for insertion.")

    def do_delete(self, arg):
        'Delete data: DELETE data'
        data = arg.strip()
        if data:
            self.bch_iblt.delete(data)
            print(f"Deleted: {data}")
            print_table_with_decoding(self.bch_iblt.table, self.bch_iblt)
        else:
            print("No data provided for deletion.")

    def do_list(self, arg):
        'List entries: LIST'
        entries = self.bch_iblt.list_entries()
        # print(f"Entries in the IBLT: {entries}")

    def do_exit(self, arg):
        'Exit the shell: EXIT'
        print("Exiting BCH IBLT shell.")
        return True

if __name__ == '__main__':
    # Initialize argument parser
    parser = argparse.ArgumentParser(description="Interactive BCH IBLT Shell")

    # Add arguments
    parser.add_argument("--type", type=int, choices=[1, 2, 3],
                        help="Type of BCH IBLT (1, 2, or 3).", required=True)
    parser.add_argument("--r", type=int, help="Parameter r for BCH", default=0)
    parser.add_argument("--d", type=int, help="Parameter d for BCH", default=0)

    # Parse arguments
    args = parser.parse_args()

    # Set default values for r and d based on type if not provided
    if args.r == 0 or args.d == 0:
        if args.type == 1:
            args.r, args.d = 12, 4
        elif args.type == 2:
            args.r, args.d = 12, 4
        elif args.type == 3:
            args.r, args.d = 12, 2

    # Create the appropriate BCH IBLT instance based on the type
    if args.type == 1:
        bch_iblt_instance = BchIbltConstruction1(args.r, args.d)
    elif args.type == 2:
        bch_iblt_instance = BchIbltConstruction2(args.r, args.d)
    elif args.type == 3:
        bch_iblt_instance = BchIbltConstruction3(args.r, args.d)
    else:
        print("Invalid type provided.")
        exit(1)

    # Start the interactive shell
    BCHIBLTShell(bch_iblt_instance).cmdloop()
