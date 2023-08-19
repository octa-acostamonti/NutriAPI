from fastapi import FastAPI, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session


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

@app.get("/sqlalchemy")
def test_conection(db: Session = Depends(get_db)):
    return {"status":"success"}

@app.get("/proteinas/")
def get_proteinas():
    cursor.execute("""SELECT producto,marca,proteina_g,cantidad FROM productos """)
    proteina = cursor.fetchall()
    return {"proteinas":proteina}


@app.get("/grasas/")
def get_grasas():
    cursor.execute("""SELECT producto,marca,grasa_g,cantidad FROM productos """)
    grasa = cursor.fetchall()
    return {"grasas":grasa}


@app.get("/carbohidratos/")
def get_carbohidratos():
    cursor.execute("""SELECT producto,marca,carbohidrato_g,cantidad FROM productos """)
    carbohidrato = cursor.fetchall()
    return {"carbohidratos":carbohidrato}


@app.get("/productos/")
def get_productos():
    cursor.execute("""SELECT * FROM productos""")
    producto = cursor.fetchall()
    return {"productos":producto}


