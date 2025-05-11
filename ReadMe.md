# B-Tree Index Tool

A simple command-line tool for creating, managing, and querying a B-Tree index stored in a binary file. Useful for learning B-Tree data structures or as a lightweight index for small datasets.

## Features

* Create a new index file
* Insert and search key-value pairs
* Bulk load from CSV
* Export (extract) data in sorted order
* Print a human-readable tree structure for debugging

## Prerequisites

* Python 3.7 or higher
* Optional: [`pytest`](https://pypi.org/project/pytest/) for running tests

## Usage

All commands use the main script `main.py`. Replace `test.idx` with your desired index file name.

| Command                                           | Description                                                                    |
| ------------------------------------------------- | ------------------------------------------------------------------------------ |
| `python main.py create <indexfile>`               | Create a new, empty B-Tree index file.                                         |
| `python main.py insert <indexfile> <key> <value>` | Insert a single key-value pair into the index.                                 |
| `python main.py search <indexfile> <key>`         | Search for a key and display its value (or "Not found").                       |
| `python main.py print <indexfile>`                | Print the B-Tree structure in a human-readable format for debugging.           |
| `python main.py load <indexfile> <csvfile>`       | Bulk load key-value pairs from a CSV (`key,value` per line) into the index.    |
| `python main.py extract <indexfile> <csvfile>`    | Export all key-value pairs in sorted order (in-order traversal) to a CSV file. |

### Examples

1. **Create a new index**

   ```bash
   python main.py create test.idx
   ```

2. **Insert a single entry**

   ```bash
   python main.py insert test.idx 15 100
   ```

3. **Search for a key**

   ```bash
   python main.py search test.idx 15
   # Output: (15, 100)
   ```

4. **Print tree structure**

   ```bash
   python main.py print test.idx
   ```

5. **Bulk load from CSV**

   ```bash
   python main.py load test.idx input.csv
   ```

6. **Extract to CSV**

   ```bash
   python main.py extract test.idx output.csv
   ```

## Running Tests

Automated tests are provided in the `tests/` directory using `pytest`.

```bash
pip install pytest          # if not already installed
pytest                      # runs all tests
```

## Project Structure

```
README.md              # This file
Project3/
├── btree.py               # B-Tree implementation
├── cache.py               # Node cache module
├── utils.py               # Utility functions (serialization, constants)
├── main.py                # CLI entry point
└── tests/
    └── test_btree.py     # Pytest test suite
```

## Contributing

Contributions are welcome! Feel free to:

* Open issues to report bugs or request features
* Submit pull requests with improvements or fixes

Please follow the existing code style and include tests for new functionality.
