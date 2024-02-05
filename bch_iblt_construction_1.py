# import galois
# import hashlib
# import numpy as np
#
# class BchIbltConstruction1:
#     def __init__(self, r, d):
#         self.r = r  # Number of bits in each cell
#         self.bch, self.Hg = self.construct_bch_code(r, d)
#         self.size = self.Hg.shape[0]  # Determine the size based on Hg
#         self.table = np.zeros((self.size, self.bch.n), dtype=int)
#
#
#
#     # def construct_bch_code(self, r, d):
#     #     n0 = self.find_n0(r, d)
#     #     n = 2 ** (int(np.log2(n0 + 1))) - 1  # Ensure n is a power of 2 minus 1
#     #     bch_code = galois.BCH(n, d)
#     #     Hg = bch_code.H
#     #
#     #     # Resize Hg if necessary to match the size of the IBLT
#     #     if Hg.shape[0] != self.size:
#     #         Hg_resized = np.zeros((self.size, Hg.shape[1]), dtype=int)
#     #         Hg_resized[:Hg.shape[0], :] = Hg
#     #         Hg = Hg_resized
#     #
#     #     return bch_code, Hg
#
#     def construct_bch_code(self, r, d):
#         # Start with the maximum possible n for the given r
#         n = 2 ** r - 1
#
#         # Adjust d to ensure a valid BCH code
#         # Begin with the provided d and decrease if necessary
#         adjusted_d = d
#         while True:
#
#             try:
#                 # Attempt to create the BCH code
#                 bch_code = galois.BCH(n, d=adjusted_d)
#                 break
#             except ValueError:
#                 # Decrease d and try again
#                 adjusted_d -= 1
#                 if adjusted_d == 0:
#                     raise ValueError(f"No valid BCH code found for r = {r} and d = {d}")
#
#         Hg = bch_code.H
#         print(f"BCH parameters - n: {n}, k: {bch_code.k}, d: {d}")
#
#         return bch_code, Hg
#
#     def robust_hash_function(self, key):
#         key_bytes = str(key).encode()
#         hash_bytes = hashlib.sha256(key_bytes).digest()
#         return int.from_bytes(hash_bytes, byteorder='big') % self.size
#
#     def decode_data(self, encoded_data):
#         decoded_data_gf = self.bch.decode(encoded_data)
#         decoded_data_binary = decoded_data_gf.tolist()
#         decoded_data_bytes = bytes(int(''.join(map(str, decoded_data_binary[i:i+8])), 2) for i in range(0, len(decoded_data_binary), 8))
#         decoded_data = decoded_data_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
#         return decoded_data
#
#
#     def encode_data(self, data):
#         # Convert data to binary format
#         # print(f" data to encode  {data}")
#         data_bytes = str(data).encode() if not isinstance(data, bytes) else data
#         data_binary = [int(bit) for byte in data_bytes for bit in format(byte, '08b')]
#
#         # Check the message length k of the BCH code
#         k = self.bch.k
#         # print(f"BCH message length k: {k}")
#         # print(f"Length of binary data before padding/truncation: {len(data_binary)}")
#
#         # Truncate or pad the binary data to match k
#         if len(data_binary) > k:
#             data_binary = data_binary[:k]
#         else:
#             data_binary += [0] * (k - len(data_binary))
#
#         # Create a Galois Field array from the binary data
#         data_gf = self.bch.field(data_binary)
#
#         # Encode the data using the BCH encoder
#         data_bch = self.bch.encode(data_gf)
#         # print(f"Encoded data: {data_bch}")
#         # print(f"data_after decode {self.decode_data(np.array(data_bch, dtype=int))}")
#         return np.array(data_bch, dtype=int)
#
#     def insert(self, data):
#         print(f"Inserting data: {data}")
#         encoded_data = self.encode_data(data)
#         # print(f"Encoded data: {encoded_data}")
#         data_hash = self.robust_hash_function(data)
#         # print(f"Data hash: {data_hash}")
#         data_hash = data_hash % self.Hg.shape[1]
#         # print(f"Table index: {data_hash}")
#
#         for i in range(self.size):
#             if self.Hg[i, data_hash] != 0:
#                 # print(f"Updating table at index {i}: before={self.table[i]}, encoded_data={encoded_data}")
#                 self.table[i] = (self.table[i] + encoded_data) % 2  # Assuming binary field
#                 # print(f"Updated table at index {i}: {self.table[i]}")
#         # print("Insertion completed.")
#
#     # def delete(self, data):
#     #     print(f"Deleting data: {data}")
#     #     encoded_data = self.encode_data(data)
#     #     data_hash = self.robust_hash_function(data)
#     #     data_hash = data_hash % self.Hg.shape[1]
#     #
#     #     # Decode the data for confirmation before deletion
#     #     cell_index = None
#     #     for i in range(self.size):
#     #         if self.Hg[i, data_hash] != 0:
#     #             try:
#     #                 decoded_data = self.bch.decode(self.bch.field(self.table[i]))
#     #                 decoded_bytes = bytearray(
#     #                     int(''.join(map(str, decoded_data)), 2).to_bytes((len(decoded_data) + 7) // 8, byteorder='big'))
#     #                 decoded_str = decoded_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
#     #                 if decoded_str == data:
#     #                     cell_index = i
#     #                     break
#     #             except galois.GaloisException:
#     #                 continue
#     #
#     #     if cell_index is not None:
#     #         print(f"Found and deleting '{data}' at cell {cell_index}")
#     #         # Remove the encoded data from the appropriate cells
#     #         for i in range(self.size):
#     #             if self.Hg[i, data_hash] != 0:
#     #                 self.table[i] = (self.table[i] - encoded_data) % 2  # Assuming binary field
#     #     else:
#     #         print(f"Data '{data}' not found or could not be decoded for deletion")
#
#     def delete(self, data):
#         print(f"Deleting data: {data}")
#         encoded_data = self.encode_data(data)
#         data_hash = self.robust_hash_function(data)
#         data_hash = data_hash % self.Hg.shape[1]
#
#         for i in range(self.size):
#             if self.Hg[i, data_hash] != 0:
#                 self.table[i] = (self.table[i] - encoded_data) % 2  # Assuming binary field
#     def list_entries(self):
#         data_items = []
#         for i, cell in enumerate(self.table):
#             if np.any(cell):
#                 print(f"Cell {i} has data: {cell}")
#                 try:
#                     decoded_str = self.decode_data(cell)
#                     print(f"Decoded string at cell {i}: '{decoded_str}'")
#
#                     if decoded_str:
#                         data_items.append(decoded_str)
#                 except galois.GaloisException as e:
#                     print(f"Decoding error at cell {i}: {e}")
#         print(f"Listed Entries: {data_items}")
#         return data_items
#     # def list_entries(self):
#     #     data_items = []
#     #     for i, cell in enumerate(self.table):
#     #         if np.any(cell):
#     #             print(f"Cell {i} has data: {cell}")
#     #             try:
#     #                 decoded_data = self.bch.decode(self.bch.field(cell))
#     #                 print(f"Raw decoded data at cell {i}: {decoded_data}")
#     #
#     #                 # Convert decoded data to bytes and then to string
#     #                 decoded_bytes = int(''.join(map(str, decoded_data.tolist())), 2).to_bytes(
#     #                     (len(decoded_data) + 7) // 8, byteorder='big')
#     #                 print(f"Decoded bytes at cell {i}: {decoded_bytes}")
#     #
#     #                 data_str = decoded_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
#     #                 print(f"Decoded string at cell {i}: '{data_str}'")
#     #
#     #                 if data_str:
#     #                     data_items.append(data_str)
#     #             except galois.GaloisException as e:
#     #                 print(f"Decoding error at cell {i}: {e}")
#     #     print(f"Listed Entries: {data_items}")
#     #     return data_items
#
#
#
#
#
#
#
