import os
from utils import BLOCK_SIZE, MAGIC, to_be8, from_be8
from cache import NodeCache

# B-Tree degree
t = 10
MAX_KEYS = 2 * t - 1
MAX_CHILDREN = 2 * t

class Header:
    def __init__(self, root_block=0, next_block_id=1):
        self.root_block = root_block
        self.next_block_id = next_block_id

    @classmethod
    def read(cls, f):
        f.seek(0)
        magic = f.read(8)
        if magic != MAGIC:
            raise ValueError("Invalid index file (magic mismatch)")
        root = from_be8(f.read(8))
        nxt = from_be8(f.read(8))
        return cls(root, nxt)

    def write(self, f):
        f.seek(0)
        f.write(MAGIC)
        f.write(to_be8(self.root_block))
        f.write(to_be8(self.next_block_id))
        f.write(b"\x00" * (BLOCK_SIZE - 24))
        f.flush()

class Node:
    def __init__(self, block_id, parent_id=0, file_handle=None):
        self.block_id = block_id
        self.parent_id = parent_id
        self.keys = []
        self.values = []
        self.children = []
        self._file = file_handle

    @classmethod
    def read(cls, f, block_id):
        f.seek(block_id * BLOCK_SIZE)
        buf = memoryview(f.read(BLOCK_SIZE))
        bid = from_be8(buf[0:8])
        pid = from_be8(buf[8:16])
        nkeys = from_be8(buf[16:24])
        node = cls(bid, pid, f)
        offset = 24
        for _ in range(MAX_KEYS):
            node.keys.append(from_be8(buf[offset:offset+8])); offset += 8
        for _ in range(MAX_KEYS):
            node.values.append(from_be8(buf[offset:offset+8])); offset += 8
        for _ in range(MAX_CHILDREN):
            node.children.append(from_be8(buf[offset:offset+8])); offset += 8
        node.keys = node.keys[:nkeys]
        node.values = node.values[:nkeys]
        node.children = [c for c in node.children[:nkeys+1] if c != 0]
        return node

    def write(self, f):
        f.seek(self.block_id * BLOCK_SIZE)
        parts = [
            to_be8(self.block_id),
            to_be8(self.parent_id),
            to_be8(len(self.keys))
        ]
        for i in range(MAX_KEYS):
            parts.append(to_be8(self.keys[i] if i < len(self.keys) else 0))
        for i in range(MAX_KEYS):
            parts.append(to_be8(self.values[i] if i < len(self.values) else 0))
        for i in range(MAX_CHILDREN):
            parts.append(to_be8(self.children[i] if i < len(self.children) else 0))
        data = b''.join(parts)
        padding = BLOCK_SIZE - len(data)
        f.write(data + b"\x00" * padding)
        f.flush()

class BTree:
    def __init__(self):
        self.f = None
        self.header = None
        self.cache = NodeCache()

    def create(self, path):
        if os.path.exists(path):
            raise FileExistsError(f"File '{path}' already exists")
        with open(path, 'wb') as f:
            Header().write(f)

    def open(self, path):
        from utils import validate_index_file
        validate_index_file(path)
        self.f = open(path, 'r+b')
        self.header = Header.read(self.f)

    def close(self):
        if self.f:
            self.cache.flush()
            self.f.close()
            self.f = None

    def get_node(self, block_id):
        return self.cache.get(block_id, lambda bid: Node.read(self.f, bid))

    def split_child(self, parent, i):
        t = 10
        child = self.get_node(parent.children[i])
        new_node = Node(self.header.next_block_id, parent.block_id, self.f)
        self.header.next_block_id += 1

        # Copy second half of keys/values to new node
        new_node.keys = child.keys[t:]
        new_node.values = child.values[t:]

        # Copy second half of children if not leaf
        if child.children:
            new_node.children = child.children[t:]
            child.children = child.children[:t]

        # Trim original child
        child.keys = child.keys[:t-1]
        child.values = child.values[:t-1]

        # Insert new node into parent
        parent.keys.insert(i, child.keys.pop())
        parent.values.insert(i, child.values.pop())
        parent.children.insert(i + 1, new_node.block_id)

        self.cache.mark_dirty(child)
        self.cache.mark_dirty(new_node)
        self.cache.mark_dirty(parent)

    def insert(self, k, v):
        if self.header.root_block == 0:
            root = Node(self.header.next_block_id, 0, self.f)
            self.header.next_block_id += 1
            root.keys = [k]
            root.values = [v]
            self.header.root_block = root.block_id
            self.cache.mark_dirty(root)
            self.header.write(self.f)
            return

        root = self.get_node(self.header.root_block)
        if len(root.keys) == MAX_KEYS:
            new_root = Node(self.header.next_block_id, 0, self.f)
            self.header.next_block_id += 1
            new_root.children = [root.block_id]
            root.parent_id = new_root.block_id
            self.header.root_block = new_root.block_id
            self.split_child(new_root, 0)
            self._insert_nonfull(new_root, k, v)
        else:
            self._insert_nonfull(root, k, v)
        self.header.write(self.f)

    def _insert_nonfull(self, node, k, v):
        i = len(node.keys) - 1

        if not node.children:
            node.keys.append(0)
            node.values.append(0)
            while i >= 0 and k < node.keys[i]:
                node.keys[i+1] = node.keys[i]
                node.values[i+1] = node.values[i]
                i -= 1
            node.keys[i+1] = k
            node.values[i+1] = v
            self.cache.mark_dirty(node)
        else:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            child = self.get_node(node.children[i])
            if len(child.keys) == MAX_KEYS:
                self.split_child(node, i)
                if k > node.keys[i]:
                    i += 1
                child = self.get_node(node.children[i])
            self._insert_nonfull(child, k, v)

    def search(self, k):
        def _search(node):
            i = 0
            while i < len(node.keys) and k > node.keys[i]:
                i += 1
            if i < len(node.keys) and k == node.keys[i]:
                return (node.keys[i], node.values[i])
            if not node.children:
                return None
            return _search(self.get_node(node.children[i]))

        if self.header.root_block == 0:
            return None
        return _search(self.get_node(self.header.root_block))

    def traverse_inorder(self):
        def _traverse(node):
            for i, key in enumerate(node.keys):
                if i < len(node.children) and node.children[i] != 0:
                    yield from _traverse(self.get_node(node.children[i]))
                yield (key, node.values[i])
            if len(node.keys) < len(node.children) and node.children[len(node.keys)] != 0:
                yield from _traverse(self.get_node(node.children[len(node.keys)]))

        if self.header.root_block != 0:
            yield from _traverse(self.get_node(self.header.root_block))
