import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.carga import carga
from scraper.extraer import extraer_productos_argentina
from app.database import SessionLocal
from app.models import Productos
import pandas as pd


def main():
    """ETL pipeline: Extract from Open Food Facts, Transform, Load to PostgreSQL."""
    print("Iniciando extracción de Open Food Facts...")
    df_productos = extraer_productos_argentina()
    
    print("\nResumen del dataset:")
    print(f"  - Total productos: {len(df_productos)}")
    print(f"  - Con Nutri-Score: {df_productos['nutriscore_grade'].notna().sum()}")
    print(f"  - Con NOVA group: {df_productos['nova_group'].notna().sum()}")
    
    print("\nCargando datos a PostgreSQL...")
    carga(df_productos)
    
    print("\nETL completado.")


def db_to_dataframe():
    """Extract data from 'productos' table and return as pandas DataFrame."""
    session = SessionLocal()
    try:
        productos = session.query(Productos).all()
        df = pd.DataFrame([producto.__dict__ for producto in productos])
        df = df.drop(columns=['_sa_instance_state'], errors='ignore')
        return df
    finally:
        session.close()


if __name__ == "__main__":
    main()
