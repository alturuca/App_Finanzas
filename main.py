
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
import models, database, schemas

app = FastAPI(title="Finanzas Antigravity")

# Creamos las tablas al iniciar (por seguridad)
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def home():
    return {"vuelo": "Exitoso", "mensaje": "Listo para registrar finanzas"}

# --- RUTAS DE MOVIMIENTOS ---

@app.post("/movimientos/", response_model=schemas.MovimientoResponse)
def crear_movimiento(mov: schemas.MovimientoCreate, db: Session = Depends(database.get_db)):
    # Convertimos el esquema de Pydantic a un modelo de SQLAlchemy
    nuevo_movimiento = models.Movimiento(**mov.model_dump())
    
    db.add(nuevo_movimiento)
    db.commit()
    db.refresh(nuevo_movimiento)
    return nuevo_movimiento

@app.get("/movimientos/", response_model=list[schemas.MovimientoResponse])
def listar_movimientos(db: Session = Depends(database.get_db)):
    return db.query(models.Movimiento).all()

@app.get("/reporte/presupuesto")
def obtener_reporte_presupuesto(db: Session = Depends(database.get_db)):
    movimientos = db.query(models.Movimiento).all()
    
    totales = {"necesidad": 0, "deseo": 0, "ahorro_deuda": 0, "sin_clasificar": 0}
    
    # 1. Sumamos los montos
    monto_total = 0
    for m in movimientos:
        cat = str(m.categoria_maestra).lower().strip() if m.categoria_maestra else "sin_clasificar"
        if cat == "necesidades": cat = "necesidad"
        elif cat == "deseos": cat = "deseo"
            
        if cat in totales:
            totales[cat] += m.monto
            monto_total += m.monto
        else:
            totales["sin_clasificar"] += m.monto
            monto_total += m.monto

    # 2. Calculamos los porcentajes (Evitando división por cero)
    porcentajes = {}
    if monto_total > 0:
        for cat, valor in totales.items():
            porcentajes[cat] = round((valor / monto_total) * 100, 2)
    else:
        porcentajes = {cat: 0 for cat in totales}

    return {
        "resumen_monetario": totales,
        "analisis_porcentual": porcentajes,
        "total_general": monto_total,
        "meta_ideal": {"necesidad": "50%", "deseo": "30%", "ahorro_deuda": "20%"}
    }

@app.get("/reporte/meta-corea")
def progreso_corea(db: Session = Depends(database.get_db)):
    # Sumamos solo lo que esté en la categoría de ahorro
    ahorro_actual = db.query(func.sum(models.Movimiento.monto)).filter(
        models.Movimiento.categoria_maestra == "ahorro_deuda",
        models.Movimiento.tipo == "ahorro"
    ).scalar() or 0
    
    meta_objetivo = 10000000  # 10 Millones
    faltante = meta_objetivo - ahorro_actual
    porcentaje = round((ahorro_actual / meta_objetivo) * 100, 2)
    
    return {
        "meta": "Viaje a Corea del Sur",
        "ahorro_actual": ahorro_actual,
        "faltante": faltante,
        "porcentaje_progreso": f"{porcentaje}%",
        "mensaje": "¡Fighting! Cada peso te acerca más a Seúl" if porcentaje < 50 else "¡Ya casi preparas maletas!"
    }

@app.get("/reporte/deudas")
def estado_deudas(db: Session = Depends(database.get_db)):
    # Buscamos todos los movimientos de tipo 'prestamo'
    prestamos = db.query(models.Movimiento).filter(models.Movimiento.tipo == "prestamo").all()
    
    analisis = []
    total_por_pagar = 0
    
    for p in prestamos:
        # Calculamos cuánto falta (suponiendo que monto es el total inicial)
        monto_cuota = p.monto / p.cuotas_totales
        pagado = monto_cuota * p.cuota_actual
        pendiente = p.monto - pagado
        total_por_pagar += pendiente
        
        analisis.append({
            "concepto": p.concepto,
            "progreso_cuotas": f"{p.cuota_actual}/{p.cuotas_totales}",
            "monto_total": p.monto,
            "valor_cuota": round(monto_cuota, 2),
            "saldo_pendiente": round(pendiente, 2)
        })
    
    return {
        "resumen": analisis,
        "deuda_total_consolidada": total_por_pagar,
        "mensaje": "¡Sigue así! Cada cuota es un paso hacia tu libertad financiera."
    }