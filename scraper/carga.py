import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Productos
from app.database import SessionLocal
import pandas as pd


def _to_int(value):
    """Convert value to int, handling NaN and float."""
    if pd.isna(value):
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def carga(df: pd.DataFrame):
    """
    Load products DataFrame into PostgreSQL with upsert logic.
    Uses barcode as unique identifier to update existing products.
    """
    df = df.drop_duplicates(subset=['barcode'], keep='first')
    
    session = SessionLocal()
    inserted = 0
    updated = 0
    skipped = 0
    seen_barcodes = set()
    
    try:
        for _, fila in df.iterrows():
            barcode = fila.get('barcode')
            if not barcode or barcode in seen_barcodes:
                skipped += 1
                continue
            seen_barcodes.add(barcode)
            
            existing = session.query(Productos).filter(Productos.barcode == barcode).first()
            
            if existing:
                existing.producto = fila.get('producto')
                existing.marca = fila.get('marca')
                existing.cantidad = fila.get('cantidad')
                existing.caloria_kcal = fila.get('caloria_kcal')
                existing.grasa_g = fila.get('grasa_g')
                existing.carbohidrato_g = fila.get('carbohidrato_g')
                existing.proteina_g = fila.get('proteina_g')
                existing.nutriscore_grade = fila.get('nutriscore_grade')
                existing.nova_group = _to_int(fila.get('nova_group'))
                existing.ingredients_text = fila.get('ingredients_text')
                existing.allergens = fila.get('allergens')
                existing.image_url = fila.get('image_url')
                updated += 1
            else:
                producto = Productos(
                    barcode=barcode,
                    producto=fila.get('producto'),
                    marca=fila.get('marca'),
                    cantidad=fila.get('cantidad'),
                    caloria_kcal=fila.get('caloria_kcal'),
                    grasa_g=fila.get('grasa_g'),
                    carbohidrato_g=fila.get('carbohidrato_g'),
                    proteina_g=fila.get('proteina_g'),
                    nutriscore_grade=fila.get('nutriscore_grade'),
                    nova_group=_to_int(fila.get('nova_group')),
                    ingredients_text=fila.get('ingredients_text'),
                    allergens=fila.get('allergens'),
                    image_url=fila.get('image_url'),
                )
                session.add(producto)
                inserted += 1
        
        session.commit()
        print(f"Carga completa: {inserted} insertados, {updated} actualizados")
        
    except Exception as error:
        session.rollback()
        print(f"Error durante la carga: {error}")
        raise
        
    finally:
        session.close()
