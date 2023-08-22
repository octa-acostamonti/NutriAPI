from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session, load_only
from schemas import ResponseProteina,ResponseCarbohidratos,ResponseGrasa, ResponseProductos
from typing import List

""" Creacion de las tablas en PostgreSQL a partir de los modelos en 'models.py' """
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


try:
    
    """ Conexion a PostgreSQL utilizando el driver psycopg2 """

    conn = psycopg2.connect(host="localhost",database="NutriAPI",user="postgres",
    password="root",cursor_factory=RealDictCursor)
    
    cursor = conn.cursor()
    
    print("Database conection was succesfull!")

except Exception as e:

    print("Conection to database failed")
    print("The Error was: ",e)


# Contuinar video 5:53:37
@app.get("/")
async def root():
    return  "NutriAPI ©"



@app.get("/proteinas/", response_model=List[ResponseProteina])
def get_proteinas(db: Session = Depends(get_db)):
    """ Conseguir las proteinas de todos los productos """
    
    proteina = db.query(models.Productos).options(load_only("producto", "marca", "proteina_g", "cantidad")).all()
    
    return proteina


@app.get("/grasas/", response_model=List[ResponseGrasa])
def get_grasas(db: Session = Depends(get_db)):
    """ Conseguir las grasas de todos los productos """
    
    grasa = db.query(models.Productos).options(load_only("producto", "marca", "grasa_g", "cantidad")).all()
    
    return grasa


@app.get("/carbohidratos/",response_model=List[ResponseCarbohidratos])
def get_carbohidratos(db: Session = Depends(get_db)):
    """ Conseguir los carbohidratos de todos los productos """
    
    carbohidratos = db.query(models.Productos).options(load_only("producto", "marca", "carbohidrato_g", "cantidad")).all()
    
    return carbohidratos


@app.get("/productos/", response_model=List[ResponseProductos])
def get_productos(db: Session = Depends(get_db)):
    """ Conseguir todos los productos """

    productos = db.query(models.Productos).all()

    return productos



