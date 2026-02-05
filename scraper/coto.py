"""Coto supermarket catalog scraper using Constructor.io API.

Coto Digital (cotodigital.com.ar) uses Constructor.io for their search/browse API.
This scraper fetches products by category using their public browse endpoint.

Total catalog: ~38,000 products across 10 main categories.
"""
import time
import requests
import pandas as pd
from typing import Generator


BASE_URL = "https://www.cotodigital.com.ar"
API_URL = "https://ac.cnstrc.com/browse/group_id"
API_KEY = "key_r6xzz4IAoTWcipni"
BATCH_SIZE = 100  # Constructor.io allows up to 100 results per page

# All Coto Digital categories (~38,000 products total)
COTO_CATEGORIES = [
    # Food & Beverages
    ("catv00001255", "Frescos"),       # Dairy, meats, produce - 2527 products
    ("catv00001254", "Almacén"),       # Pantry items - 4604 products
    ("catv00001256", "Bebidas"),       # Beverages - 3565 products
    ("catv00001296", "Congelados"),    # Frozen foods - 513 products
    # Personal Care & Cleaning
    ("catv00001257", "Perfumería"),    # Personal care - 3835 products
    ("catv00001258", "Limpieza"),      # Cleaning products - 1867 products
    # Home & Other
    ("catv00001260", "Hogar"),         # Home items - 10272 products
    ("catv00001259", "Textil"),        # Textiles - 7872 products
    ("catv00001261", "Aire Libre"),    # Outdoor - 941 products
    ("catv00001990", "Electro"),       # Electronics - 2148 products
]


def extraer_productos_coto(max_products: int | None = None) -> pd.DataFrame:
    """Extract products from Coto Digital catalog using Constructor.io API."""
    all_products = []
    total_extracted = 0
    seen_skus = set()
    
    for category_id, category_name in COTO_CATEGORIES:
        print(f"[coto] Extrayendo categoría {category_name} ({category_id})...")
        
        for batch in _fetch_category_products(category_id):
            for product in batch:
                extracted = _extraer_info_producto(product)
                if extracted and extracted.get('sku'):
                    sku = extracted['sku']
                    if sku not in seen_skus:
                        seen_skus.add(sku)
                        all_products.append(extracted)
                        total_extracted += 1
                    
                    if max_products and total_extracted >= max_products:
                        print(f"[coto] Alcanzado límite de {max_products} productos")
                        return pd.DataFrame(all_products)
            
            if max_products and total_extracted >= max_products:
                break
        
        print(f"[coto]   Categoría {category_name}: total {total_extracted} productos únicos")
    
    print(f"\n[coto] Total extraído: {len(all_products)} productos")
    return pd.DataFrame(all_products)


def _fetch_category_products(category_id: str) -> Generator[list, None, None]:
    """Fetch all products from a Coto category using Constructor.io browse API."""
    page = 1
    
    while True:
        url = f"{API_URL}/{category_id}"
        params = {
            "key": API_KEY,
            "num_results_per_page": BATCH_SIZE,
            "page": page,
        }
        
        try:
            response = requests.get(url, params=params, timeout=30, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
            })
            response.raise_for_status()
            data = response.json()
            
            results = data.get("response", {}).get("results", [])
            if not results:
                break
            
            yield results
            
            # Check if we've fetched all products
            total = data.get("response", {}).get("total_num_results", 0)
            fetched = page * BATCH_SIZE
            if fetched >= total:
                break
            
            page += 1
            time.sleep(0.3)  # Rate limiting
            
        except requests.RequestException as e:
            print(f"[coto] Error categoría {category_id} página {page}: {e}")
            break


def _extraer_info_producto(product: dict) -> dict | None:
    """Extract relevant fields from a Constructor.io product result."""
    try:
        data = product.get("data", {})
        
        # Extract SKU from product ID (format: "prod00000446" -> "00000446")
        product_id = data.get("id", "")
        sku = product_id.replace("prod", "") if product_id.startswith("prod") else product_id
        
        if not sku:
            return None
        
        # Product name from 'value' or 'description'
        product_name = product.get("value", "") or data.get("description", "")
        if not product_name:
            return None
        
        # Extract brand from product name (typically "BRAND" appears in uppercase)
        brand = _extract_brand(product_name)
        
        # Get first available price (from first store in the price list)
        prices = data.get("price", [])
        price = None
        list_price = None
        if prices:
            first_price = prices[0]
            price = first_price.get("formatPrice") or first_price.get("listPrice")
            list_price = first_price.get("listPrice")
        
        # Build URLs
        image_url = data.get("image_url", "")
        url_path = data.get("url", "")
        product_url = f"{BASE_URL}/sitios/cdigi/producto/{url_path}" if url_path else ""
        
        # Category from group_ids
        group_ids = data.get("group_ids", [])
        category = group_ids[0] if group_ids else ""
        
        # Use SKU as EAN fallback (Coto's SKU is often the product code)
        # Real EAN would need to be fetched from product detail page
        ean = sku
        
        return {
            "retailer": "coto",
            "ean": ean,
            "sku": sku,
            "product_name": product_name,
            "brand": brand,
            "price": float(price) if price else None,
            "list_price": float(list_price) if list_price else None,
            "category": category,
            "image_url": image_url,
            "product_url": product_url,
        }
    except Exception as e:
        print(f"[coto] Error extrayendo producto: {e}")
        return None


def _extract_brand(product_name: str) -> str:
    """Extract brand name from product name.
    
    Coto product names often follow pattern: "Description BRAND Size"
    e.g., "Leche Larga Vida Entera LA SERENISIMA Sachet 1l"
    """
    import re
    
    # Common brand patterns (all caps words that are likely brands)
    # This is a heuristic - brands are typically 2+ uppercase words together
    brand_pattern = r'\b([A-Z][A-Z]+(?:\s+[A-Z][A-Z]+)*)\b'
    matches = re.findall(brand_pattern, product_name)
    
    # Filter out common non-brand words
    non_brands = {'ML', 'LT', 'GR', 'KG', 'UN', 'CC', 'CM', 'MM', 'PK', 'PACK', 'X', 'TTB', 'PET'}
    brands = [m for m in matches if m not in non_brands and len(m) > 2]
    
    return brands[0] if brands else ""


def cargar_productos_coto(df: pd.DataFrame) -> tuple[int, int]:
    """Load Coto products to database."""
    from scraper.vtex_base import cargar_productos
    return cargar_productos(df, "coto")


if __name__ == "__main__":
    print("Extrayendo catálogo de Coto Digital...")
    df = extraer_productos_coto()
    
    if df.empty:
        print("No se extrajeron productos. Verifica la conexión y el API.")
    else:
        print(f"\nMuestra de productos extraídos:")
        print(df[['sku', 'product_name', 'brand', 'price']].head(10).to_string())
        
        print(f"\nCargando {len(df)} productos a la base de datos...")
        inserted, updated = cargar_productos_coto(df)
        print(f"Carga completa: {inserted} insertados, {updated} actualizados")
