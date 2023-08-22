from .database import Base
from datetime import datetime
from sqlalchemy import Column

from sqlalchemy import Integer, String, Float, Date


class Productos(Base):
    """ Tabla 'productos' """
    
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
    """ Tabla 'requests' """

    __tablename__="requests"

    id_request = Column(Integer,primary_key=True,nullable=False)
    requested_at = Column(Date)

    # AÑADIR FOREIGNKEY id_productos
