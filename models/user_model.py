from dataclasses import dataclass
from models.order_model import Order

@dataclass
class User:
    name: str
    uid: str
    # Additional attributes can be added here, such as email, password, etc.
