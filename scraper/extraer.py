import pandas as pd
from openfoodfacts import ProductDataset


def extraer_productos_argentina():
    """
    Download Open Food Facts CSV dataset and filter Argentina products.
    Returns a pandas DataFrame with nutritional information.
    """
    print("Descargando dataset de Open Food Facts (esto puede tomar unos minutos la primera vez)...")
    dataset = ProductDataset(dataset_type="csv")
    
    productos_argentina = []
    total_procesados = 0
    
    print("Filtrando productos de Argentina...")
    for product in dataset:
        total_procesados += 1
        
        if total_procesados % 100000 == 0:
            print(f"Procesados {total_procesados} productos, encontrados {len(productos_argentina)} de Argentina...")
        
        countries = product.get("countries_tags", "") or ""
        if "en:argentina" not in countries.lower():
            continue
        
        producto_info = _extraer_info_producto(product)
        if producto_info:
            productos_argentina.append(producto_info)
    
    print(f"Extracción completa: {len(productos_argentina)} productos de Argentina encontrados")
    
    df = pd.DataFrame(productos_argentina)
    return df


def _extraer_info_producto(product: dict) -> dict | None:
    """Extract relevant fields from a single Open Food Facts product."""
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
        "cantidad": product.get("serving_size") or product.get("quantity", "100g"),
        "caloria_kcal": _safe_float(product.get("energy-kcal_100g")),
        "grasa_g": _safe_float(product.get("fat_100g")),
        "carbohidrato_g": _safe_float(product.get("carbohydrates_100g")),
        "proteina_g": _safe_float(product.get("proteins_100g")),
        "nutriscore_grade": product.get("nutriscore_grade", ""),
        "nova_group": _safe_int(product.get("nova_group"), min_val=1, max_val=4),
        "ingredients_text": product.get("ingredients_text_es") or product.get("ingredients_text", ""),
        "allergens": _format_allergens(product.get("allergens", "")),
        "image_url": product.get("image_url", ""),
    }


def _safe_float(value) -> float | None:
    """Safely convert a value to float, returning None if not possible."""
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def _safe_int(value, min_val: int = None, max_val: int = None) -> int | None:
    """Safely convert a value to int, returning None if not possible or out of range."""
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
    """Format allergens string by removing 'en:' prefixes."""
    if not allergens:
        return ""
    tags = [tag.strip().replace("en:", "") for tag in allergens.split(",")]
    return ", ".join(tags)
