from models.order_model import Order, Status
from Helpers import import_data
import uuid


MAX_ORDER_DURATION_SECONDS = 120


class Order_logic:
    def add_order() -> bool:
        print("============ CREATE ORDER ============")
        try: 
            name = input("Name: ")
            description = input("Description: ")
            duration = int(input("Duration: "))
            user_uid = input("User UID: ")
            order_id = str(uuid.uuid4().hex)

            if not name.strip() or not description.strip():
                print("Name and description are required.")
                return False
            if duration <= 0 or duration > MAX_ORDER_DURATION_SECONDS:
                print(f"Duration must be between 1 and {MAX_ORDER_DURATION_SECONDS} seconds.")
                return False
            if not import_data.user_exists(user_uid):
                print(f"User with UID {user_uid} does not exist.")
                return False

            import_data.save_order(
                Order(name.strip(), description.strip(), duration, Status.OPEN, user_uid, order_id)
            )
        except ValueError as e:
            print("Invalid input. Error: ", e)
            return False

        return True

    @staticmethod
    def _orders_from_db() -> list[Order]:
        orders = import_data._load_json_db(import_data.ORDER_DB_PATH)
        return [
            Order(
                name=o.get("name", ""),
                description=o.get("description", ""),
                duration=o.get("duration", 0),
                status=Status[o.get("status", "OPEN")],
                user_uid=o.get("user_uid", ""),
                order_id=o.get("order_id", ""),
            )
            for o in orders
        ]

    def get_orders_by_user(user_uid: str) -> list[Order]:
        """Retrieve all orders associated with a specific user UID."""
        return [order for order in Order_logic._orders_from_db() if order.user_uid == user_uid]

    def update_order_status(order_id: str, new_status: Status) -> bool:
        """Update the status of a specific order by its order_id."""
        orders = import_data._load_json_db(import_data.ORDER_DB_PATH)
        updated = False
        status_str = new_status.name if hasattr(new_status, "name") else str(new_status)
        
        for o in orders:
            if o.get("order_id") == order_id:
                o["status"] = status_str
                updated = True
                break
                
        if updated:
            import_data._save_json_db(import_data.ORDER_DB_PATH, orders)
            return True
        return False

    def get_orders_by_status(status: Status) -> list[Order]:
        """Retrieve all orders matching a specific status."""
        return [order for order in Order_logic._orders_from_db() if order.status == status]

    def queue_order(order_id: str) -> bool:
        """Move an open order to the scanner's persisted FIFO queue."""
        order = next(
            (item for item in Order_logic._orders_from_db() if item.order_id == order_id),
            None,
        )
        if order is None or order.status is not Status.OPEN:
            return False
        if order.duration <= 0 or order.duration > MAX_ORDER_DURATION_SECONDS:
            return False
        return Order_logic.update_order_status(order_id, Status.IN_QUEUE)

    def get_all_orders() -> list[Order]:
        """Retrieve all orders from the database."""
        return Order_logic._orders_from_db()