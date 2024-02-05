from bch_iblt_construction_3 import BchIbltConstruction3
import galois
r = 10  # Since 2^r - 1 = 1023, r should be 10
d = 2
bch_iblt = BchIbltConstruction3(r, d)
#
# test_data =  ["hello world", "world",  "hello", "tests"]
# for i in test_data:
#     encoded_data = bch_iblt.encode_data(i)
#
#     decoded_data = bch_iblt.decode_data(encoded_data)
#
#     print(f"Original Data: {i}")
#     print(f"Encoded Data: {encoded_data}")
#     print(f"Decoded Data: {decoded_data}")


# bch_iblt.insert("exam")
# print("Updated table after insertion :")
# for i, cell in enumerate(bch_iblt.table):
#     print(f"Cell {i}: {cell} decoded data: {bch_iblt.decode_data(cell)}")
# bch_iblt.insert("test")
# # bch_iblt.insert("love")
# # bch_iblt.insert("like")
#
# # Show the updated table
# print("Updated table after insertion :")
# for i, cell in enumerate(bch_iblt.table):
#     print(f"Cell {i}: {cell} decoded data: {bch_iblt.decode_data(cell)}")
# bch_iblt.delete("test")
# print("Updated table after deletion :")
# for i, cell in enumerate(bch_iblt.table):
#     print(f"Cell {i}: {cell} decoded data: {bch_iblt.decode_data(cell)}")
#
# bch_iblt.delete("exam")
# print("Updated table after deletion :")
# for i, cell in enumerate(bch_iblt.table):
#     print(f"Cell {i}: {cell} decoded data: {bch_iblt.decode_data(cell)}")

# def attempt_decode_data(construction3, encoded_data):
#     try:
#         # Ensure encoded_data is 1-D and the correct size
#
#
#         decoded_data_gf = construction3.decode_data(encoded_data)
#         decoded_data_binary = decoded_data_gf.tolist()
#         decoded_data_bytes = bytes(
#             int(''.join(map(str, decoded_data_binary[i:i+8])), 2)
#             for i in range(0, len(decoded_data_binary), 8)
#         )
#         return decoded_data_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
#     except Exception as e:  # Catch-all exception handling
#         print(f"Decoding error: {e}")
#         return "Undecodable or no data"


# Function to print table data with an attempt to decode each cell
def print_table_with_decoding(construction3):
    for i, cell in enumerate(construction3.table):
        decoded_word = construction3.decode_data(cell)
        print(f"Cell {i}: {cell} - Decoded Word: '{decoded_word}'")


bch_iblt = BchIbltConstruction3(r, d)

# List of test data strings
test_data_list = ["hello", "world", "test", "data", "iblt"]


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