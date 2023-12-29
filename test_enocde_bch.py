import galois
import numpy as np

# Adjusted BCH parameters for "hello world"
n = 1023  # Codeword length
d = 5     # Error-correcting capability
bch_code = galois.BCH(n, d=d)
print(bch_code.k)
# Sample data
data = "hello world"

# Encoding process
data_bytes = data.encode()
data_binary = [int(bit) for byte in data_bytes for bit in format(byte, '08b')]

# Check the message length k of the BCH code
k = bch_code.k
print(f"BCH message length k: {k}")
print(f"Length of binary data before padding/truncation: {len(data_binary)}")

# Truncate or pad the binary data to match k
if len(data_binary) > k:
    data_binary = data_binary[:k]
else:
    data_binary += [0] * (k - len(data_binary))

# Create a Galois Field array from the binary data
data_gf = bch_code.field(data_binary)

# Encode the data using the BCH encoder
data_bch = bch_code.encode(data_gf)
print(f"Encoded data: {data_bch}")

# Decoding process
decoded_data_gf, n_errors_corrected = bch_code.decode(data_bch, errors=True)
decoded_data_binary = decoded_data_gf.tolist()

# Convert binary data back to string
decoded_data_bytes = bytes(int(''.join(map(str, decoded_data_binary[i:i+8])), 2) for i in range(0, len(decoded_data_binary), 8))
decoded_data = decoded_data_bytes.decode('utf-8', errors='ignore').rstrip('\x00')

# Output original, decoded data, and number of corrected errors
print(f"Original Data: {data}")
print(f"Decoded Data: {decoded_data}")
print(f"Number of Errors Corrected: {n_errors_corrected}")
