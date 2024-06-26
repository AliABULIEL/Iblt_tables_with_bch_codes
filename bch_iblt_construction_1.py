import galois
import hashlib
import numpy as np
import math

class BchIbltConstruction1:
    def __init__(self, r, d):
        """
        Initialize the BCH IBLT with given parameters r (bits per cell) and d (minimum distance).
        Constructs the BCH code and initializes the lookup table.
        """
        self.r = r  # Number of bits in each cell
        self.d = d  # Minimum distance
        self.bch, self.Hg = self.construct_bch_code(r, d)
        self.size = self.Hg.shape[0]  # Adjust size based on calculated m
        self.table = np.zeros((self.size, self.bch.n), dtype=int)  # Initialize the table with zeros

    def construct_bch_code(self, r, d):
        """
        Construct a BCH code with parameters r and d.
        Adjusts d if necessary to find a valid BCH code.
        """
        n = 2 ** r - 1
        adjusted_d = d
        while True:
            try:
                bch_code = galois.BCH(n, d=adjusted_d)
                break
            except ValueError:
                adjusted_d -= 1
                if adjusted_d <= 0:
                    raise ValueError(f"No valid BCH code found for r = {r} and d = {d}")
        Hg = bch_code.H
        print(f"BCH parameters - n: {n}, k: {bch_code.k}, d: {adjusted_d}")
        return bch_code, Hg

    def robust_hash_function(self, key, seed):
        """
        Generate a robust hash value for a given key using SHA-256 and a seed.
        The hash value is mapped to the size of the lookup table.
        """
        key_bytes = (str(key) + str(seed)).encode()
        hash_bytes = hashlib.sha256(key_bytes).digest()
        hash_value = int.from_bytes(hash_bytes, byteorder='big') % self.size
        # print(f"Hash for key '{key}' with seed {seed}: {hash_value}")
        return hash_value

    def multi_hash_function(self, key, num_hashes=3):
        """
        Generate multiple hash values for a given key using different seeds.
        """
        return [self.robust_hash_function(key, seed) for seed in range(num_hashes)]

    def encode_data(self, data):
        """
        Encode data using the BCH encoder.
        Converts data to binary format, pads or truncates it to match the BCH message length, and encodes it.
        """
        data_bytes = str(data).encode() if not isinstance(data, bytes) else data
        data_binary = [int(bit) for byte in data_bytes for bit in format(byte, '08b')]

        k = self.bch.k

        if len(data_binary) > k:
            data_binary = data_binary[:k]
        else:
            data_binary += [0] * (k - len(data_binary))

        data_gf = self.bch.field(data_binary)
        data_bch = self.bch.encode(data_gf)
        return np.array(data_bch, dtype=int)

    def decode_data(self, encoded_data):
        """
        Decode data from the BCH encoded format back to the original format.
        Handles conversion from binary to string.
        """
        decoded_data_gf = self.bch.decode(encoded_data)
        decoded_data_binary = decoded_data_gf.tolist()
        decoded_data_bytes = bytes(int(''.join(map(str, decoded_data_binary[i:i+8])), 2) for i in range(0, len(decoded_data_binary), 8))
        decoded_data = decoded_data_bytes.decode('utf-8', errors='ignore').rstrip('\x00')
        return decoded_data

    def insert(self, data):
        """
        Insert data into the IBLT. Encodes the data, hashes it, and updates one relevant cell in the table.
        """
        if len(self.table) < 1:
            raise ValueError("Table must have at least one row.")

        encoded_data = self.encode_data(data)
        data_hashes = self.multi_hash_function(data)
        print(f"Inserting data '{data}' with encoded form: {encoded_data}")

        for data_hash in data_hashes:
            if not np.any(self.table[data_hash]):
                self.table[data_hash] = (self.table[data_hash] + encoded_data) % 2  # Assuming binary field
                print(f"Inserted data '{data}' at table index {data_hash}")
                return  # Ensure only one cell is updated
        print(f"Failed to insert data '{data}': all hashed cells are occupied")

    def delete(self, data):
        encoded_data = self.encode_data(data)
        data_hashes = self.multi_hash_function(data)

        # Resize encoded_data to match the size of table's row
        encoded_data = np.resize(encoded_data, self.table.shape[1])

        for data_hash in data_hashes:
            for i in range(self.size):
                if np.array_equal(self.table[i], encoded_data):
                    self.table[i] = (self.table[i] - encoded_data) % 2
                    print(f"Data '{data}' deleted from table index {i}.")
                    return  # Ensure only one cell is updated
        print(f"Failed to delete data '{data}': no matching cell found")

    def list_entries(self):
        """
        List all entries in the IBLT by decoding the data in each cell.
        """
        data_items = []
        for i, cell in enumerate(self.table):
            if np.any(cell):
                try:
                    decoded_str = self.decode_data(cell)
                    if decoded_str:
                        data_items.append(decoded_str)
                except galois.GaloisException as e:
                    print(f"Decoding error at cell {i}: {e}")
        print(f"list entries result is {data_items}")
        return data_items




