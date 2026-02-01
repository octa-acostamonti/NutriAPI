"""Disco supermarket catalog scraper using VTEX Catalog API."""
import time
import requests
import pandas as pd
from typing import Generator


BASE_URL = "https://www.disco.com.ar"
API_URL = f"{BASE_URL}/api/catalog_system/pub/products/search"
BATCH_SIZE = 50
MAIN_CATEGORIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def extraer_productos_disco(max_products: int | None = None) -> pd.DataFrame:
    """Extract products from Disco catalog."""
    all_products = []
    total_extracted = 0
    
    for category_id in MAIN_CATEGORIES:
        print(f"Extrayendo categoría {category_id}...")
        
        for batch in _fetch_category_products(category_id):
            for product in batch:
                extracted = _extraer_info_producto(product)
                if extracted:
                    all_products.append(extracted)
                    total_extracted += 1
                    
                    if max_products and total_extracted >= max_products:
                        print(f"Alcanzado límite de {max_products} productos")
                        return pd.DataFrame(all_products)
            
            if max_products and total_extracted >= max_products:
                break
        
        print(f"  Categoría {category_id}: {len([p for p in all_products if p])} productos hasta ahora")
    
    print(f"\nTotal extraído: {len(all_products)} productos de Disco")
    return pd.DataFrame(all_products)


def _fetch_category_products(category_id: int) -> Generator[list, None, None]:
    """Fetch all products from a category with pagination."""
    offset = 0
    
    while True:
        url = f"{API_URL}?fq=C:/{category_id}/&_from={offset}&_to={offset + BATCH_SIZE - 1}"
        
        try:
            response = requests.get(url, timeout=30, headers={
                "User-Agent": "Mozilla/5.0 (compatible; NutriAPI/1.0)",
                "Accept": "application/json"
            })
            response.raise_for_status()
            products = response.json()
            
            if not products:
                break
                
            yield products
            
            if len(products) < BATCH_SIZE:
                break
                
            offset += BATCH_SIZE
            time.sleep(0.5)
            
        except requests.RequestException as e:
            print(f"Error fetching category {category_id} offset {offset}: {e}")
            break


def _extraer_info_producto(product: dict) -> dict | None:
    """Extract relevant fields from a VTEX product."""
    try:
        items = product.get("items", [])
        if not items:
            return None
        
        item = items[0]
        ean = item.get("ean", "")
        
        sellers = item.get("sellers", [])
        price = None
        list_price = None
        if sellers:
            offer = sellers[0].get("commertialOffer", {})
            price = offer.get("Price")
            list_price = offer.get("ListPrice")
        
        images = item.get("images", [])
        image_url = images[0].get("imageUrl", "") if images else ""
        
        categories = product.get("categories", [])
        category = categories[0].strip("/") if categories else ""
        
        return {
            "retailer": "disco",
            "ean": ean,
            "sku": item.get("itemId", ""),
            "product_name": product.get("productName", ""),
            "brand": product.get("brand", ""),
            "price": price,
            "list_price": list_price,
            "category": category,
            "image_url": image_url,
            "product_url": f"{BASE_URL}/{product.get('linkText', '')}/p",
        }
    except Exception as e:
        print(f"Error extracting product: {e}")
        return None


def cargar_productos_disco(df: pd.DataFrame) -> tuple[int, int]:
    """Load Disco products to database."""
    from app.database import SessionLocal
    from app.models import RetailerProducts
    
    if df.empty:
        return 0, 0
    
    df = df.drop_duplicates(subset=['ean'], keep='first')
    
    session = SessionLocal()
    inserted = 0
    updated = 0
    
    try:
        for _, row in df.iterrows():
            ean = row.get('ean')
            if not ean:
                continue
            
            existing = session.query(RetailerProducts).filter(
                RetailerProducts.retailer == "disco",
                RetailerProducts.ean == ean
            ).first()
            
            if existing:
                existing.product_name = row.get('product_name')
                existing.brand = row.get('brand')
                existing.price = row.get('price')
                existing.list_price = row.get('list_price')
                existing.category = row.get('category')
                existing.image_url = row.get('image_url')
                existing.product_url = row.get('product_url')
                updated += 1
            else:
                new_product = RetailerProducts(
                    retailer=row.get('retailer', 'disco'),
                    ean=ean,
                    sku=row.get('sku'),
                    product_name=row.get('product_name'),
                    brand=row.get('brand'),
                    price=row.get('price'),
                    list_price=row.get('list_price'),
                    category=row.get('category'),
                    image_url=row.get('image_url'),
                    product_url=row.get('product_url'),
                )
                session.add(new_product)
                inserted += 1
            
            if (inserted + updated) % 500 == 0:
                session.commit()
                print(f"  Progreso: {inserted} insertados, {updated} actualizados")
        
        session.commit()
        
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    
    return inserted, updated


if __name__ == "__main__":
    print("Extrayendo catálogo de Disco...")
    df = extraer_productos_disco()
    
    print(f"\nCargando {len(df)} productos a la base de datos...")
    inserted, updated = cargar_productos_disco(df)
    print(f"Carga completa: {inserted} insertados, {updated} actualizados")
