
from btree import BTree
import csv
def test_create_and_basic_insert_search(tmp_path):
    idx = tmp_path / 'test.idx'
    bt = BTree()
    bt.create(str(idx))
    bt.open(str(idx))
    assert bt.search(1) is None
    bt.insert(1, 100)
    bt.insert(2, 200)
    res = bt.search(2)
    assert res == (2, 200)
    out = list(bt.traverse_inorder())
    assert out == [(1, 100), (2, 200)]
    bt.close()


def test_load_and_extract(tmp_path):
    idx = tmp_path / 'test2.idx'
    csv_in = tmp_path / 'in.csv'
    csv_out = tmp_path / 'out.csv'
    data = [(5,50),(3,30),(7,70)]
    with open(csv_in, 'w') as f:
        for k,v in data:
            f.write(f"{k},{v}\n")
    bt = BTree()
    bt.create(str(idx))
    bt.open(str(idx))
    with open(str(csv_in)) as f:
        for r in csv.reader(f):
            bt.insert(int(r[0]), int(r[1]))
    with open(str(csv_out), 'x') as f:
        for k,v in bt.traverse_inorder():
            f.write(f"{k},{v}\n")
    bt.close()
    lines = open(csv_out).read().strip().split('\n')
    assert lines == ["3,30","5,50","7,70"]