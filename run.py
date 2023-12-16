import argparse
from bch_iblt_first_construction_1 import BchIbltConstruction1

def main():
    parser = argparse.ArgumentParser(description='IBLT Implementation with BCH Codes')
    parser.add_argument('--r', type=int, required=True, help='r value for GF(2^r)')
    parser.add_argument('--d', type=int, required=True, help='Error-correcting capability d')
    parser.add_argument('--data', nargs='+', help='Data to insert into the IBLT')
    parser.add_argument('--insert', nargs='+', help='Additional data to insert')
    parser.add_argument('--delete', nargs='+', help='Data to delete from the IBLT')
    parser.add_argument('--list_entries', action='store_true', help='List all entries in the IBLT')
    args = parser.parse_args()

    # Initialize the IBLT
    iblt = BchIbltConstruction1( args.r, args.d)

    # Insert initial data into the IBLT
    if args.data:
        for data in args.data:
            iblt.insert(data)

    # Insert additional data if specified
    if args.insert:
        for data in args.insert:
            iblt.insert(data)

    # Delete data if specified
    if args.delete:
        for data in args.delete:
            iblt.delete(data)

    # List entries if specified
    if args.list_entries:
        entries = iblt.list_entries()
        print("Listed Entries:", entries)

if __name__ == '__main__':
    main()
