"""Dia supermarket catalog scraper using VTEX Catalog API."""
from scraper.vtex_base import VTEXScraper, cargar_productos
import pandas as pd


DIA_CATEGORIES = [
    1,  # Almacén
    2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
    29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 48, 49, 50, 51, 52,
    53,  # Bebés y Niños
    54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
    71,  # Mascotas
    72, 73, 74, 75, 76, 77, 78, 79,
    80,  # Desayuno
    81, 82, 83, 84, 85, 86, 87, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104,
    105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119,
    121,  # Frescos
    122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141,
    142, 143, 144, 145, 148, 149, 150, 151, 152, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163,
    164,  # Bebidas
    165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 177, 178, 179, 180, 181, 182, 183, 184, 185,
    186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199,
    200,  # Congelados
    201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215,
]

scraper = VTEXScraper(
    retailer_name="dia",
    base_url="https://diaonline.supermercadosdia.com.ar",
    categories=DIA_CATEGORIES
)


def extraer_productos_dia(max_products: int | None = None) -> pd.DataFrame:
    return scraper.extraer_productos(max_products)


def cargar_productos_dia(df: pd.DataFrame) -> tuple[int, int]:
    return cargar_productos(df, "dia")


if __name__ == "__main__":
    print("Extrayendo catálogo de Dia...")
    df = extraer_productos_dia()
    
    print(f"\nCargando {len(df)} productos a la base de datos...")
    inserted, updated = cargar_productos_dia(df)
    print(f"Carga completa: {inserted} insertados, {updated} actualizados")
