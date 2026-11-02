from fastapi import APIRouter, HTTPException, status
from typing import Annotated
from fastapi import Depends
from ..schemas import OrderIn, OrderOut, OrderStatus
from ..repository_sql import SqlOrderRepository, get_repo

router = APIRouter(prefix="/orders", tags=["orders"])
Repo = Annotated[SqlOrderRepository, Depends(get_repo)]

@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def crear_orden(data: OrderIn, repo: Repo) -> OrderOut:
    return repo.add(data)

@router.get("", response_model=list[OrderOut])
def listar_ordenes(repo: Repo, estado: OrderStatus | None = None) -> list[OrderOut]:
    return repo.list(estado)

@router.get("/{order_id}", response_model=OrderOut)
def obtener_orden(order_id: int, repo: Repo) -> OrderOut:
    order = repo.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order

@router.put("/{order_id}", response_model=OrderOut)
def actualizar_orden(order_id: int, data: OrderIn, repo: Repo) -> OrderOut:
    order = repo.update(order_id, data)
    if order is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar_orden(order_id: int, repo: Repo):
    ok = repo.delete(order_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
