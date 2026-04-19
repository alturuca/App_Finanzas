from pydantic import BaseModel
from typing import Optional

# La base de lo que comparten todos los movimientos
class MovimientoBase(BaseModel):
    concepto: str
    monto: float
    tipo: str # 'ahorro', 'gasto', 'prestamo'
    categoria_maestra: Optional[str] = "necesidad"

# Lo que el usuario nos envía cuando CREA algo nuevo
class MovimientoCreate(MovimientoBase):
    automatico: Optional[bool] = False
    dia_pago: Optional[int] = None
    cuotas_totales: Optional[int] = 1

# Lo que la API devuelve (incluye el ID que genera la base de datos)
class MovimientoResponse(MovimientoBase):
    id: int
    cuota_actual: int
    
    class Config:
        from_attributes = True # Esto permite que Pydantic lea modelos de SQLAlchemy