import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models import Productos
from app.database import SessionLocal, engine
from sqlalchemy.exc import IntegrityError


def carga(nombre_tabla, df):
    try:
        
        engine
        
        session = SessionLocal()

        
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
            session.add(producto)
            session.commit() 
            print("Datos ingestados correctamente!")
        except IntegrityError as e:
            session.rollback()  
            print("Datos duplicados")
            
    
    except Exception as error:
        print("Error al insertar las filas", nombre_tabla, error)

    finally:
        
        if session:
            session.close()