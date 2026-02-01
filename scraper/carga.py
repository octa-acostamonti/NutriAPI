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
                existing.serving_size = fila.get('serving_size')
                existing.serving_quantity_g = fila.get('serving_quantity_g')
                existing.product_quantity_g = fila.get('product_quantity_g')
                existing.caloria_kcal_100g = fila.get('caloria_kcal_100g')
                existing.grasa_g_100g = fila.get('grasa_g_100g')
                existing.carbohidrato_g_100g = fila.get('carbohidrato_g_100g')
                existing.proteina_g_100g = fila.get('proteina_g_100g')
                existing.caloria_kcal_serving = fila.get('caloria_kcal_serving')
                existing.grasa_g_serving = fila.get('grasa_g_serving')
                existing.carbohidrato_g_serving = fila.get('carbohidrato_g_serving')
                existing.proteina_g_serving = fila.get('proteina_g_serving')
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
                    serving_size=fila.get('serving_size'),
                    serving_quantity_g=fila.get('serving_quantity_g'),
                    product_quantity_g=fila.get('product_quantity_g'),
                    caloria_kcal_100g=fila.get('caloria_kcal_100g'),
                    grasa_g_100g=fila.get('grasa_g_100g'),
                    carbohidrato_g_100g=fila.get('carbohidrato_g_100g'),
                    proteina_g_100g=fila.get('proteina_g_100g'),
                    caloria_kcal_serving=fila.get('caloria_kcal_serving'),
                    grasa_g_serving=fila.get('grasa_g_serving'),
                    carbohidrato_g_serving=fila.get('carbohidrato_g_serving'),
                    proteina_g_serving=fila.get('proteina_g_serving'),
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
