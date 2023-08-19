from .database import Base
from sqlalchemy import Column
from sqlalchemy import Integer, String, Float


class Productos(Base):
    __tablename__ = "productos"

    id = Column(Integer,primary_key=True,nullable=False)
    producto = Column(String)
    marca = Column(String)
    cantidad = Column(String)
    caloria_g = Column(Integer)
    grasa_g = Column(Float)
    carbohidrato_g = Column(Float)
    proteina_g = Column(Float)