import sys
import os

# This solves a issue with relative paths 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Productos
from app.database import SessionLocal, engine
from sqlalchemy.exc import IntegrityError

# Define the carga function asking for a table name and a DataFrame
def carga(nombre_tabla, df):
    
    try:
        
        engine # Connect to the PostgreSQL engine
        
        session = SessionLocal() # We instanciate a Session of PostgreSQL to operate 

        # We add everyproducto to the PostgreSQL
        for index, fila in df.iterrows():
            producto = Productos(
                id_producto=index,
                producto=fila['Producto'],
                marca=fila['Marca'],
                cantidad=fila['Cantidad(g)'],
                caloria_kcal=fila['Caloria(kcal)'],
                grasa_g=fila['Grasa(g)'],
                carbohidrato_g=fila['Carbohidrato(g)'],
                proteina_g=fila['Proteina(g)']
            )
            session.add(producto)

        try:
            # If we can add all of the products we commit them
            session.add(producto)
            session.commit() 
            print("Datos ingestados correctamente!")
            # If not we do a rollback since there are already products in the database
        except IntegrityError as e:
            session.rollback()  
            print("Datos duplicados")
            
    
    except Exception as error:
        print("Error al insertar las filas", nombre_tabla, error)

    finally:
        # We close the session
        if session:
            session.close()