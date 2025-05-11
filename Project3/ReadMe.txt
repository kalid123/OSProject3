1 Command: python main.py create test.idx

What it does:
Creates a new B-Tree index file named test.idx.
Purpose:
Initializes the data structure for future insertions. Think of it as creating a blank database index.

2 Command: python main.py insert test.idx 15 100

What it does:
Inserts a key-value pair (15, 100) into the B-Tree stored in test.idx.
Purpose:
Adds a single record (index entry) to the B-Tree.

3 Command: python main.py search test.idx 15
 
What it does:
Searches for the key 15 in the B-Tree and prints its associated value (100 in this case if it was inserted before).
Purpose:
Retrieve a value by key — like looking up a value in an indexed database.

4 Command: python main.py print test.idx

What it does:
Prints a human-readable representation of the current state of the B-Tree in test.idx.
Purpose:
Useful for debugging — lets you visualize the structure (nodes, keys, children).

5 Command: python main.py load test.idx input.csv

What it does:
Loads data from input.csv, which is expected to contain rows of key-value pairs, and inserts them into the B-Tree.
Purpose:
Bulk insertion of many records into the B-Tree from a CSV file.

6 Command: python main.py extract test.idx output.csv

What it does:
Traverses the B-Tree and writes all key-value pairs to output.csv.
Purpose:
Export the B-Tree data in sorted order (in-order traversal) to a file — useful for verification or external use.



Note: I also added 2 test cases to run the test cases just write
Command: pytest ( if pytest is not installed first run pip install pytest)