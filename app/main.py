from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session, load_only
from schemas import ResponseProteina,ResponseCarbohidratos,ResponseGrasa, ResponseProductos
from typing import List


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

try:
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
    
    # cursor.execute("""SELECT producto,marca,proteina_g,cantidad FROM productos """)
    # proteina = cursor.fetchall()
    
    proteina = db.query(models.Productos).options(load_only("producto", "marca", "proteina_g", "cantidad")).all()
    
    return proteina


@app.get("/grasas/", response_model=List[ResponseGrasa])
def get_grasas(db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT producto,marca,grasa_g,cantidad FROM productos """)
    # grasa = cursor.fetchall()
    
    grasa = db.query(models.Productos).options(load_only("producto", "marca", "grasa_g", "cantidad")).all()
    
    return grasa


@app.get("/carbohidratos/",response_model=List[ResponseCarbohidratos])
def get_carbohidratos(db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT producto,marca,carbohidrato_g,cantidad FROM productos """)
    # carbohidrato = cursor.fetchall()
    
    carbohidratos = db.query(models.Productos).options(load_only("producto", "marca", "carbohidrato_g", "cantidad")).all()
    
    return carbohidratos


@app.get("/productos/", response_model=List[ResponseProductos])
def get_productos(db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * FROM productos""")
    # producto = cursor.fetchall()
    
    productos = db.query(models.Productos).all()

    return productos



