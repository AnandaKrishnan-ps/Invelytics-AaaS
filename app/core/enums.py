from enum import Enum


class InventoryChangeCategory(str, Enum):
    RESTOCK = "RESTOCK"
    SALES = "SALES"
