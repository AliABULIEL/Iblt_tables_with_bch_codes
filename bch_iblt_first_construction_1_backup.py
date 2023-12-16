import galois
import hashlib
import numpy as np

class BchIbltFirstConstruction1:
    def __init__(self, size, r, d):
        self.size = size
        self.r = r  # Number of bits in each cell
        self.bch = self.construct_bch_code(r, d)
        self.table = np.zeros((size, self.bch.n), dtype=int)  # Adjust size based on BCH code word length
        self.H = self.bch.parity_check_matrix.astype(int)  # Use BCH parity-check matrix for IBLT mapping

    def construct_bch_code(self, r, d):
        GF = galois.GF(2**r)
        alpha = GF.primitive_elements[0]
        n = 2**r - 1
        n0 = int(2 ** (d * np.log2(n + 1) // r) - 1)
        g = [0] + [alpha**i for i in range(int(n0))]
        print("g is ")
        print(g)
        Hg_rows = [g + [0]*(n - len(g))] * (n // n0)
        print(" HG rows")
        print(Hg_rows)
        Hg = np.array(Hg_rows, dtype=int)

        Hg_poly = galois.Poly(Hg[0], field=GF)
        print("Hg poly is ")
        print(Hg_poly)

        bch_code = galois.BCH(n, 1)
        print(bch_code.parity_check_poly)
        print(bch_code.generator_poly)
        print(bch_code.H)
        print("Hg")
        print(Hg)
        print("!!!!!!!")
        return bch_code, Hg

    def robust_hash_function(self, key):
        key_bytes = str(key).encode()
        hash_bytes = hashlib.sha256(key_bytes).digest()
        return int.from_bytes(hash_bytes, byteorder='big') % self.size

    def encode_data(self, data):
        if isinstance(data, int):
            data_bytes = str(data).encode()
        elif isinstance(data, str):
            data_bytes = data.encode()
        else:
            raise ValueError("Unsupported data type")

        data_bytes = data_bytes.ljust(self.bch.n - self.bch.t * 2, b'\0')
        data_bch = self.bch.encode(self.bch.field(data_bytes))
        return np.array(data_bch, dtype=int)

    def insert(self, data):
        encoded_data = self.encode_data(data)
        data_hash = self.robust_hash_function(data)
        for i in range(self.size):
            if self.H[i, data_hash] != 0:
                self.table[i] = (self.table[i] + encoded_data) % self.bch.field.characteristic

    def delete(self, data):
        encoded_data = self.encode_data(data)
        data_hash = self.robust_hash_function(data)
        for i in range(self.size):
            if self.H[i, data_hash] != 0:
                self.table[i] = (self.table[i] - encoded_data) % self.bch.field.characteristic

    def list_entries(self):
        data_items = []
        for i, cell in enumerate(self.table):
            if np.sum(cell) != 0:
                try:
                    packet = bytearray(self.bch.decode(self.bch.field(cell))[1])
                    data = packet.decode().rstrip('\x00')
                    data_items.append(data)
                except galois.GaloisException as e:
                    print(f"Decoding error at cell {i}: {e}")
        return data_items


