import time

class OrderSystem:
    def __init__(self):
        self.orders = {}
        self.history_orders = []

    def record_history(self, order_id, old_status, new_status, create_at=None):
        if create_at is None:
            create_at = time.time()
        self.history_orders.append(
            {
                "id": order_id,
                "old_status": old_status,
                "new_status": new_status,
                "create_at": create_at,
            }
        )

    def create_order(self, order_id, customer, amount, create_at=None):
        if order_id in self.orders:
            raise ValueError("Pedido ja existe")
        if amount <= 0:
            raise ValueError("Valor invalido")
        self.orders[order_id] = {
            "id": order_id,
            "customer": customer,
            "amount": amount,
            "status": "pending",
        }
        self.record_history(order_id, None, "pending", create_at)

    def get_order(self, order_id):
        if order_id not in self.orders:
            raise ValueError(f"Pedido {order_id} não existe")
        return self.orders[order_id]

    def cancel_order(self, order_id, create_at=None):
        order = self.get_order(order_id)
        if order["status"] != "pending":
            raise ValueError(
                f"Apenas pedidos em 'pending' podem ser cancelados, status do pedido {order_id}: {order['status']}"
            )
        old_status = "pending"
        order["status"] = "cancelled"
        self.record_history(order_id, old_status, "cancelled", create_at)
        return True

    def complete_order(self, order_id, create_at=None):
        order = self.get_order(order_id)
        if order["status"] != "pending":
            raise ValueError(
                f"Apenas pedidos em 'pending' podem ser completados, status do pedido {order_id}: {order['status']}"
            )
        old_status = "pending"
        order["status"] = "completed"
        self.record_history(order_id, old_status, "completed", create_at)
        return True

    def reopen_order(self, order_id, create_at=None):
        order = self.get_order(order_id)
        if order["status"] == "cancelled":
            raise ValueError(
                f"Apenas pedidos completados podem ser reabertos, status do pedido {order_id}: {order['status']}"
            )
        old_status = "completed"
        order["status"] = "pending"
        self.record_history(order_id, old_status, "pending", create_at)
        return True

    def get_total_amount(self):
        return sum(order["amount"] for order in self.orders.values())

    def get_total_by_status(self, status):
        return sum(
            order["amount"]
            for order in self.orders.values()
            if order["status"] == status
        )

    def count_by_status(self):
        total_pending = 0
        total_completed = 0
        total_cancelled = 0
        for order in self.orders.values():
            if order["status"] == "pending":
                total_pending += 1
            elif order["status"] == "completed":
                total_completed += 1
            else:
                total_cancelled += 1
        return f"pending -> {total_pending}\ncompleted -> {total_completed}\ncancelled -> {total_cancelled}"

    def export_orders(self):
        for order in self.orders.values():
            print(
                f"{order['id']},{order['customer']},{order['amount']},{order['status']}"
            )

    def get_history(self, start=None, end=None):
        if start is None and end is None:
            return self.history_orders
        return [
            event for event in self.history_orders if start <= event["create_at"] <= end
        ]

    def get_total_by_customer(self, status=None):
        total = {}
        for order in self.orders.values():
            if status is None or order["status"] == status:
                customer = order["customer"]
                amount = order["amount"]
                total[customer] = total.get(customer, 0) + amount
        ordened = sorted(total.items(), key=lambda item: (-item[1], item[0]))
        return ordened

    def top_customers(self, n, status=None):
        ordened = self.get_total_by_customer(status)
        return [
            item[0] for item in ordened[:n]
            ]