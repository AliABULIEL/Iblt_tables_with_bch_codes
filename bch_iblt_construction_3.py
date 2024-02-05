import galois
import hashlib
import numpy as np


class BchIbltConstruction3:
    def __init__(self, r, d):
        self.r = r  # Number of bits in each cell
        self.d = d
        self.n0 = self.find_n0(r, d)
        self.Hb4n0 = self.create_Hb4n0(self.n0)
        self.H_U, self.H_L, self.g_U, self.g_L = self.create_H_U_L(self.Hb4n0)
        self.Gc2 = self.create_Gc2(self.g_U, self.g_L)
        self.Hc2 = self.create_Hc2(self.Gc2)
        self.size = self.Hc2.shape[0]
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

    def create_Hb4n0(self, n0):
        # Create an empty matrix of zeros with dimensions (n0, n0 - 1)
        Hb4n0 = np.zeros((n0, n0 - 1), dtype=int)

        # Fill the matrix according to Construction 3 in the article
        for i in range(n0):
            for j in range(n0 - 1):
                if (j % n0) == ((i * 2) % n0):
                    Hb4n0[i, j] = 1

        return Hb4n0

    def create_H_U_L(self, Hb4n0):
        # Split Hb4n0 into upper and lower halves H(U) and H(L)
        H_U = Hb4n0[:, :Hb4n0.shape[1] // 2]
        H_L = Hb4n0[:, Hb4n0.shape[1] // 2:]

        # Generate random binary vectors g(U) and g(L)
        g_U = np.random.randint(2, size=H_U.shape[1])
        g_L = np.random.randint(2, size=H_L.shape[1])

        return H_U, H_L, g_U, g_L

    def create_Gc2(self, g_U, g_L):
        # Create the Gc2 matrix based on g(U) and g(L)
        Gc2 = np.zeros((3, len(g_U) + len(g_L)), dtype=int)
        Gc2[0, :len(g_U)] = g_U
        Gc2[1, :len(g_U)] = g_U
        Gc2[2, len(g_U):] = g_L

        return Gc2

    def create_Hc2(self, Gc2):
        # Create the Hc2 matrix based on Gc2
        Hc2 = np.tile(Gc2, (Gc2.shape[0], 1))
        return Hc2

    def robust_hash_function(self, key, hash1='sha256', hash2='md5'):
        key_bytes = str(key).encode()

        # First hash function
        hash1_bytes = hashlib.new(hash1, key_bytes).digest()
        hash1_int = int.from_bytes(hash1_bytes, byteorder='big')

        # Second hash function
        hash2_bytes = hashlib.new(hash2, key_bytes).digest()
        hash2_int = int.from_bytes(hash2_bytes, byteorder='big')

        # Combine hashes using double hashing technique
        combined_hash = (hash1_int + hash2_int) % self.size
        return combined_hash

    def encode_data(self, data):
        # Convert data to binary format
        data_bytes = str(data).encode()
        data_binary = [int(bit) for byte in data_bytes for bit in format(byte, '08b')]

        k = self.Hc2.shape[1]
        # Adjust data length to match Hc2 matrix row size
        if len(data_binary) > k:
            data_binary = data_binary[:k]  # Truncate if longer
        elif len(data_binary) < k:
            data_binary += [0] * (k - len(data_binary))  # Pad if shorter

        data_gf = data_binary
        return np.array(data_gf, dtype=int)

    def insert(self, data):
        print(f"Inserting data: '{data}'")
        encoded_data = self.encode_data(data)
        print(f"Encoded data: {encoded_data}")
        data_hash = self.robust_hash_function(data)
        print(f"Data hash: {data_hash}")

        for i in range(self.size):
            if self.Hc2[i, data_hash % self.Hc2.shape[1]] != 0:
                encoded_data = np.resize(encoded_data, self.table[i].size)
                self.table[i] = (self.table[i] + encoded_data) % 2
                print(f"Updating cell {i}: {self.table[i]}")
        print(f"Data '{data}' successfully inserted.")

    def delete(self, data):
        print(f"Deleting data: '{data}'")
        encoded_data = self.encode_data(data)
        print(f"Encoded data: {encoded_data}")
        data_hash = self.robust_hash_function(data)
        print(f"Data hash: {data_hash}")

        for i in range(self.size):
            if self.Hc2[i, data_hash % self.Hc2.shape[1]] != 0:
                encoded_data = np.resize(encoded_data, self.table[i].size)
                self.table[i] = (self.table[i] - encoded_data) % 2
                print(f"Updating cell {i}: {self.table[i]}")
        print(f"Data '{data}' successfully deleted.")

    def list_entries(self):
        data_items = []
        for i, cell in enumerate(self.table):
            print(f"Cell {i} contents: {cell}")
            decoded_str = self.decode_data(cell)
            print(f"Decoded Word at Cell {i}: '{decoded_str}'")
            if decoded_str and decoded_str != "Undecodable or no data":
                data_items.append(decoded_str)
        return data_items

    def decode_data(self, encoded_data):
        try:
            if len(encoded_data) > self.Hc2.shape[1]:
                encoded_data = encoded_data[:self.Hc2.shape[1]]  # Trim to valid length

            decoded_data_binary = encoded_data.tolist()
            decoded_bytes = bytes(
                int(''.join(map(str, decoded_data_binary[i:i + 8])), 2)
                for i in range(0, len(decoded_data_binary), 8)
            )
            decoded_str = decoded_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
            return decoded_str if decoded_str else "Undecodable or no data"
        except Exception as e:
            print(f"Decoding error: {e}")
            return "Undecodable or no data"


# # Example usage:
# r = 8  # Number of bits in each cell
# d = 4  # Distance parameter
# iblt = BchIbltConstruction3(r, d)
#
# iblt.insert("Alice")
# iblt.insert("Bob")
# iblt.insert("Charlie")
#
# entries = iblt.list_entries()
# print("Data Entries:")
# for entry in entries:
#     print(entry)
