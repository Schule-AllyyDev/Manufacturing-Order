if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from Business_logic.order_logic import Order_logic
from Business_logic.user_logic import User_logic
from Helpers.scanner import process_queue
from models.order_model import Order, Status


def _show_users() -> None:
    users = User_logic.get_all_users()
    if not users:
        print("No users found.")
        return
    for user in users:
        print(f"{user.name} | UID: {user.uid}")


def _show_orders(orders: list[Order]) -> None:
    if not orders:
        print("No orders found.")
        return
    for order in orders:
        print(
            f"{order.name} | ID: {order.order_id} | User: {order.user_uid} | "
            f"{order.duration}s | {order.status.name}"
        )


def _create_order() -> None:
    users = User_logic.get_all_users()
    if not users:
        print("Create a user before creating an order.")
        return
    _show_users()
    Order_logic.add_order()


def _queue_order() -> None:
    open_orders = Order_logic.get_orders_by_status(Status.OPEN)
    if not open_orders:
        print("There are no open orders to queue.")
        return
    _show_orders(open_orders)
    order_id = input("Order ID to add to the scanner queue: ").strip()
    if Order_logic.queue_order(order_id):
        print("Order added to the scanner queue.")
    else:
        print("Order could not be queued. Check its ID, status, and duration.")


def run_menu() -> None:
    actions = {
        "1": ("Create user", User_logic.add_user),
        "2": ("List users", _show_users),
        "3": ("Delete user", lambda: User_logic.delete_user(input("User UID: ").strip())),
        "4": ("Create order", _create_order),
        "5": ("List orders", lambda: _show_orders(Order_logic.get_all_orders())),
        "6": ("Queue an open order", _queue_order),
        "7": (
            "View scanner queue",
            lambda: _show_orders(Order_logic.get_orders_by_status(Status.IN_QUEUE)),
        ),
        "8": ("Run scanner queue", process_queue),
    }

    while True:
        print(
            "\n=== Manufacturing Order Menu ===\n"
            "1. Create user\n"
            "2. List users\n"
            "3. Delete user and their orders\n"
            "4. Create order (maximum 120 seconds)\n"
            "5. List orders\n"
            "6. Queue an open order\n"
            "7. View scanner queue\n"
            "8. Run scanner (maximum 5 minutes)\n"
            "0. Exit"
        )
        choice = input("Select an option: ").strip()
        if choice == "0":
            return
        action = actions.get(choice)
        if action is None:
            print("Invalid option. Choose a number from 0 to 8.")
            continue
        try:
            action[1]()
        except (EOFError, KeyboardInterrupt):
            print("\nReturning to menu.")


if __name__ == "__main__":
    run_menu()