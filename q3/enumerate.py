import sys
class Node:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

class Binary_tree:
    def __init__(self, left_subtree=None, right_subtree=None):
        self.root = Node(left=left_subtree, right=right_subtree)
        return
    def preorder_traverse(self):
        return self._preorder_traverse_aux(self.root)
    def _preorder_traverse_aux(self, current):
        if current.left is None and current.right is None:
            return '1'
        return '0' + self._preorder_traverse_aux(current.left) + self._preorder_traverse_aux(current.right)
def flatten_list(lst):
    result = []
    for sublist in lst:
        for item in sublist:
            result.append(item)
    return result
def get_trees_in_level(n):
    if n == 0:
        return [Binary_tree()]
    else:
        trees = []
        level_pairs = list(zip(reversed(range(n)), range(n)))
        tree_list = map(lambda x : (get_trees_in_level(x[0]), get_trees_in_level(x[1])), level_pairs)
        for tp in tree_list:
            for lt in tp[0]:
                for rt in tp[1]:
                    trees.append(Binary_tree(left_subtree=lt.root, right_subtree=rt.root))
        trees = sorted(trees, key=lambda x : int(x.preorder_traverse(), 2))
        return trees

def get_trees_to_level(n):
    trees = []
    for i in range(n+1):
        trees.extend(get_trees_in_level(i))
    return trees

def write_trees_to_file(trees, filepath='./output_enumerate.txt'):
    with open(filepath, 'w') as f:
        for i, t in enumerate(trees, 1):
            f.writelines(str(i) + '\t' + t.preorder_traverse()+'\n')

if __name__ == "__main__":
    to_level = int(sys.argv[1]) 
    write_trees_to_file(get_trees_to_level(to_level))
    
