class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.values = []
        self.children = []
class BTree:
    def __init__(self, t=2):
        self.root = BTreeNode(t, True)
    
    def search():
        return 0
    
    def insert():
        return 0
    
    def insert_non_full():
        return 0
    
    def split_child():
        return 0