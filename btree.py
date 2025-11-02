'''
Tree implementation, if u wanna understand more what is happening here I recommend this video from Tony Saro

https://www.youtube.com/watch?v=CWI6sDEdBLM

gl bro
'''

class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t # at most (2 * t) - 1 keys
        self.leaf = leaf # true if has no children
        self.keys = []
        self.values = []
        self.children = []

class BTree:
    def __init__(self, t=2):
        self.root = BTreeNode(t, True)
    
    def search(self, node, key):
        '''
        The loop finds which child index i could contain the key.
        1. If the key is in this node we return node.values[i]
        2. If it's a leaf we return None (since there is no more children to keep looking for)
        3. Otherwise we must search the child where the key would be
        '''
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        if node.leaf:
            return None
        return self.search(node.children[i], key)

    def insert(self, key, value):
        '''
        If root is full create a new root, make old root its child, split that child, then insert into the now non-full tree.
        Otherwise call insert_non_full on the root.
        '''
        root = self.root
        if len(root.keys) == (2 * root.t - 1):
            new_root = BTreeNode(root.t, False)
            new_root.children.insert(0, root)
            self.split_child(new_root, 0)
            self.root = new_root
            self.insert_non_full(new_root, key, value)
        else:
            self.insert_non_full(root, key, value)
    
    def insert_non_full(self, node, key, value):
        '''
        Insert key/value into a node that is not full.

        1. If node is a leaf, insert key/value into the correct sorted position.
        2. If node is internal, choose the child to descend to, if that child is full, split it first, then recurse.

        tf is this shi bruh but ok
        '''
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            node.values.append(None)
            while i >= 0 and key < node.keys[i]: # shift existing keys, values to make room
                node.keys[i + 1] = node.keys[i]
                node.values[i + 1] = node.values[i]
                i -= 1
            # insertion in correct position
            node.keys[i + 1] = key
            node.values[i + 1] = value
        else:
            # internal node, find child to descend into
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            # If the target child is full, split it so we never recurse into a full node
            if len(node.children[i].keys) == (2 * node.t - 1):
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            # Recurse into the appropriate child (guaranteed non-full)
            self.insert_non_full(node.children[i], key, value)
    
    def split_child(self, parent, i):
        '''
        Split parent.children[i] (full node with 2*t-1 keys) into two nodes.
        - left keeps first t-1 keys (y)
        - right gets last t-1 keys (z)
        - median key at index t-1 is promoted into parent at position i

        I guess bro
        '''
        t = parent.children[i].t
        y = parent.children[i]
        z = BTreeNode(t, y.leaf)

        # create right sibling and promote median key/value into parent
        parent.children.insert(i + 1, z)
        parent.keys.insert(i, y.keys[t - 1])
        parent.values.insert(i, y.values[t - 1])

        # move right-half keys/values to z
        z.keys = y.keys[t:(2 * t - 1)]
        z.values = y.values[t:(2 * t - 1)]
        # keep left-half keys/values in y
        y.keys = y.keys[0:t - 1]
        y.values = y.values[0:t - 1]
        
        # if internal node, move the corresponding child pointers to z and keep left ones in y
        if not y.leaf:
            z.children = y.children[t:(2 * t)]
            y.children = y.children[0:t]