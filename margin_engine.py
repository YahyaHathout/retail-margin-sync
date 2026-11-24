```python
import json
from dataclasses import dataclass
from typing import List


@dataclass
class MenuItem:
    sku: str
    name_ar: str
    name_en: str
    direct_cost: float
    selling_price: float
    min_margin_pct: float = 50.0

    @property
    def gross_margin_pct(self) -> float:
        if self.selling_price <= 0:
            return 0.0
        return round(((self.selling_price - self.direct_cost) / self.selling_price) * 100, 2)

    def is_compliant(self) -> bool:
        return self.gross_margin_pct >= self.min_margin_pct

    def suggested_price(self) -> float:
        factor = 1 - (self.min_margin_pct / 100)
        return round(self.direct_cost / factor, 2)


class BranchSyncManager:
    def __init__(self, branch_names: List[str]):
        self.branch_names = branch_names
        self.catalog: List[MenuItem] = []

    def add_item(self, item: MenuItem) -> dict:
        self.catalog.append(item)
        status = "APPROVED" if item.is_compliant() else "MARGIN_WARNING"
        return {
            "sku": item.sku,
            "status": status,
            "current_margin": f"{item.gross_margin_pct}%",
            "recommended_price": item.suggested_price() if not item.is_compliant() else item.selling_price,
            "synced_branches": self.branch_names,
        }


if __name__ == "__main__":
    manager = BranchSyncManager(["Main Branch", "Stadium Branch", "City Club"])
    sample_item = MenuItem(
        sku="ITEM-101",
        name_ar="لاتيه كلاسيك",
        name_en="Classic Latte",
        direct_cost=22.0,
        selling_price=50.0,
    )
    print(json.dumps(manager.add_item(sample_item), ensure_ascii=False, indent=2))