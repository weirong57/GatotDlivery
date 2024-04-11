class PNode:
    # Initialize a node with a priority, order ID, left and right children set to None, and height set to 1.
    def __init__(self, priority, order_id):
        self.priority = priority
        self.order_id = order_id
        self.left = None
        self.right = None
        self.height = 1

class PriorityAVLTree:
    def __init__(self):
        # Initialize the AVL tree with the root node set to None.
        self.root = None

    def insert(self, priority, order_id):
        # Insert a new node into the AVL tree based on priority and order ID.
        self.root = self._insert(self.root, priority, order_id)

    def _insert(self, node, priority, order_id):
        # Recursive method to insert a node, ensuring the tree remains balanced.
        if not node:
            return PNode(priority, order_id)

        # Determine the position to insert the new node based on its priority and order ID.
        if priority < node.priority or (priority == node.priority and order_id < node.order_id):
            node.left = self._insert(node.left, priority, order_id)
        else:
            node.right = self._insert(node.right, priority, order_id)

        # Update the height of the current node and check the balance factor.
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._get_balance(node)

        # Perform rotations to maintain the AVL tree balance.
        # Left Left Case
        if balance > 1 and (priority < node.left.priority or (priority == node.left.priority and order_id < node.left.order_id)):
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and (priority > node.right.priority or (priority == node.right.priority and order_id > node.right.order_id)):
            return self._left_rotate(node)

        # Left Right Case
        if balance > 1 and (priority > node.left.priority or (priority == node.left.priority and order_id > node.left.order_id)):
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Left Case
        if balance < -1 and (priority < node.right.priority or (priority == node.right.priority and order_id < node.right.order_id)):
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def delete(self, priority, order_id):
        # Delete a node by priority and order ID from the AVL tree.
        self.root = self._delete(self.root, priority, order_id)

    def _delete(self, node, priority, order_id):
        # Recursive method to delete a node and maintain the AVL balance.
        if not node:
            return node

        # Navigate to the node to be deleted.
        if priority < node.priority or (priority == node.priority and order_id < node.order_id):
            node.left = self._delete(node.left, priority, order_id)
        elif priority > node.priority or (priority == node.priority and order_id > node.order_id):
            node.right = self._delete(node.right, priority, order_id)
        else:
            # Node found, perform deletion.
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self._min_value_node(node.right)
            node.priority = temp.priority
            node.order_id = temp.order_id
            node.right = self._delete(node.right, temp.priority, temp.order_id)

        if not node:
            return node

        # Update the height and rebalance the tree.
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._get_balance(node)

        # Perform rotations if necessary to maintain the tree balance.
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)

        # Left Right Case
        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        # Right Right Case
        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)

        # Right Left Case
        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _min_value_node(self, node):
        # Find the node with the minimum priority in the subtree.
        current = node
        while current.left:
            current = current.left
        return current

    def print_tree_structure(self):
        # Print the structure of the AVL tree.
        self._print_node_details(self.root)

    def _print_node_details(self, node):
        # Recursively print details of each node.
        if node:
            print(f"Node [Priority: {node.priority}, OrderId: {node.order_id}]")
            print("  Left Child:", end=" ")
            if node.left:
                print(f"[Priority: {node.left.priority}, OrderId: {node.left.order_id}]")
            else:
                print("null")
            print("  Right Child:", end=" ")
            if node.right:
                print(f"[Priority: {node.right.priority}, OrderId: {node.right.order_id}]")
            else:
                print("null")
            self._print_node_details(node.left)
            self._print_node_details(node.right)

    def get_order_ids(self):
        # Collect and return all order IDs in the tree.
        order_ids = []
        self._collect_order_ids(self.root, order_ids)
        return order_ids

    def _collect_order_ids(self, node, order_ids):
        # Recursively collect order IDs from the tree.
        if node:
            self._collect_order_ids(node.right, order_ids)
            order_ids.append(node.order_id)
            self._collect_order_ids(node.left, order_ids)

    def find_previous_higher_priority(self, target_priority, target_order_id):
        # Find the previous node with a higher priority than the target.
        last_visited_wrapper = [None]
        result_node = self._find_previous_node(self.root, target_priority, target_order_id, last_visited_wrapper)
        return result_node.order_id if result_node else -1

    def _find_previous_node(self, node, target_priority, target_order_id, last_visited_wrapper):
        # Recursive method to find the previous higher priority node.
        if not node:
            return None

        right_result = self._find_previous_node(node.right, target_priority, target_order_id, last_visited_wrapper)
        if right_result:
            return right_result

        if node.priority == target_priority and node.order_id == target_order_id:
            return last_visited_wrapper[0]

        last_visited_wrapper[0] = node
        return self._find_previous_node(node.left, target_priority, target_order_id, last_visited_wrapper)

    def find_first_node(self):
        # Find the node with the highest priority.
        return self._find_first_node(self.root)

    def _find_first_node(self, node):
        # Recursive method to find the node with the highest priority.
        if not node or not node.right:
            return node
        return self._find_first_node(node.right)

    def _height(self, node):
        # Get the height of a node.
        return node.height if node else 0

    def _get_balance(self, node):
        # Calculate the balance factor of a node.
        if not node:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _right_rotate(self, y):
        # Perform right rotation.
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        return x

    def _left_rotate(self, x):
        # Perform left rotation.
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

# Example usage:
if __name__ == "__main__":
    avl_tree = PriorityAVLTree()
    avl_tree.insert(1.0, 1)
    avl_tree.insert(2.0, 2)
    avl_tree.insert(3.0, 3)
    avl_tree.print_tree_structure()
    print(avl_tree.get_order_ids())
    avl_tree.delete(2.0, 2)
    avl_tree.print_tree_structure()
    print(avl_tree.find_previous_higher_priority(1.0, 1))
    print(avl_tree.find_first_node().order_id if avl_tree.find_first_node() else None)
