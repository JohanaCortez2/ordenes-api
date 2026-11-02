from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from .db import get_session
from .models import OrderModel
from .schemas import OrderIn, OrderOut, OrderStatus

class SqlOrderRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, data: OrderIn) -> OrderOut:
        orden = OrderModel(**data.model_dump(), total=round(data.cantidad * data.precio_unitario, 2))
        self.session.add(orden)
        self.session.commit()
        self.session.refresh(orden)
        return OrderOut.model_validate(orden)

    def list(self, estado: OrderStatus | None = None) -> list[OrderOut]:
        consulta = select(OrderModel).order_by(OrderModel.id)
        if estado:
            consulta = consulta.where(OrderModel.status == estado.value)
        filas = self.session.scalars(consulta).all()
        return [OrderOut.model_validate(f) for f in filas]

    def get(self, order_id: int) -> OrderOut | None:
        orden = self.session.get(OrderModel, order_id)
        return OrderOut.model_validate(orden) if orden else None

    def update(self, order_id: int, data: OrderIn) -> OrderOut | None:
        orden = self.session.get(OrderModel, order_id)
        if not orden:
            return None
        for campo, valor in data.model_dump().items():
            setattr(orden, campo, valor)
        orden.total = round(data.cantidad * data.precio_unitario, 2)
        self.session.commit()
        self.session.refresh(orden)
        return OrderOut.model_validate(orden)

    def delete(self, order_id: int) -> bool:
        orden = self.session.get(OrderModel, order_id)
        if not orden:
            return False
        self.session.delete(orden)
        self.session.commit()
        return True

def get_repo(session: Annotated[Session, Depends(get_session)]) -> SqlOrderRepository:
    return SqlOrderRepository(session)