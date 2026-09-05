class OrderSystem:
    def __init__(self):
        self.orders = {}

    def create_order(self, order_id, customer, amount):
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

    def get_order(self, order_id):
        if order_id not in self.orders:
            raise ValueError(f"Pedido {order_id} não existe")
        return self.orders[order_id]

    def cancel_order(self, order_id):
        order = self.get_order(order_id)
        if order["status"] != "pending":
            raise ValueError(
                f"Apenas pedidos em 'pending' podem ser cancelados, status do pedido {order_id}: {order['status']}"
            )
        order["status"] = "cancelled"
        return True

    def complete_order(self, order_id):
        order = self.get_order(order_id)
        if order["status"] != "pending":
            raise ValueError(
                f"Apenas pedidos em 'pending' podem ser completados, status do pedido {order_id}: {order['status']}"
            )
        order["status"] = "completed"
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
