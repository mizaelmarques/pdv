from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Dict


@dataclass
class Order:
    id: int
    number: int
    created_at: datetime
    total: Decimal
    is_finalized: bool
    items: Dict[int, int]  # product_id -> quantity
