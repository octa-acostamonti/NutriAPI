from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine,get_db
from sqlalchemy.orm import Session, load_only
from .schemas import ResponseProteina,ResponseCarbohidratos,ResponseGrasa, ResponseProductos
from typing import List

""" Creacion de las tablas y conexión a PostgreSQL a partir de los modelos en 'models.py' """
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


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


def log_request(db: Session, id_producto:int):
    request_info = models.Requests(id_producto=id_producto)
    db.add(request_info)
    db.commit()
