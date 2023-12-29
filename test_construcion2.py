from bch_iblt_first_construction_2 import BchIbltConstruction2
r = 10  # Since 2^r - 1 = 1023, r should be 10
d = 5
bch_iblt = BchIbltConstruction2(r, d)

test_data = "h"
encoded_data = bch_iblt.encode_data(test_data)

decoded_data = bch_iblt.decode_data(encoded_data)

print(f"Original Data: {test_data}")
print(f"Encoded Data: {encoded_data}")
print(f"Decoded Data: {decoded_data}")


# bch_iblt.insert("hello")
# for i, cell in enumerate(bch_iblt.table):
#     print(f"Cell {i}: {cell}")
# bch_iblt.insert("world")
# for i, cell in enumerate(bch_iblt.table):
#     print(f"Cell {i}: {cell}")
# # bch_iblt.insert("love")
# # bch_iblt.insert("like")
#
# # Show the updated table
# print("Updated table:")
# for i, cell in enumerate(bch_iblt.table):
#     print(f"Cell {i}: {cell}")
# # bch_iblt.delete("love")
# # for i, cell in enumerate(bch_iblt.table):
# #     print(f"Cell {i}: {cell}")

def attempt_decode_data(encoded_data, bch_code):
    try:
        decoded_data_gf = bch_code.decode(encoded_data)
        decoded_data_binary = decoded_data_gf.tolist()
        decoded_data_bytes = bytes(int(''.join(map(str, decoded_data_binary[i:i+8])), 2) for i in range(0, len(decoded_data_binary), 8))
        decoded_data = decoded_data_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
        return decoded_data
    except galois.GaloisException:
        return "Undecodable or no data"

# Function to print table data with an attempt to decode each cell
def print_table_with_decoding(table, bch_code):
    for i, cell in enumerate(table):
        decoded_word = attempt_decode_data(cell, bch_code)
        print(f"Cell {i}: {cell} - Decoded Word: '{decoded_word}'")

# r = 10  # Since 2^r - 1 = 1023, r should be 10
# d = 5
# bch_iblt = BchIbltConstruction1(r, d)
#
# # List of test data strings
# test_data_list = ["hello", "world", "test", "data", "iblt"]
#
#
# # Insert each string into the IBLT
# for data in test_data_list:
#     bch_iblt.insert(data)
#     print(f"Inserted: {data}")
#
# # Print the table after all insertions
# print("\nTable after all insertions:")
# print_table_with_decoding(bch_iblt.table, bch_iblt.bch)
#
# # Attempt to list entries from the IBLT
# print("\nAttempting to list entries from the IBLT:")
# listed_entries = bch_iblt.list_entries()
#
#
# # Delete each string from the IBLT and print the table after each deletion
# for data in test_data_list[::-1]:
#     bch_iblt.delete(data)
#     print(f"\nTable after deleting '{data}':")
#     print_table_with_decoding(bch_iblt.table, bch_iblt.bch)