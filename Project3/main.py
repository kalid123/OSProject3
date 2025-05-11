import sys
import csv
from btree import BTree


def usage():
    print("Usage:")
    print("  project3 create <indexfile>")
    print("  project3 insert <indexfile> <key> <value>")
    print("  project3 search <indexfile> <key>")
    print("  project3 load <indexfile> <csvfile>")
    print("  project3 print <indexfile>")
    print("  project3 extract <indexfile> <csvfile>")
    sys.exit(1)


def main():
    if len(sys.argv) < 3:
        usage()
    cmd = sys.argv[1].lower()
    tree = BTree()
    try:
        if cmd == 'create':
            tree.create(sys.argv[2])
        else:
            idx = sys.argv[2]
            tree.open(idx)
            if cmd == 'insert':
                k, v = int(sys.argv[3]), int(sys.argv[4])
                tree.insert(k, v)
            elif cmd == 'search':
                res = tree.search(int(sys.argv[3]))
                print(res if res else "Not found")
            elif cmd == 'load':
                with open(sys.argv[3], newline='', encoding='utf-8-sig') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        # skip blank lines or headers
                        if len(row) < 2 or not row[0].strip().lstrip('-').isdigit():
                            continue
                        k = int(row[0].strip())
                        v = int(row[1].strip())
                        tree.insert(k, v)
            elif cmd == 'print':
                for k, v in tree.traverse_inorder():
                    print(k, v)
            elif cmd == 'extract':
                out = sys.argv[3]
                with open(out, 'x', newline='') as f:
                    for k, v in tree.traverse_inorder():
                        f.write(f"{k},{v}\n")
            else:
                usage()
    finally:
        tree.close()


if __name__ == '__main__':
    main()