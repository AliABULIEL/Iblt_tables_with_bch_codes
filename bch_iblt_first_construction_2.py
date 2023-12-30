import galois
import hashlib
import numpy as np


class BchIbltConstruction2:
    def __init__(self, r, d):
        self.r = r  # Number of bits in each cell
        self.d = d
        self.n0 = self.find_n0(r, d)
        self.bch, self.H2 = self.construct_bch_code(self.n0, d)
        self.size = self.H2.shape[0]
        self.table = np.zeros((self.size, 2 ** r), dtype=int)

    def find_n0(self, r, d):
        """
        Find the largest power of 2, n0 + 1, such that d * log2(n0 + 1) <= 2r.
        """
        n0 = 1
        while d * np.log2(n0 + 1) <= 2 * r:
            n0 *= 2
        n0 = n0 // 2
        # Adjust n0 to ensure it leads to a larger n
        n0 = 2 ** (int(np.log2(n0)) + 1) - 1
        return n0

    def construct_bch_code(self, n0, d):
        """
        Create BCH code based on n0 and d. Construct the H2 matrix.
        """
        # Use n0 directly as n
        n = n0
        adjusted_d = d
        while True:
            try:
                bch_code = galois.BCH(n, d=adjusted_d)
                print(f"Successful BCH code creation - n: {n}, k: {bch_code.k}, adjusted d: {adjusted_d}")
                break
            except ValueError:
                adjusted_d -= 1
                print(f"Adjusting d to {adjusted_d} due to failure in BCH code creation")
                if adjusted_d == 0:
                    raise ValueError(f"No valid BCH code found for n = {n} and d = {d}")

        Hg = bch_code.H
        H_upper = Hg[:Hg.shape[0] // 2, :]
        H_lower = Hg[Hg.shape[0] // 2:, :]
        H2 = self.construct_H2(H_upper, H_lower)
        return bch_code, H2

    def construct_H2(self, H_upper, H_lower):
        """
        Construct the H2 matrix from the upper (H_upper) and lower (H_lower) halves of a BCH parity-check matrix.
        """
        rows_upper = H_upper.shape[0]
        rows_lower = H_lower.shape[0]
        H2_blocks = []

        for i in range(max(rows_upper, rows_lower)):
            if i < rows_upper:
                H2_blocks.append(H_upper[i, :])
            if i < rows_lower:
                H2_blocks.append(H_lower[i, :])

        H2 = np.vstack(H2_blocks)
        return H2

    def robust_hash_function(self, key):
        key_bytes = str(key).encode()
        hash_bytes = hashlib.sha256(key_bytes).digest()
        return int.from_bytes(hash_bytes, byteorder='big') % self.size

    def encode_data(self, data):
        # Convert data to binary format
        data_bytes = str(data).encode()
        data_binary = [int(bit) for byte in data_bytes for bit in format(byte, '08b')]

        k = self.bch.k
        # Adjust data length to match BCH code length k
        if len(data_binary) > k:
            data_binary = data_binary[:k]  # Truncate if longer
        elif len(data_binary) < k:
            data_binary += [0] * (k - len(data_binary))  # Pad if shorter

        data_gf = self.bch.field(data_binary)
        encoded_data = self.bch.encode(data_gf)
        return np.array(encoded_data, dtype=int)

    # def encode_data(self, data):
    #     # Convert data to binary format
    #     data_bytes = str(data).encode()
    #     data_binary = [int(bit) for byte in data_bytes for bit in format(byte, '08b')]
    #     # print(f"Initial Binary Data: {data_binary} , length data {len(data_binary)}")  # Debug print
    #
    #     k = self.bch.k
    #     # print(f"BCH message length k: {k}")  # Debug print
    #
    #     # Adjust data length to match BCH code length k
    #     if len(data_binary) > k:
    #         data_binary = data_binary[:k]
    #     elif len(data_binary) < k:
    #         data_binary += [0] * (k - len(data_binary))
    #     # print(f"Adjusted Binary Data: {data_binary}")  # Debug print
    #
    #     data_gf = self.bch.field(data_binary)
    #     encoded_data = self.bch.encode(data_gf)
    #     # print(f"Encoded Data: {encoded_data}")  # Debug print
    #
    #     return np.array(encoded_data, dtype=int)

    def decode_data(self, encoded_data):
        try:
            if len(encoded_data) > self.bch.n:
                encoded_data = encoded_data[:self.bch.n]  # Trim to valid length

            decoded_data_gf = self.bch.decode(encoded_data)
            decoded_data_binary = decoded_data_gf.tolist()
            decoded_bytes = bytes(
                int(''.join(map(str, decoded_data_binary[i:i + 8])), 2)
                for i in range(0, len(decoded_data_binary), 8)
            )
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
            return decoded_str if decoded_str else "Undecodable or no data"
        except Exception as e:
            print(f"Decoding error: {e}")
            return "Undecodable or no data"

    # def decode_data(self, encoded_data):
    #     try:
    #         # Ensure encoded_data is 1-D and the correct size
    #         if len(encoded_data) > self.bch.n:
    #             encoded_data = encoded_data[:self.bch.n]
    #
    #         decoded_data_gf = self.bch.decode(encoded_data)
    #         decoded_data_binary = decoded_data_gf.tolist()
    #         decoded_data_bytes = bytes(
    #             int(''.join(map(str, decoded_data_binary[i:i + 8])), 2)
    #             for i in range(0, len(decoded_data_binary), 8)
    #         )
    #         return decoded_data_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
    #     except Exception as e:
    #         print(f"Decoding error: {e}")
    #         return "Undecodable or no data"

    # def insert(self, data):
    #     encoded_data = self.encode_data(data)
    #     data_hash = self.robust_hash_function(data)
    #
    #     # Ensure encoded_data is the same size as the table's row
    #     if len(encoded_data) < self.table.shape[1]:
    #         # Pad encoded_data to match the size
    #         padding = np.zeros(self.table.shape[1] - len(encoded_data), dtype=int)
    #         encoded_data = np.concatenate((encoded_data, padding))
    #
    #     for i in range(self.size):
    #         if self.H2[i, data_hash % self.H2.shape[1]] != 0:
    #             self.table[i] = (self.table[i] + encoded_data) % 2
    def insert(self, data):
        encoded_data = self.encode_data(data)
        data_hash = self.robust_hash_function(data)

        # Resize encoded_data to match the size of table's row
        encoded_data = np.resize(encoded_data, self.table.shape[1])

        for i in range(self.size):
            if self.H2[i, data_hash % self.H2.shape[1]] != 0:
                self.table[i] = (self.table[i] + encoded_data) % 2
        print(f"Data '{data}' inserted.")

    # def insert(self, data):
    #     encoded_data = self.encode_data(data)
    #     data_hash = self.robust_hash_function(data)
    #
    #     if len(encoded_data) < self.table.shape[1]:
    #         padding = np.zeros(self.table.shape[1] - len(encoded_data), dtype=int)
    #         encoded_data = np.concatenate((encoded_data, padding))
    #
    #     for i in range(self.size):
    #         if self.H2[i, data_hash % self.H2.shape[1]] != 0:
    #             self.table[i] = (self.table[i] + encoded_data) % 2
    #     print(f"Data inserted: {data}")

    def delete(self, data):
        encoded_data = self.encode_data(data)
        data_hash = self.robust_hash_function(data)

        # Resize encoded_data to match the size of table's row
        encoded_data = np.resize(encoded_data, self.table.shape[1])

        for i in range(self.size):
            if self.H2[i, data_hash % self.H2.shape[1]] != 0:
                self.table[i] = (self.table[i] - encoded_data) % 2
        print(f"Deleting data '{data}' from cell {i}")

    # def delete(self, data):
    #     encoded_data = self.encode_data(data)
    #     data_hash = self.robust_hash_function(data)
    #
    #     if len(encoded_data) < self.table.shape[1]:
    #         padding = np.zeros(self.table.shape[1] - len(encoded_data), dtype=int)
    #         encoded_data = np.concatenate((encoded_data, padding))
    #
    #     for i in range(self.size):
    #         if self.H2[i, data_hash % self.H2.shape[1]] != 0:
    #             self.table[i] = (self.table[i] - encoded_data) % 2
    #     print(f"Data deleted: {data}")

    # def delete(self, data):
    #     encoded_data = self.encode_data(data)
    #     data_hash = self.robust_hash_function(data)
    #
    #     # Pad encoded_data to match the size of the table's row
    #     if len(encoded_data) < self.table.shape[1]:
    #         padding = np.zeros(self.table.shape[1] - len(encoded_data), dtype=int)
    #         encoded_data = np.concatenate((encoded_data, padding))
    #
    #     for i in range(self.size):
    #         if self.H2[i, data_hash % self.H2.shape[1]] != 0:
    #             self.table[i] = (self.table[i] - encoded_data) % 2



    def list_entries(self):
        data_items = []
        for i, cell in enumerate(self.table):
            print(f"Cell {i} contents: {cell}")
            decoded_str = self.decode_data(cell)
            print(f"Decoded Word at Cell {i}: '{decoded_str}'")
            if decoded_str and decoded_str != "Undecodable or no data":
                data_items.append(decoded_str)
        return data_items

