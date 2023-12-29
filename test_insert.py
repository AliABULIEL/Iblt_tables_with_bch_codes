from bch_iblt_first_construction_1 import BchIbltConstruction1
def test_insert_method():
    r = 10  # Number of bits in each cell
    d = 3   # Error-correcting capability

    # Initialize the IBLT
    iblt = BchIbltConstruction1(r, d)

    # Insert a test data string
    iblt.insert("hello")
    iblt.insert("world")
    iblt.insert("love")
    iblt.insert("like")

    # Show the updated table
    print("Updated table:")
    for i, cell in enumerate(iblt.table):
        print(f"Cell {i}: {cell}")
    iblt.delete("love")
    for i, cell in enumerate(iblt.table):
        print(f"Cell {i}: {cell}")

# Run the test
test_insert_method()