from models.order_model import Order
from models.user_model import User
from dataclasses import asdict
from pathlib import Path
import json
from typing import Any, List, Union

# --- Centralized Configuration ---
BASE_DB_DIR = Path("DB_files")
USER_DB_PATH = BASE_DB_DIR / "user_DB.json"
ORDER_DB_PATH = BASE_DB_DIR / "order_DB.json"


def _load_json_db(filepath: Union[str, Path]) -> List[Any]:
    """Load data from a JSON database file safely.

    Returns an empty list if the file doesn't exist or contains invalid JSON.
    """
    path = Path(filepath)
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def _save_json_db(filepath: Union[str, Path], data: List[Any]) -> None:
    """Save data to a JSON database file, ensuring parent directories exist."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def user_exists(user_uid: str, filepath: Union[str, Path] = USER_DB_PATH) -> bool:
    """Check if a user with the specified UID exists in the JSON database.

    Args:
        user_uid (str): The unique identifier of the user to check.
        filepath (str | Path, optional): Path to the user database. Defaults to USER_DB_PATH.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    users = _load_json_db(filepath)
    return any(user.get("uid") == user_uid for user in users)


def save_order(order: Order, filepath: Union[str, Path] = ORDER_DB_PATH) -> None:
    """Save an Order dataclass instance to the JSON database file.

    Args:
        order (Order): The Order dataclass instance to save.
        filepath (str | Path, optional): Path to the order database. Defaults to ORDER_DB_PATH.
    """
    orders = _load_json_db(filepath)

    order_dict = {
        "name": order.name,
        "description": order.description,
        "duration": order.duration,
        "status": order.status.name,  # Saves as string ("OPEN", "IN_QUEUE", etc.)
        "user_uid": order.user_uid,
        "order_id": order.order_id,
    }

    orders.append(order_dict)
    _save_json_db(filepath, orders)


def save_user(user: User, filepath: Union[str, Path] = USER_DB_PATH) -> None:
    """Save a User dataclass instance to the JSON database file.

    Args:
        user (User): The User dataclass instance to save.
        filepath (str | Path, optional): Path to the user database. Defaults to USER_DB_PATH.
    """
    users = _load_json_db(filepath)
    users.append(asdict(user))
    _save_json_db(filepath, users)