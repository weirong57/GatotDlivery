class ENode:
# Initialize an ENode with the order ID, estimated time of arrival (ETA),
# left and right children set to None, and height set to 1.
    def __init__(self, order_id, eta):
        self.order_id = order_id
        self.eta = eta
        self.left = None
        self.right = None
        self.height = 1


class EtaAVLTree:
    def __init__(self):
        # Initialize the AVL tree with the root set to None
        self.root = None

    def insert(self, eta, order_id):
        # Public method to insert a new node into the AVL tree based on ETA and order ID.
        self.root = self._insert(self.root, eta, order_id)

    def _insert(self, node, eta, order_id):
        # Internal method to insert a new node into the tree. It does the actual
        # work of finding the correct location and maintaining the AVL balance.
        if node is None:
            return ENode(order_id, eta)

        if eta < node.eta:
            node.left = self._insert(node.left, eta, order_id)
        elif eta > node.eta:
            node.right = self._insert(node.right, eta, order_id)
        else:
            return node
        # Update the height and balance factor of the nodes.
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._get_balance(node)
        # Perform rotations to maintain the AVL tree balance.
        if balance > 1 and eta < node.left.eta:
            return self._right_rotate(node)

        if balance < -1 and eta > node.right.eta:
            return self._left_rotate(node)

        if balance > 1 and eta > node.left.eta:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1 and eta < node.right.eta:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _height(self, node):
        # Helper method to calculate the height of a node in the tree.
        if node is None:
            return 0
        return node.height

    def _get_balance(self, node):
        # Helper method to determine the balance factor of a node.
        if node is None:
            return 0
        return self._height(node.left) - self._height(node.right)

    def _right_rotate(self, y):
        # Perform right rotation around the given node to maintain AVL balance.
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2
        # Update heights after rotation.
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))

        return x

    def _left_rotate(self, x):
        # Perform left rotation around the given node to maintain AVL balance.
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2
        # Update heights after rotation.
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))

        return y

    def find_min_eta_node(self):
        # Find the node with the minimum ETA value.
        if self.root is None:
            return [0, 0]

        current = self.root
        while current.left is not None:
            current = current.left

        return [current.order_id, current.eta]

    def delete(self, eta):
        # Public method to delete a node based on ETA.
        self.root = self._delete(self.root, eta)

    def _delete(self, node, eta):
        # Internal method to delete a node from the tree while maintaining the AVL balance.
        if node is None:
            return node

        if eta < node.eta:
            node.left = self._delete(node.left, eta)
        elif eta > node.eta:
            node.right = self._delete(node.right, eta)
        else:
            if node.left is None or node.right is None:
                temp = node.left if node.left is not None else node.right

                if temp is None:
                    node = None
                else:
                    node = temp
            else:
                temp = self._min_value_node(node.right)
                node.eta = temp.eta
                node.order_id = temp.order_id
                node.right = self._delete(node.right, temp.eta)

        if node is None:
            return node
        # Update the height and balance of the node.
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._get_balance(node)
        # Perform rotations if necessary to maintain balance.
        if balance > 1 and self._get_balance(node.left) >= 0:
            return self._right_rotate(node)

        if balance > 1 and self._get_balance(node.left) < 0:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)

        if balance < -1 and self._get_balance(node.right) <= 0:
            return self._left_rotate(node)

        if balance < -1 and self._get_balance(node.right) > 0:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def _min_value_node(self, node):
        # Find the node with the minimum ETA value in a subtree.
        current = node
        while current.left is not None:
            current = current.left
        return current

    def print_orders_in_time_range(self, time1, time2):
        # Public method to get all orders within a specific ETA range.
        orders = []
        self._find_orders_in_time_range(self.root, time1, time2, orders)
        return orders

    def _find_orders_in_time_range(self, node, time1, time2, orders):
        # Internal method to recursively find orders in the specified ETA range.
        if node is None:
            return

        if time1 < node.eta:
            self._find_orders_in_time_range(node.left, time1, time2, orders)

        if time1 <= node.eta <= time2:
            orders.append(node.order_id)

        if time2 > node.eta:
            self._find_orders_in_time_range(node.right, time1, time2, orders)