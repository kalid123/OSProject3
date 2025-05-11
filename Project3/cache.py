from collections import OrderedDict

class NodeCache:
    def __init__(self, limit=3):
        self.limit = limit
        self.cache = OrderedDict()  # block_id -> (node, dirty)

    def get(self, block_id, loader):
        if block_id in self.cache:
            node, dirty = self.cache.pop(block_id)
            self.cache[block_id] = (node, dirty)
            return node
        node = loader(block_id)
        self.cache[block_id] = (node, False)
        if len(self.cache) > self.limit:
            old_id, (old_node, was_dirty) = self.cache.popitem(last=False)
            if was_dirty:
                old_node.write(old_node._file)
        return node

    def mark_dirty(self, node):
        bid = node.block_id
        if bid in self.cache:
            _, _ = self.cache.pop(bid)
        self.cache[bid] = (node, True)

    def flush(self):
        for node, dirty in self.cache.values():
            if dirty:
                node.write(node._file)
        self.cache.clear()