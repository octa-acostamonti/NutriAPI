from .database import Base
from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, String, Float, TIMESTAMP, text


class Productos(Base):
    """ Crear Tabla 'productos' """
    
    __tablename__ = "productos"

    id_producto = Column(Integer,primary_key=True,nullable=False)
    producto = Column(String)
    marca = Column(String)
    cantidad = Column(String)
    caloria_kcal = Column(Integer)
    grasa_g = Column(Float)
    carbohidrato_g = Column(Float)
    proteina_g = Column(Float)

class Requests(Base):
    """ Crear Tabla 'requests' """

    __tablename__="requests"

    id_request = Column(Integer,primary_key=True,nullable=False)
    requested_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    id_producto = Column(Integer, ForeignKey("productos.id_producto"),nullable=False)

