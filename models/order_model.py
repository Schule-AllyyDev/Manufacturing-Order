from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    OPEN = 1
    IN_QUEUE = 2
    DONE = 3
    ON_HOLD = 4


@dataclass
class Order:
    name: str
    description: str
    duration: int
    status: Status
    user_uid: str
    order_id: str = ""