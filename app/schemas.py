from pydantic import BaseModel
from typing import Optional


class Response(BaseModel):
    producto: str
    marca: Optional[str] = None
    cantidad: Optional[str] = None

    class Config:
        from_attributes = True


class ResponseProteina(Response):
    proteina_g: Optional[float] = None


class ResponseGrasa(Response):
    grasa_g: Optional[float] = None


class ResponseCarbohidratos(Response):
    carbohidrato_g: Optional[float] = None


class ResponseProductos(Response):
    id_producto: int
    barcode: Optional[str] = None
    caloria_kcal: Optional[float] = None
    proteina_g: Optional[float] = None
    grasa_g: Optional[float] = None
    carbohidrato_g: Optional[float] = None
    nutriscore_grade: Optional[str] = None
    nova_group: Optional[int] = None
    ingredients_text: Optional[str] = None
    allergens: Optional[str] = None
    image_url: Optional[str] = None


class ResponseRetailerProduct(BaseModel):
    id: int
    retailer: str
    ean: Optional[str] = None
    sku: Optional[str] = None
    product_name: str
    brand: Optional[str] = None
    price: Optional[float] = None
    list_price: Optional[float] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    product_url: Optional[str] = None

    class Config:
        from_attributes = True


class ResponseEnrichedProduct(ResponseRetailerProduct):
    nutriscore_grade: Optional[str] = None
    nova_group: Optional[int] = None
    caloria_kcal: Optional[float] = None
    proteina_g: Optional[float] = None
    grasa_g: Optional[float] = None
    carbohidrato_g: Optional[float] = None
    allergens: Optional[str] = None
    ingredients_text: Optional[str] = None
