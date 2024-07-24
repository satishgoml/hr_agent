class TreeNode:
    def __init__(self, name, manager):
        self.name = name
        self.manager = manager
        self.children = []

def find_managers(root, department_name):
    # Helper function to find the node for the given department name
    def find_department_node(node, name):
        if node is None:
            return None
        if node.name == name:
            return node
        for child in node.children:
            found = find_department_node(child, name)
            if found:
                return found
        return None
    
    # Helper function to find the managers from the given node to the root
    def get_managers_to_root(node):
        managers = []
        while node is not None:
            managers.append(node.manager)
            node = parent_map.get(node, None)
        return managers

    # Create a map to store parent pointers
    parent_map = {}

    # Create a queue for BFS traversal and initialize with root
    queue = [root]
    while queue:
        current = queue.pop(0)
        for child in current.children:
            parent_map[child] = current
            queue.append(child)

    # Find the starting node for the given department name
    start_node = find_department_node(root, department_name)
    if start_node is None:
        return []

    # Get the managers from the start node to the root
    return get_managers_to_root(start_node)

# Example usage
# Create the tree structure
ceo = TreeNode("CEO", "Alice")
engineering = TreeNode("Engineering", "Bob")
sales = TreeNode("Sales", "Charlie")
backend = TreeNode("Backend", "David")
frontend = TreeNode("Frontend", "Eve")
domestic = TreeNode("Domestic", "Fay")

# Build the tree
ceo.children.extend([engineering, sales])
engineering.children.extend([backend, frontend])
sales.children.append(domestic)

# Test the function
print(find_managers(ceo, "Backend"))  # Output: ['David', 'Bob', 'Alice']
print(find_managers(ceo, "Sales"))    # Output: ['Charlie', 'Alice']
