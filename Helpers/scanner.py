from collections import deque
from time import monotonic, sleep

from Business_logic.order_logic import MAX_ORDER_DURATION_SECONDS, Order_logic
from models.order_model import Order, Status

MAX_SCANNER_DURATION_SECONDS = 5 * 60


def process_queue() -> list[Order]:
    """Print queued orders sequentially for up to five minutes per scan run."""
    queue = deque(Order_logic.get_orders_by_status(Status.IN_QUEUE))
    completed: list[Order] = []
    started_at = monotonic()

    while queue:
        order = queue[0]
        if order.duration <= 0 or order.duration > MAX_ORDER_DURATION_SECONDS:
            raise ValueError(
                f"Order {order.order_id} has an invalid duration of {order.duration} seconds."
            )

        elapsed = monotonic() - started_at
        if elapsed + order.duration > MAX_SCANNER_DURATION_SECONDS:
            print("Scanner's five-minute test limit reached; remaining orders stay queued.")
            break

        queue.popleft()
        print(f"Printing {order.name} ({order.duration} seconds)...")
        sleep(order.duration)

        if not Order_logic.update_order_status(order.order_id, Status.DONE):
            raise RuntimeError(f"Could not mark order {order.order_id} as complete.")
        completed.append(order)
        print(f"Completed order {order.order_id}.")

    if not completed and not queue:
        print("Scanner queue is empty.")
    return completed
