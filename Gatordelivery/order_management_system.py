from PriorityAVLTree import PriorityAVLTree

from EtaAVLTree import EtaAVLTree
from order import Order


class OrderManagementSystem:
    def __init__(self):
        self.p_tree = PriorityAVLTree()
        self.order_map = {}
        self.e_tree = EtaAVLTree()
        self.order_has_delivered = set()
        self.earliest_available_time = 0

    def print_order(self, order_id):
        order = self.order_map.get(order_id)
        print(f"[{order.order_id}, {order.current_system_time}, {order.order_value}, {order.delivery_time}, {order.eta}]")

    def print_orders_in_time_range(self, time1, time2):
        orders = self.e_tree.print_orders_in_time_range(time1, time2)
        if not orders:
            print("There are no orders in that time period")
        else:
            print(orders)

    def get_rank_of_order(self, order_id):
        if order_id not in self.order_map:
            return
        order_ids = self.p_tree.get_order_ids()
        orders_before = 0
        for i, oid in enumerate(order_ids):
            if oid == order_id:
                orders_before = i
                break
        print(f"Order {order_id} will be delivered after {orders_before} orders")

    # def create_order(self, order_id, current_system_time, order_value, delivery_time):
    #     first_node = self.e_tree.find_min_eta_node()[0]
    #     first_eta = self.e_tree.find_min_eta_node()[1]
    #     if first_node != 0:
    #         if current_system_time >= first_eta and current_system_time < first_eta + self.order_map[first_node].delivery_time:
    #             first_p_node = self.p_tree.find_first_node()
    #             first_p_node.priority = float('inf')
    #             self.order_map[first_node].priority = float('inf')
    #         elif current_system_time < first_eta and current_system_time > first_eta - self.order_map[first_node].delivery_time:
    #             first_p_node = self.p_tree.find_first_node()
    #             first_p_node.priority = float('inf')
    #             self.order_map[first_node].priority = float('inf')
    #
    #     order = Order(order_id, current_system_time, order_value, delivery_time)
    #     self.p_tree.insert(order.priority, order_id)
    #     previous_higher_priority_order = self.p_tree.find_previous_higher_priority(order.priority, order_id)
    #
    #     if previous_higher_priority_order == 0:
    #         order.eta = order.current_system_time + order.delivery_time
    #     else:
    #         prev = self.order_map[previous_higher_priority_order]
    #         order.eta = prev.eta + prev.delivery_time + order.delivery_time
    #
    #     self.order_map[order_id] = order
    #     self.e_tree.insert(order.eta, order_id)
    #
    #     order_need_to_be_updated = []
    #     successor = self.p_tree.get_order_ids()
    #     start = 0
    #     for i, oid in enumerate(successor):
    #         if oid == order_id:
    #             start = i
    #             break
    #
    #     for i in range(start + 1, len(successor)):
    #         prev = self.order_map[successor[i - 1]]
    #         successor_order = self.order_map[successor[i]]
    #         og_eta = successor_order.eta
    #         new_eta = prev.eta + prev.delivery_time + successor_order.delivery_time
    #         if og_eta != new_eta:
    #             order_need_to_be_updated.append([successor[i], og_eta, new_eta])
    #             self.order_map[successor[i]].eta = new_eta
    #
    #     order_need_to_be_updated.sort(key=lambda x: x[2])
    #     for order_update in order_need_to_be_updated:
    #         self.e_tree.delete(order_update[1])
    #         self.e_tree.insert(order_update[2], order_update[0])
    #
    #     print(f"Order {order_id} has been created - ETA: {order.eta}")
    #
    #     if order_need_to_be_updated:
    #         updated_etas = "Updated ETAs: [" + ", ".join([f"{update[0]}:{update[2]}" for update in order_need_to_be_updated]) + "]"
    #         print(updated_etas)
    #
    #     self.check_delivered_orders(current_system_time)
    def create_order(self, order_id, current_system_time, order_value, delivery_time):
        first_node = self.e_tree.find_min_eta_node()[0]
        first_eta = self.e_tree.find_min_eta_node()[1]
        if first_node != 0:
            if current_system_time >= first_eta and current_system_time < first_eta + self.order_map[
                first_node].delivery_time:
                first_p_node = self.p_tree.find_first_node()
                first_p_node.priority = float('inf')
                self.order_map[first_node].priority = float('inf')
            elif current_system_time < first_eta and current_system_time > first_eta - self.order_map[
                first_node].delivery_time:
                first_p_node = self.p_tree.find_first_node()
                first_p_node.priority = float('inf')
                self.order_map[first_node].priority = float('inf')

        order = Order(order_id, current_system_time, order_value, delivery_time)
        self.p_tree.insert(order.priority, order_id)
        previous_higher_priority_order = self.p_tree.find_previous_higher_priority(order.priority, order_id)

        if previous_higher_priority_order >= 0:
            prev = self.order_map[previous_higher_priority_order]
            order.eta = prev.eta + prev.delivery_time + order.delivery_time
        else:
            order.eta = order.current_system_time + order.delivery_time

        self.order_map[order_id] = order
        self.e_tree.insert(order.eta, order_id)

        order_need_to_be_updated = []
        successor = self.p_tree.get_order_ids()
        start = 0
        for i, oid in enumerate(successor):
            if oid == order_id:
                start = i
                break

        for i in range(start + 1, len(successor)):
            prev = self.order_map[successor[i - 1]]
            successor_order = self.order_map[successor[i]]
            og_eta = successor_order.eta
            new_eta = prev.eta + prev.delivery_time + successor_order.delivery_time
            if og_eta != new_eta:
                order_need_to_be_updated.append([successor[i], og_eta, new_eta])
                self.order_map[successor[i]].eta = new_eta

        order_need_to_be_updated.sort(key=lambda x: x[2])
        for order_update in order_need_to_be_updated:
            self.e_tree.delete(order_update[1])
            self.e_tree.insert(order_update[2], order_update[0])

        print(f"Order {order_id} has been created - ETA: {order.eta}")

        if order_need_to_be_updated:
            updated_etas = "Updated ETAs: [" + ", ".join(
                [f"{update[0]}:{update[2]}" for update in order_need_to_be_updated]) + "]"
            print(updated_etas)

        self.check_delivered_orders(current_system_time)

    def cancel_order(self, order_id, current_system_time):
        self.check_delivered_orders(current_system_time)
        if order_id in self.order_has_delivered:
            print(f"Cannot cancel. Order {order_id} has already been delivered.")
        else:
            orders = self.p_tree.get_order_ids()
            start = 0
            for i, oid in enumerate(orders):
                if oid == order_id:
                    start = i
                    break

            order_need_to_be_removed = self.order_map[order_id]
            self.p_tree.delete(order_need_to_be_removed.priority, order_id)
            self.e_tree.delete(order_need_to_be_removed.eta)
            del self.order_map[order_id]
            print(f"Order {order_id} has been cancelled")

            order_need_to_be_updated = []
            orders = self.p_tree.get_order_ids()
            for i in range(start, len(orders)):
                prev = self.order_map[orders[i - 1]] if i - 1 >= 0 else None
                successor_order = self.order_map[orders[i]]
                og_eta = successor_order.eta
                new_eta = self.earliest_available_time + successor_order.delivery_time if prev is None else prev.eta + prev.delivery_time + successor_order.delivery_time
                if og_eta != new_eta:
                    order_need_to_be_updated.append([orders[i], og_eta, new_eta])
                    self.order_map[orders[i]].eta = new_eta

            order_need_to_be_updated.sort(key=lambda x: x[2])
            for order_update in order_need_to_be_updated:
                self.e_tree.delete(order_update[1])
                self.e_tree.insert(order_update[2], order_update[0])

            if order_need_to_be_updated:
                updated_etas = "Updated ETAs: [" + ", ".join([f"{update[0]}:{update[2]}" for update in order_need_to_be_updated]) + "]"
                print(updated_etas)

    def check_delivered_orders(self, current_system_time):
        while self.e_tree.find_min_eta_node()[1] != 0 and self.e_tree.find_min_eta_node()[1] <= current_system_time:
            order_id = self.e_tree.find_min_eta_node()[0]
            order_need_to_be_removed = self.order_map.get(order_id)
            if order_need_to_be_removed is None:
                continue
            self.order_has_delivered.add(order_id)
            self.p_tree.delete(order_need_to_be_removed.priority, order_id)
            self.e_tree.delete(order_need_to_be_removed.eta)
            del self.order_map[order_id]
            self.earliest_available_time = order_need_to_be_removed.eta + order_need_to_be_removed.delivery_time
            print(f"Order {order_id} has been delivered at time {order_need_to_be_removed.eta}")

    def update_time(self, order_id, current_system_time, new_delivery_time):
        self.check_delivered_orders(current_system_time)
        if order_id in self.order_has_delivered:
            print(f"Cannot update. Order {order_id} has already been delivered.")
            return

        order = self.order_map[order_id]
        old_eta = order.eta
        updated_eta = old_eta - order.delivery_time + new_delivery_time
        order.eta = updated_eta
        order.delivery_time = new_delivery_time
        self.e_tree.delete(old_eta)
        self.e_tree.insert(updated_eta, order_id)
        self.order_map[order_id] = order

        order_need_to_be_updated = [[order_id, old_eta, updated_eta]]
        successor = self.p_tree.get_order_ids()
        start = 0
        for i, oid in enumerate(successor):
            if oid == order_id:
                start = i
                break

        for i in range(start + 1, len(successor)):
            prev = self.order_map[successor[i - 1]]
            successor_order = self.order_map[successor[i]]
            og_eta = successor_order.eta
            new_eta = self.earliest_available_time + successor_order.delivery_time if prev is None else prev.eta + prev.delivery_time + successor_order.delivery_time
            if og_eta != new_eta:
                order_need_to_be_updated.append([successor[i], og_eta, new_eta])
                self.order_map[successor[i]].eta = new_eta

        order_need_to_be_updated.sort(key=lambda x: x[2])
        for order_update in order_need_to_be_updated:
            self.e_tree.delete(order_update[1])
            self.e_tree.insert(order_update[2], order_update[0])

        if order_need_to_be_updated:
            updated_etas = "Updated ETAs: [" + ", ".join([f"{update[0]}:{update[2]}" for update in order_need_to_be_updated]) + "]"
            print(updated_etas)

    def quit(self):
        self.check_delivered_orders(99999)
