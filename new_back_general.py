import bchlib
import hashlib
import math

class BCHIBLT:
    def __init__(self, size, bch_polynomial, bch_bits, d):
        self.size = size
        self.bch = bchlib.BCH(bch_polynomial, bch_bits)
        self.max_count = 2 ** int(math.ceil(math.log2(d)))  # Max value for count based on d
        self.table = [{'count': 0, 'xorSum': bytearray(self.bch.n)} for _ in range(size)]

    def robust_hash_function(self, key):
        key_bytes = str(key).encode()
        hash_bytes = hashlib.sha256(key_bytes).digest()
        return int.from_bytes(hash_bytes, byteorder='big') % self.size

    def encode_data(self, data):
        data_bytes = str(data).encode().ljust(self.bch.n - self.bch.ecc_bytes, b'\0')
        data_bch = self.bch.encode(data_bytes)
        return data_bch

    def insert(self, data):
        encoded_data = self.encode_data(data)
        data_hash = self.robust_hash_function(data)
        cell = self.table[data_hash]
        cell['count'] = (cell['count'] + 1) % self.max_count
        cell['xorSum'] = bytearray(a ^ b for a, b in zip(cell['xorSum'], encoded_data))

    def delete(self, data):
        encoded_data = self.encode_data(data)
        data_hash = self.robust_hash_function(data)
        cell = self.table[data_hash]
        cell['count'] = (cell['count'] - 1) % self.max_count
        cell['xorSum'] = bytearray(a ^ b for a, b in zip(cell['xorSum'], encoded_data))

    def list_entries(self):
        entries = []
        for cell in self.table:
            if cell['count'] != 0:
                try:
                    # Attempt to decode the data
                    packet = bytearray(self.bch.decode(cell['xorSum'])[1])
                    data = packet.decode().rstrip('\x00')
                    entries.append((data, cell['count']))
                except bchlib.BCHException as e:
                    print(f"Decoding error for cell: {e}")
        return entries

    def peel(self):
        peeled_data = []
        while True:
            made_progress = False
            for i, cell in enumerate(self.table):
                if cell['count'] == 1:
                    try:
                        packet = bytearray(self.bch.decode(cell['xorSum'])[1])
                        data = packet.decode().rstrip('\x00')
                        peeled_data.append(data)

                        encoded_data = self.encode_data(data)
                        cell['count'] = (cell['count'] - 1) % self.max_count
                        cell['xorSum'] = bytearray(a ^ b for a, b in zip(cell['xorSum'], encoded_data))

                        made_progress = True
                    except bchlib.BCHException as e:
                        print(f"Decoding error: {e}")

            if not made_progress:
                break

        return peeled_data

# Example usage
bch_polynomial = 8219  # Example polynomial
bch_bits = 16          # Example bits
d = 1024               # Example maximum number of insertions/deletions
iblt = BCHIBLT(10, bch_polynomial, bch_bits, d)

# Inserting data
iblt.insert("data1")
iblt.insert("data2")

# Deleting data
iblt.delete("data1")

# Peeling process to recover data
recovered_data = iblt.peel()
print("Recovered Data:", recovered_data)
