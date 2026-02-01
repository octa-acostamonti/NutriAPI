"""Base VTEX catalog scraper for Argentine supermarkets."""
import time
import requests
import pandas as pd
from typing import Generator


BATCH_SIZE = 50


class VTEXScraper:
    def __init__(
        self,
        retailer_name: str,
        base_url: str,
        categories: list[int],
        ean_from_spec: str | None = None
    ):
        self.retailer_name = retailer_name
        self.base_url = base_url
        self.api_url = f"{base_url}/api/catalog_system/pub/products/search"
        self.categories = categories
        self.ean_from_spec = ean_from_spec

    def extraer_productos(self, max_products: int | None = None) -> pd.DataFrame:
        """Extract products from catalog."""
        all_products = []
        total_extracted = 0
        seen_eans = set()
        
        for category_id in self.categories:
            print(f"[{self.retailer_name}] Extrayendo categoría {category_id}...")
            
            for batch in self._fetch_category_products(category_id):
                for product in batch:
                    extracted = self._extraer_info_producto(product)
                    if extracted and extracted.get('ean'):
                        ean = extracted['ean']
                        if ean not in seen_eans:
                            seen_eans.add(ean)
                            all_products.append(extracted)
                            total_extracted += 1
                        
                        if max_products and total_extracted >= max_products:
                            print(f"[{self.retailer_name}] Alcanzado límite de {max_products} productos")
                            return pd.DataFrame(all_products)
                
                if max_products and total_extracted >= max_products:
                    break
            
            print(f"[{self.retailer_name}]   Categoría {category_id}: total {total_extracted} productos únicos")
        
        print(f"\n[{self.retailer_name}] Total extraído: {len(all_products)} productos")
        return pd.DataFrame(all_products)

    def _fetch_category_products(self, category_id: int) -> Generator[list, None, None]:
        """Fetch all products from a category with pagination."""
        offset = 0
        
        while True:
            url = f"{self.api_url}?fq=C:/{category_id}/&_from={offset}&_to={offset + BATCH_SIZE - 1}"
            
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
                time.sleep(0.3)
                
            except requests.RequestException as e:
                if "400" in str(e):
                    break
                print(f"[{self.retailer_name}] Error categoría {category_id} offset {offset}: {e}")
                break

    def _extraer_info_producto(self, product: dict) -> dict | None:
        """Extract relevant fields from a VTEX product."""
        try:
            items = product.get("items", [])
            if not items:
                return None
            
            item = items[0]
            ean = item.get("ean", "")
            
            if self.ean_from_spec and not ean:
                spec_ean = product.get(self.ean_from_spec, [])
                if spec_ean:
                    ean = spec_ean[0] if isinstance(spec_ean, list) else spec_ean
            
            if not ean:
                return None
            
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
                "retailer": self.retailer_name,
                "ean": ean,
                "sku": item.get("itemId", ""),
                "product_name": product.get("productName", ""),
                "brand": product.get("brand", ""),
                "price": price,
                "list_price": list_price,
                "category": category,
                "image_url": image_url,
                "product_url": f"{self.base_url}/{product.get('linkText', '')}/p",
            }
        except Exception as e:
            print(f"[{self.retailer_name}] Error extrayendo producto: {e}")
            return None


def cargar_productos(df: pd.DataFrame, retailer: str) -> tuple[int, int]:
    """Load retailer products to database."""
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
                RetailerProducts.retailer == retailer,
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
                    retailer=row.get('retailer', retailer),
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
                print(f"[{retailer}] Progreso: {inserted} insertados, {updated} actualizados")
        
        session.commit()
        
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
    
    return inserted, updated
