from enum import Enum


class InventoryChangeCategory(str, Enum):
    RESTOCK = "RESTOCK"
    SALES = "SALES"

class UpdatedByCategory(str, Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"
