import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Productos
from app.database import SessionLocal, engine
from sqlalchemy.exc import IntegrityError


def carga(table_name, df):
    try:
        
        engine

        
        
        session = SessionLocal()

        
        for index, row in df.iterrows():
            producto = Productos(
                id_producto=index,
                producto=row['Producto'],
                marca=row['Marca'],
                cantidad=row['Cantidad(g)'],
                caloria_kcal=row['Caloria(kcal)'],
                grasa_g=row['Grasa(g)'],
                carbohidrato_g=row['Carbohidrato(g)'],
                proteina_g=row['Proteina(g)']
            )
            session.add(producto)

        try:
            session.add(producto)
            session.commit() 
        except IntegrityError as e:
            session.rollback()  
            
    
    except Exception as error:
        print("Failed to insert records into", table_name, error)

    finally:
        
        if session:
            session.close()