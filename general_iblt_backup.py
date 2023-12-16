import bchlib
import hashlib
import numpy as np

class GeneralBCHIBLT:
    def __init__(self, size, bch_polynomial, bch_bits):
        self.size = size
        self.bch = bchlib.BCH(bch_polynomial, bch_bits)
        self.table = [{'count': 0, 'xorSum': bytearray(self.bch.n)} for _ in range(size)]

    def robust_hash_function(self, key):
        # Using SHA-256 hash function for robust hashing
        key_bytes = str(key).encode()
        hash_bytes = hashlib.sha256(key_bytes).digest()
        return int.from_bytes(hash_bytes, byteorder='big') % self.size

    def encode_data(self, data):
        # Convert data to bytes and pad to the correct length for BCH
        data_bytes = str(data).encode().ljust(self.bch.n - self.bch.ecc_bytes, b'\0')
        data_bch = self.bch.encode(data_bytes)
        return data_bch

    def insert(self, data):
        encoded_data = self.encode_data(data)
        data_hash = self.robust_hash_function(data)
        cell = self.table[data_hash]
        cell['count'] += 1
        cell['xorSum'] = bytearray(a ^ b for a, b in zip(cell['xorSum'], encoded_data))

    def delete(self, data):
        encoded_data = self.encode_data(data)
        data_hash = self.robust_hash_function(data)
        cell = self.table[data_hash]
        cell['count'] -= 1
        cell['xorSum'] = bytearray(a ^ b for a, b in zip(cell['xorSum'], encoded_data))

    def list_entries(self):
        data_items = []
        for cell in self.table:
            if cell['count'] == 1:
                try:
                    packet = bytearray(self.bch.decode(cell['xorSum'])[1])
                    data = packet.decode().rstrip('\x00')
                    data_items.append(data)
                except bchlib.BCHException as e:
                    print(f"Decoding error: {e}")
        return data_items

# Example usage
bch_polynomial = 8219  # Example polynomial, adjust as needed
bch_bits = 16          # Example bits, adjust as needed
iblt = GeneralBCHIBLT(10, bch_polynomial, bch_bits)

# Inserting data
iblt.insert("data1")
iblt.insert("data2")

# Deleting data
iblt.delete("data1")

# Listing entries
print("List Entries:", iblt.list_entries())
