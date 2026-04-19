from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base  # <--- ESTA ES LA LÍNEA QUE FALTA

class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    concepto = Column(String(100))
    monto = Column(Float)
    tipo = Column(String(50)) # 'gasto', 'ingreso', 'prestamo'
    
    # NUEVO CAMPO: Para clasificar en el sistema 50/30/20
    # Opciones sugeridas: 'necesidad', 'deseo', 'ahorro_deuda'
    categoria_maestra = Column(String(50), default="necesidad") 
    
    automatico = Column(Boolean, default=False)
    dia_pago = Column(Integer, nullable=True)
    cuotas_totales = Column(Integer, default=1)
    cuota_actual = Column(Integer, default=0)