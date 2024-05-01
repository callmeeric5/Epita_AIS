# PALISSON Antoine
## BST Search
def search_bst_iterative(tree, root_key, x):
    current_key = root_key

    while current_key:
        node = tree[current_key]

        if x == node['value']:
            return node
        elif x < node['value']:
            current_key = node['left']
        else:
            current_key = node['right']

    return

## BST Inorder Traversal
def inorder_traversal(tree, root_key):
    traversal = []
    stack = []
    current_key = root_key

    while current_key or stack:
        # this while loop is to go to the leftmost node
        while current_key:
            stack.append(current_key)
            current_key = tree[current_key]['left']
        # this part extracts the node and go to the right subtree
        current_key = stack.pop()
        traversal.append(tree[current_key]['value'])
        current_key = tree[current_key]['right']

    return traversal

def inorder_recursive(tree, node_key, traversal=None):
    if traversal is None:
        traversal = []

    if node_key:
        node = tree[node_key]
        inorder_recursive(tree, node['left'], traversal)
        traversal.append(node['value'])
        inorder_recursive(tree, node['right'], traversal)

    return traversal

## BST Preorder Traversal
def preorder_traversal(tree, root_key):
    traversal = []
    stack = [root_key]

    while stack:
        current_key = stack.pop()

        if current_key:
            node = tree[current_key]
            traversal.append(node['value'])
            # add right node then left node to stack
            # thus left will be visited first
            stack.append(node['right'])
            stack.append(node['left'])

    return traversal

def preorder_recursive(tree, node_key, traversal=None):
    if traversal is None:
        traversal = []

    if node_key:
        node = tree[node_key]
        traversal.append(node['value'])
        preorder_recursive(tree, node['left'], traversal)
        preorder_recursive(tree, node['right'], traversal)

    return traversal

## BST Postorder Traversal

def postorder_traversal(tree, root_key):
    stack = [root_key]
    traversal = []
    visited = set()

    while stack:
        current = stack[-1] # peek !
        node = tree[current]
        left_visited = node['left'] is None or node['left'] in visited
        right_visited = node['right'] is None or node['right'] in visited

        if left_visited or right_visited: # pop !
            visited.add(current)
            traversal.append(node['value'])
            stack.pop() 
        else: # push !
            if not right_visited: stack.append(node['right'])
            if not left_visited: stack.append(node['left'])

    return traversal

def postorder_recursive(tree, node_key, traversal=None):
    if traversal is None:
        traversal = []

    if node_key:
        node = tree[node_key]
        postorder_recursive(tree, node['left'], traversal)
        postorder_recursive(tree, node['right'], traversal)
        traversal.append(node['value'])

    return traversal

## BST Level-Order Traversal
def level_order_traversal(tree, root_key):
    traversal = []
    queue = [root_key]

    while queue:
        current_key = queue.pop(0)
        node = tree[current_key]
        traversal.append(node['value'])

        if node['left']:
            queue.append(node['left'])

        if node['right']:
            queue.append(node['right'])

    return traversal

## BST Node Addition
def node_addition(tree, current, new_value):
    current_key = 'root'

    while True:
        node = tree[current_key]

        if new_value < node['value']: side = "left"
        elif new_value > node['value']: side = "right"
        else : break # duplicates are not allowed in this implementation

        if node[side] is None:
            new_key = 'node' + str(len(tree))
            node[side] = new_key
            tree[new_key] = {'value': new_value, 'left': None, 'right': None}
            break
        else:
            current_key = node[side]

    return tree


## BST Node Removal
def min_value_node(tree, node):
        current = node
        while tree[current]['left'] is not None:
            current = tree[current]['left']
        return current

def node_removal(tree, root, x):
    node = search_bst_iterative(tree, root, x)
    
    # value not found
    if not node:
        print("Value not in key")
        return tree 
    
    node_name = list(node.keys())[0]

    # case 1 - no children
    if node['left'] is None and node['right'] is None:
        del tree[node_name]
        return tree

    # case 2 - one child
    elif node['left'] is None:
        child = node['right']
        tree[node_name] = tree[child]
        del tree[child]
        return tree
    elif node['right'] is None:
        child = node['left']
        tree[node_name] = tree[child]
        del tree[child]
        return tree

    # case 3 - two children
    else:
        successor = min_value_node(node['right'])
        node['value'] = tree[successor]['value']
        # Delete the successor
        for _, node in tree.items():
            if node['left'] == successor or node['right'] == successor:
                if node['left'] == successor:
                    node['left'] = None
                else:
                    node['right'] = None
                del tree[successor]
                break

    return tree

if __name__ == "__main__":

    tree = {'root' : {'value': 10, 'left': 'node1', 'right': 'node2'},
            'node1': {'value': 5, 'left': 'node3', 'right': 'node4'},
            'node2': {'value': 15, 'left': 'node5', 'right': 'node6'},
            'node3': {'value': 2, 'left': None, 'right': None},
            'node4': {'value': 8, 'left': None, 'right': None},
            'node5': {'value': 12, 'left': None, 'right': None},
            'node6': {'value': 20, 'left': None, 'right': None}}

    tree = node_addition(tree, 'root', 16)
    tree = node_removal(tree, 'root', 16) 
    print(f"inorder     : {inorder_traversal(tree, 'root')}")   
    print(f"preorder    : {preorder_traversal(tree, 'root')}")   
    print(f"postorder   : {postorder_traversal(tree, 'root')}")
    print(f"level-order : {level_order_traversal(tree, 'root')}")