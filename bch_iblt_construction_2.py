import galois
import hashlib
import numpy as np
import math

class BchIbltConstruction2:
    def __init__(self, r, d):
        self.r = r  # Number of bits in each cell
        self.d = d
        self.n0 = self.find_n0(r, d)
        self.bch, self.H2 = self.construct_bch_code(self.n0, d)
        self.size = self.calculate_optimal_size()
        self.table = np.zeros((self.size, 2 ** r), dtype=int)

    def calculate_optimal_size(self):
        # Assuming n = 2^r - 1 for the BCH code
        n = 2 ** self.r - 1
        # Adjust the formula as per the interpretation for s^*
        s_star = math.ceil((2 * np.sqrt(self.d) / (n - 2)) * np.log2(n))
        return s_star

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
        print(f"n0 = {n0}, d= {d}")
        while True:
            try:
                bch_code = galois.BCH(n, d=adjusted_d)
                break
            except ValueError:
                adjusted_d -= 1
                print(f"Adjusting d to {adjusted_d} due to failure in BCH code creation")
                if adjusted_d == 0:
                    raise ValueError(f"No valid BCH code found for n = {n} and d = {d}")
        Hg = bch_code.H
        H_upper, H_lower = np.array_split(Hg, 2)
        H2 = self.construct_H2(H_upper, H_lower)
        print(f"Successful BCH code creation - n: {n}, k: {bch_code.k}, adjusted d: {adjusted_d}")
        return bch_code, H2

    def construct_H2(self, H_upper, H_lower):
        """
        Construct the H2 matrix from the upper (H_upper) and lower (H_lower) halves of a BCH parity-check matrix.
        Rows are alternated between H_upper and H_lower to form H2 as per Construction 2.
        """
        H2 = []  # Initialize an empty list to hold the alternated rows

        # Determine the maximum number of rows to iterate over
        max_rows = max(H_upper.shape[0], H_lower.shape[0])

        for i in range(max_rows):
            if i < H_upper.shape[0]:
                H2.append(H_upper[i, :])  # Add row from H_upper
            if i < H_lower.shape[0]:
                H2.append(H_lower[i, :])  # Add row from H_lower

        # Convert the list of arrays into a single numpy array
        H2 = np.vstack(H2)
        self.test_H2_alternation(H2, H_upper, H_lower)
        return H2
    def test_H2_alternation(self,H2, H_upper, H_lower):
        for i in range(0, min(len(H_upper), len(H_lower)) * 2, 2):
            assert np.array_equal(H2[i], H_upper[i // 2]), "Upper row does not match"
            assert np.array_equal(H2[i + 1], H_lower[i // 2]), "Lower row does not match"
        print("Alternation verification passed!")
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

    def insert(self, data):
        encoded_data = self.encode_data(data)
        data_hash = self.robust_hash_function(data)

        # Resize encoded_data to match the size of table's row
        encoded_data = np.resize(encoded_data, self.table.shape[1])

        for i in range(self.size):
            if self.H2[i, data_hash % self.H2.shape[1]] != 0:
                self.table[i] = (self.table[i] + encoded_data) % 2
        print(f"Data '{data}' inserted.")


    def delete(self, data):
        encoded_data = self.encode_data(data)
        data_hash = self.robust_hash_function(data)

        # Resize encoded_data to match the size of table's row
        encoded_data = np.resize(encoded_data, self.table.shape[1])

        for i in range(self.size):
            if self.H2[i, data_hash % self.H2.shape[1]] != 0:
                self.table[i] = (self.table[i] - encoded_data) % 2
        print(f"Deleting data '{data}' from cell {i}")

    def list_entries(self):
        data_items = []
        for i, cell in enumerate(self.table):
            print(f"Cell {i} contents: {cell}")
            decoded_str = self.decode_data(cell)
            print(f"Decoded Word at Cell {i}: '{decoded_str}'")
            if decoded_str and decoded_str != "Undecodable or no data":
                data_items.append(decoded_str)
        return data_items

