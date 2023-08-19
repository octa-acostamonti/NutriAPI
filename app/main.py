from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session, load_only


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


@app.get("/")
async def root():
    return  ({"mi no bia":"e e e "})



@app.get("/proteinas/")
def get_proteinas(db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT producto,marca,proteina_g,cantidad FROM productos """)
    # proteina = cursor.fetchall()
    
    proteina = db.query(models.Productos).options(load_only("producto", "marca", "proteina_g", "cantidad")).all()
    
    return {"proteinas":proteina}


@app.get("/grasas/")
def get_grasas(db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT producto,marca,grasa_g,cantidad FROM productos """)
    # grasa = cursor.fetchall()
    
    grasa = db.query(models.Productos).options(load_only("producto", "marca", "grasa_g", "cantidad")).all()
    
    return {"grasas":grasa}


@app.get("/carbohidratos/")
def get_carbohidratos(db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT producto,marca,carbohidrato_g,cantidad FROM productos """)
    # carbohidrato = cursor.fetchall()
    
    carbohidratos = db.query(models.Productos).options(load_only("producto", "marca", "carbohidrato_g", "cantidad")).all()
    
    return {"carbohidratos":carbohidratos}


@app.get("/productos/")
def get_productos(db: Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * FROM productos""")
    # producto = cursor.fetchall()
    
    productos = db.query(models.Productos).all()

    return {"data":productos}



