from carga import carga
from extraer import extraer_info_nutricional, estandarizar_a_100g
from utils import conseguir_urls
from cProfile import Profile
from app.database import SessionLocal, engine
from app.models import Productos
import pandas as pd


def main():
    """ Main loop for the scraper """

    import pstats

    with Profile() as pr:
        

    
        URLS = conseguir_urls() # Gets a list of all the URLS to scrape

        Tabla_Nutricional_Productos = extraer_info_nutricional(URLS) # Scrapes the URLS and gets the Nutritional Information and stores it into a Pandas DataFrame

        Tabla_Nutricional_Productos_Estandarizada = estandarizar_a_100g(Tabla_Nutricional_Productos) # Standardize the nutritional information to 100g

        carga("productos",Tabla_Nutricional_Productos_Estandarizada) # Creates a conection with the table "productos" in PostreSQL, and loads the Pandas DataFrame

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='stats.prof')


def db_to_dataframe():
    """
    Extrae datos de la tabla 'productos' y los devuelve como un DataFrame de pandas.
    """
    # Crea una sesión en la base de datos
    session = SessionLocal()
    try:
        # Realiza una consulta para obtener todos los registros de la tabla 'productos'
        productos = session.query(Productos).all()
        # Convierte los resultados en un DataFrame de pandas
        df = pd.DataFrame([producto.__dict__ for producto in productos])
        # Elimina la columna '_sa_instance_state' que es añadida por SQLAlchemy
        df = df.drop(columns=['_sa_instance_state'])
        return df
    finally:
        # Cierra la sesión para liberar los recursos
        session.close()


if __name__ == "__main__":
    main()
    # Llama a la función para obtener el DataFrame
    df_productos = db_to_dataframe()
    # Imprime el DataFrame
    print(df_productos)

    