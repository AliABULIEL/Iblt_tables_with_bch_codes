import galois
import hashlib
import numpy as np
import math

class BchIbltConstruction3:
    def __init__(self, r, d=4):  # d is fixed at 4 for this construction
        self.r = r
        self.d = d
        self.n0 = self.find_n0(r)
        self.bch = galois.BCH(self.n0, d=d)
        self.Hb4n0 = self.modify_Hb4n0(self.bch.H)
        self.Gc2 = self.create_Gc2()
        self.size = self.calculate_optimal_size()
        self.Hc2 = self.create_Hc2()
        self.table = np.zeros((self.size, self.bch.n - 1), dtype=int)  # Adjusted to n-1 based on modified H
        print(f"Optimal size: {self.size}, log2(n): {int(math.log2(2 ** self.r))}")

    def find_n0(self, r):
        n0 = 1
        while 2 * math.log2(n0 + 1) <= r:
            n0 *= 2
        n0 = n0 // 2  # Adjust to ensure it leads to a larger n
        n0 = 2 ** (int(math.log2(n0)) + 1) - 1
        return n0

    def modify_Hb4n0(self, H):
        # Remove the left-most column from H
        return H[:, 1:]

    def create_Gc2(self):
        n0 = self.n0
        alpha = galois.GF(2 ** self.r).primitive_element

        # Generate elements for Gc2 based on the pattern described in the article
        g_U = [alpha ** i for i in range(n0)]  # Upper part
        g_L = [alpha ** i for i in range(n0)]  # Lower part with the same pattern as the upper part

        # Combine g_U and g_L to form Gc2 according to the specific pattern
        Gc2 = np.vstack([g_U, np.zeros_like(g_U), g_L])
        return Gc2

    def create_Hc2(self):
        # Align Hc2 with Construction 3's specific pattern
        rows_to_repeat = (self.size // 3) + 1
        Hc2 = np.tile(self.Gc2, (rows_to_repeat, 1))
        return Hc2[:self.size, :]

    def calculate_optimal_size(self):
        # Recalculate the size based on Construction 3 formula
        n = 2 ** self.r
        s_star = int(np.ceil((2 * n / (3 * np.sqrt(n) - 4))) + 1)
        return s_star

    def robust_hash_function(self, key, seed=0):
        key_bytes = (str(key) + str(seed)).encode()
        hash_bytes = hashlib.sha256(key_bytes).digest()
        hash_value = int.from_bytes(hash_bytes, byteorder='big') % self.size
        return hash_value

    def multi_hash_function(self, key, num_hashes=5):
        return [self.robust_hash_function(key, seed) for seed in range(num_hashes)]

    def encode_data(self, data):
        data_bytes = data.encode('utf-8')
        data_binary = [int(bit) for byte in data_bytes for bit in format(byte, '08b')]

        k = self.Hc2.shape[1]
        if len(data_binary) > k:
            data_binary = data_binary[:k]  # Truncate if longer
        elif len(data_binary) < k:
            data_binary += [0] * (k - len(data_binary))  # Pad if shorter

        data_gf = data_binary
        return np.array(data_gf, dtype=int)

    def decode_data(self, encoded_data):
        try:
            if len(encoded_data) > self.Hc2.shape[1]:
                encoded_data = encoded_data[:self.Hc2.shape[1]]  # Trim to valid length

            binary_bytes = ''.join(map(str, encoded_data.tolist()))
            byte_array = bytearray(int(binary_bytes[i:i + 8], 2) for i in range(0, len(binary_bytes), 8))

            decoded_str = byte_array.decode('utf-8', errors='ignore')
            return decoded_str if decoded_str else "Undecodable or no data"
        except Exception as e:
            print(f"Decoding error: {e}")
            return "Undecodable or no data"

    def insert(self, data):
        encoded_data = self.encode_data(data)
        data_hashes = self.multi_hash_function(data)

        encoded_data = np.resize(encoded_data, self.table.shape[1])
        for data_hash in data_hashes:
            if not np.any(self.table[data_hash]):
                self.table[data_hash] = (self.table[data_hash] + encoded_data) % 2
                print(f"Data '{data}' inserted at table index {data_hash}.")
                return
        print(f"Failed to insert data '{data}': all hashed cells are occupied")

    def delete(self, data):
        encoded_data = self.encode_data(data)
        data_hashes = self.multi_hash_function(data)

        encoded_data = np.resize(encoded_data, self.table.shape[1])
        for data_hash in data_hashes:
            if np.array_equal(self.table[data_hash], encoded_data):
                self.table[data_hash] = (self.table[data_hash] - encoded_data) % 2
                print(f"Data '{data}' deleted from table index {data_hash}.")
                return
        print(f"Failed to delete data '{data}': no matching cell found")

    def list_entries(self):
        data_items = []
        for i, cell in enumerate(self.table):
            decoded_str = self.decode_data(cell)
            print(f"Decoded Word at Cell {i}: '{decoded_str}'")
            if decoded_str and decoded_str != "Undecodable or no data" and decoded_str.rstrip('\x00') !='':
                data_items.append(decoded_str.rstrip('\x00'))
        print(f"List entries result is  {data_items}")
        return data_items

