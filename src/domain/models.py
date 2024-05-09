from dataclass import dataclass
from typings import Optional

@dataclass(froze=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int

class Batch:

    def __init__(
        self, ref: str, sku:str, qty:int, eta: Optional[date]
    )

    self.referance = ref
    self.sku = sku
    self.eta = eta
    self.available_quantity = qty

    def allocate(self, line: OrderLine):
        self.available_quantity -= line.qty