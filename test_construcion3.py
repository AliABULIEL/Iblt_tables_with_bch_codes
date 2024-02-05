from bch_iblt_construction_3 import BchIbltConstruction3


def print_table_with_decoding(construction3):
    for i, cell in enumerate(construction3.table):
        decoded_word = construction3.decode_data(cell)
        print(f"Cell {i}: {cell} - Decoded Word: '{decoded_word}'")


bch_iblt = BchIbltConstruction3(11, 4)

# List of test data strings
test_data_list = ["hello", "world", "test", "data", "iblt"]

for i in test_data_list:
    encoded_data = bch_iblt.encode_data(i)

    decoded_data = bch_iblt.decode_data(encoded_data)

    print(f"Original Data: {i}")
    print(f"Encoded Data: {encoded_data}")
    print(f"Decoded Data: {decoded_data}")

# Insert each string into the IBLT
for data in test_data_list:
    bch_iblt.insert(data)
    print_table_with_decoding(bch_iblt)

# Print the table after all insertions
print("\nTable after all insertions:")
print_table_with_decoding(bch_iblt)

# Attempt to list entries from the IBLT
print("\nAttempting to list entries from the IBLT:")
listed_entries = bch_iblt.list_entries()
print(f" list entries result {listed_entries}")


# Delete each string from the IBLT and print the table after each deletion
for data in test_data_list:
    bch_iblt.delete(data)
    print(f"\nTable after deleting '{data}':")
    print_table_with_decoding(bch_iblt)