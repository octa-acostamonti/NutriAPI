import sys
import os
import pandas as pd
from openfoodfacts import ProductDataset

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import RetailerProducts, Productos


def get_unmatched_eans():
    session = SessionLocal()
    
    retailer_eans = set(
        e[0] for e in session.query(RetailerProducts.ean).distinct().all() 
        if e[0] and len(e[0]) >= 8
    )
    
    nutri_eans = set(
        b[0] for b in session.query(Productos.barcode).all() 
        if b[0]
    )
    
    session.close()
    
    unmatched = retailer_eans - nutri_eans
    return unmatched


def extraer_productos_global(target_eans: set):
    print("Loading Open Food Facts CSV dataset...")
    dataset = ProductDataset(dataset_type="csv")
    
    productos_matched = []
    total_procesados = 0
    
    print(f"Searching for {len(target_eans)} EANs in global database...")
    for product in dataset:
        total_procesados += 1
        
        if total_procesados % 100000 == 0:
            print(f"  Processed {total_procesados:,} products | Matches: {len(productos_matched)}")
        
        barcode = product.get("code", "")
        if barcode not in target_eans:
            continue
        
        producto_info = _extraer_info_producto(product)
        if producto_info:
            productos_matched.append(producto_info)
    
    print(f"Extraction complete: {len(productos_matched)} matches found")
    return pd.DataFrame(productos_matched)


def _extraer_info_producto(product: dict) -> dict | None:
    barcode = product.get("code")
    if not barcode:
        return None
    
    producto_nombre = product.get("product_name") or product.get("product_name_es", "")
    if not producto_nombre:
        return None
    
    return {
        "barcode": barcode,
        "producto": producto_nombre,
        "marca": product.get("brands", ""),
        "serving_size": product.get("serving_size") or product.get("quantity", ""),
        "serving_quantity_g": _safe_float(product.get("serving_quantity")),
        "product_quantity_g": _safe_float(product.get("product_quantity")),
        "caloria_kcal_100g": _safe_float(product.get("energy-kcal_100g")),
        "grasa_g_100g": _safe_float(product.get("fat_100g")),
        "carbohidrato_g_100g": _safe_float(product.get("carbohydrates_100g")),
        "proteina_g_100g": _safe_float(product.get("proteins_100g")),
        "caloria_kcal_serving": _safe_float(product.get("energy-kcal_serving")),
        "grasa_g_serving": _safe_float(product.get("fat_serving")),
        "carbohidrato_g_serving": _safe_float(product.get("carbohydrates_serving")),
        "proteina_g_serving": _safe_float(product.get("proteins_serving")),
        "nutriscore_grade": product.get("nutriscore_grade", ""),
        "nova_group": _safe_int(product.get("nova_group"), min_val=1, max_val=4),
        "ingredients_text": product.get("ingredients_text_es") or product.get("ingredients_text", ""),
        "allergens": _format_allergens(product.get("allergens", "")),
        "image_url": product.get("image_url", ""),
    }


def _safe_float(value) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _safe_int(value, min_val: int = None, max_val: int = None) -> int | None:
    if value is None or value == "":
        return None
    try:
        result = int(float(value))
        if min_val is not None and result < min_val:
            return None
        if max_val is not None and result > max_val:
            return None
        return result
    except (ValueError, TypeError):
        return None


def _format_allergens(allergens: str) -> str:
    if not allergens:
        return ""
    tags = [tag.strip().replace("en:", "") for tag in allergens.split(",")]
    return ", ".join(tags)


def save_products(df):
    session = SessionLocal()
    inserted = 0
    updated = 0
    
    for _, row in df.iterrows():
        try:
            existing = session.query(Productos).filter(Productos.barcode == row["barcode"]).first()
            
            if existing:
                for key, value in row.items():
                    if key != "barcode":
                        setattr(existing, key, value if pd.notna(value) else None)
                updated += 1
            else:
                product_data = {k: (v if pd.notna(v) else None) for k, v in row.items()}
                producto = Productos(**product_data)
                session.add(producto)
                inserted += 1
            
            if (inserted + updated) % 500 == 0:
                session.commit()
                print(f"  Saved {inserted + updated} products...")
                
        except Exception as e:
            session.rollback()
            print(f"  Error saving {row['barcode']}: {e}")
    
    session.commit()
    session.close()
    
    return inserted, updated


def main():
    print("=" * 60)
    print("MATCHING RETAILER EANS AGAINST GLOBAL OPEN FOOD FACTS")
    print("=" * 60)
    
    print("\nGetting unmatched EANs from retailer data...")
    unmatched_eans = get_unmatched_eans()
    print(f"Found {len(unmatched_eans)} EANs without nutritional data")
    
    matched_df = extraer_productos_global(unmatched_eans)
    
    if len(matched_df) > 0:
        print(f"\nSaving {len(matched_df)} products to database...")
        inserted, updated = save_products(matched_df)
        
        print("\n" + "=" * 60)
        print("COMPLETE")
        print("=" * 60)
        print(f"  Inserted: {inserted}")
        print(f"  Updated: {updated}")
    else:
        print("\nNo matches found.")


if __name__ == "__main__":
    main()
