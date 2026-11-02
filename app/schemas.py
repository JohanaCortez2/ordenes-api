from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class OrderStatus(str, Enum):
    pendiente = "pendiente"
    pagada = "pagada"
    enviada = "enviada"
    cancelada = "cancelada"

class OrderIn(BaseModel):
    cliente: str = Field(min_length=1, max_length=80)
    producto: str = Field(min_length=1, max_length=120)
    cantidad: int = Field(gt=0)
    precio_unitario: float = Field(gt=0)

class OrderOut(OrderIn):
    id: int
    total: float
    status: OrderStatus = OrderStatus.pendiente
    creada: datetime

    model_config = ConfigDict(from_attributes=True)