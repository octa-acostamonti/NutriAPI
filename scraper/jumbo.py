"""Jumbo supermarket catalog scraper using VTEX Catalog API."""
from scraper.vtex_base import VTEXScraper, cargar_productos
import pandas as pd


JUMBO_CATEGORIES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

scraper = VTEXScraper(
    retailer_name="jumbo",
    base_url="https://www.jumbo.com.ar",
    categories=JUMBO_CATEGORIES
)


def extraer_productos_jumbo(max_products: int | None = None) -> pd.DataFrame:
    return scraper.extraer_productos(max_products)


def cargar_productos_jumbo(df: pd.DataFrame) -> tuple[int, int]:
    return cargar_productos(df, "jumbo")


if __name__ == "__main__":
    print("Extrayendo catálogo de Jumbo...")
    df = extraer_productos_jumbo()
    
    print(f"\nCargando {len(df)} productos a la base de datos...")
    inserted, updated = cargar_productos_jumbo(df)
    print(f"Carga completa: {inserted} insertados, {updated} actualizados")
