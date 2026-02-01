import sys
import os
import time
import requests

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
    return list(unmatched)


def fetch_product_from_off(ean):
    url = f"https://world.openfoodfacts.org/api/v0/product/{ean}.json"
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "NutriAPI/1.0"})
        data = resp.json()
        
        if data.get("status") != 1:
            return None
        
        product = data.get("product", {})
        
        product_name = product.get("product_name") or product.get("product_name_es", "")
        if not product_name:
            return None
        
        return {
            "barcode": ean,
            "producto": product_name,
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
            "nova_group": _safe_int(product.get("nova_group")),
            "ingredients_text": product.get("ingredients_text_es") or product.get("ingredients_text", ""),
            "allergens": _format_allergens(product.get("allergens", "")),
            "image_url": product.get("image_url", ""),
        }
    except Exception as e:
        return None


def _safe_float(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _safe_int(value):
    if value is None or value == "":
        return None
    try:
        result = int(float(value))
        if result < 1 or result > 4:
            return None
        return result
    except (ValueError, TypeError):
        return None


def _format_allergens(allergens):
    if not allergens:
        return ""
    tags = [tag.strip().replace("en:", "") for tag in allergens.split(",")]
    return ", ".join(tags)


def save_product(product_data):
    session = SessionLocal()
    try:
        existing = session.query(Productos).filter(Productos.barcode == product_data["barcode"]).first()
        
        if existing:
            for key, value in product_data.items():
                if key != "barcode":
                    setattr(existing, key, value)
            session.commit()
            return "updated"
        else:
            producto = Productos(**product_data)
            session.add(producto)
            session.commit()
            return "inserted"
    except Exception as e:
        session.rollback()
        return "error"
    finally:
        session.close()


def main():
    print("=" * 60)
    print("FETCHING NUTRITIONAL DATA FROM GLOBAL OPEN FOOD FACTS")
    print("=" * 60)
    
    print("\nGetting unmatched EANs from retailer data...")
    unmatched_eans = get_unmatched_eans()
    print(f"Found {len(unmatched_eans)} EANs without nutritional data")
    
    inserted = 0
    updated = 0
    not_found = 0
    errors = 0
    
    print(f"\nFetching from global Open Food Facts API...")
    print("(This may take a while - ~1 request per second to be polite)")
    
    for i, ean in enumerate(unmatched_eans):
        product_data = fetch_product_from_off(ean)
        
        if product_data:
            result = save_product(product_data)
            if result == "inserted":
                inserted += 1
            elif result == "updated":
                updated += 1
            else:
                errors += 1
        else:
            not_found += 1
        
        if (i + 1) % 100 == 0:
            print(f"  Progress: {i + 1}/{len(unmatched_eans)} | Found: {inserted + updated} | Not found: {not_found}")
        
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("COMPLETE")
    print("=" * 60)
    print(f"  Inserted: {inserted}")
    print(f"  Updated: {updated}")
    print(f"  Not found in OFF: {not_found}")
    print(f"  Errors: {errors}")
    print(f"  Total processed: {len(unmatched_eans)}")


if __name__ == "__main__":
    main()
