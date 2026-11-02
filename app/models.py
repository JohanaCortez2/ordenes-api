from datetime import datetime, timezone
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class OrderModel(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    cliente: Mapped[str] = mapped_column(String(80))
    producto: Mapped[str] = mapped_column(String(120))
    cantidad: Mapped[int] = mapped_column()
    precio_unitario: Mapped[float] = mapped_column()
    total: Mapped[float] = mapped_column()
    status: Mapped[str] = mapped_column(String(20), default="pendiente")
    creada: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))