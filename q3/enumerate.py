import sys
def node_generator():
    while True:
        yield Node()
class Node:
    def __init__(self):
        self.left = None 
        self.right = None
        self.active = False
    def get_left(self):
        if self.left is None:
            self.left = Node()
        return self.left
    def get_right(self):
        if self.right is None:
            self.right = Node()
        return self.right


def flatten_list(lst):
    result = []
    for i in lst:
        if type(i) is list:
            for j in i:
                result.append(j)
        else:
            result.append(i)
    return result

class Tree:
    def __init__(self):
        self.root = Node()
        return 
    def enum_level(self, N):
        self.ans = []
        if N == 0:
            self.ans.append('1')
        else:
            # N-=1
            # self.last_activated = None
            self.__init__()
            self.activated_num = 0
            # self.current_depth = 0
            self.start_enum = False

            self.last_activation_gen = iter(self.postorder_traverse(self.root, 1, N))
            self.enum_internal(self.root, N , 1)
        return self.ans
    # def postorder_traverse(self, current, current_depth, N):
    #     # print(current_depth)
    #     if current_depth == N:
    #         yield current
    #         return
    #     self.postorder_traverse(current.get_left(), current_depth+1, N)
    #     self.postorder_traverse(current.get_right(), current_depth+1, N)
    #     yield current
    def postorder_traverse(self, current, current_depth, N):
        # print(current_depth)
        if current_depth == N:
            return [current]
        left = self.postorder_traverse(current.get_left(), current_depth+1, N)
        right = self.postorder_traverse(current.get_right(), current_depth+1, N)
        return flatten_list([left, right, current])

    # def postorder_traverse(self, N):
    #     current = self.root
    #     depth = 1
    #     while depth < N:
    #         current = current.get_left()
    #         depth += 1
    #     yield current

    # def _postorder_aux()
    def enum_internal(self, current, N, current_depth):
        # if len(node_path) == N:
        #     print(node_path)
        #     return 
        # print(activated_num)
        
        if self.activated_num == N-1:
            if not self.start_enum:
                current.active = True
                # self.last_activated = current
                self.start_enum = True
                self.ans.append(self.traverse_activation(self.root))
                print(self.traverse_activation(self.root))
                return 
            else:
                # self.last_activated.active = False
                last_activation = next(self.last_activation_gen)
                last_activation.active = False
                current.active = True
                # self.last_activated = current
                self.ans.append(self.traverse_activation(self.root))
                print(self.traverse_activation(self.root))
                if current_depth == N:
                    return 
                else:
                    self.enum_internal(current.get_left(), N, current_depth+1)
                    self.enum_internal(current.get_right(), N, current_depth+1)
                    return
        current.active = True
        # self.last_activated = current
        self.activated_num+=1
        self.enum_internal(current.get_left(), N, current_depth+1)
        self.enum_internal(current.get_right(), N, current_depth+1)
        return 
    def traverse_activation(self, current):
        if not current.active:
            return '1'
        return '0' + self.traverse_activation(current.get_left()) + self.traverse_activation(current.get_right())
def factorial(N):
    if N == 0:
        return 1
    return factorial(N-1)*N
def get_tree_num(N):
    return int(factorial(2*N)/(factorial(N+1)*factorial(N)))
if __name__ == "__main__":
    # assert len(sys.argv) == 2
    # N = sys.argv[1]
    N = 4
    bitree = Tree()
    ans = [] 
    for i in range(N+1):
        ans.append(bitree.enum_level(i))
    ans = flatten_list(ans)
    with open('output_enumerate.txt', 'w') as f:
        for i in range(len(ans)):
            f.write(str(i+1) + '\t' + ans[i] + '\n')

