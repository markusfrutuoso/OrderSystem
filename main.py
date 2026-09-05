from order_system import OrderSystem

system = OrderSystem()

system.create_order(1, "Markus", 200)
system.create_order(2, "Cindel", 300)
system.create_order(3, "Quindim", 500)

print(system.get_total_by_status("cancelled"))
print(system.count_by_status())
