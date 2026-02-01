from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Float, TIMESTAMP, Text, text


class Productos(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    barcode = Column(String, unique=True, index=True)
    producto = Column(String)
    marca = Column(String)
    cantidad = Column(String)
    caloria_kcal = Column(Float)
    grasa_g = Column(Float)
    carbohidrato_g = Column(Float)
    proteina_g = Column(Float)
    nutriscore_grade = Column(String)
    nova_group = Column(Integer)
    ingredients_text = Column(Text)
    allergens = Column(String)
    image_url = Column(String)

class Requests(Base):
    __tablename__="requests"

    id_request = Column(Integer,primary_key=True,nullable=False)
    requested_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    id_producto = Column(Integer, ForeignKey("productos.id_producto"),nullable=False)


class RetailerProducts(Base):
    __tablename__ = "retailer_products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    retailer = Column(String, nullable=False, index=True)
    ean = Column(String, index=True)
    sku = Column(String)
    product_name = Column(String, nullable=False)
    brand = Column(String)
    price = Column(Float)
    list_price = Column(Float)
    category = Column(String)
    image_url = Column(String)
    product_url = Column(String)
    last_updated = Column(TIMESTAMP(timezone=True), server_default=text("now()"))

