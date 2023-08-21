from pydantic import BaseModel


class Response(BaseModel):
    producto: str
    marca: str
    cantidad: str
    class Config:
        orm_mode = True


class ResponseProteina(Response):
    proteina_g: float

class ResponseGrasa(Response):
    grasa_g: float

class ResponseCarbohidratos(Response):
    carbohidrato_g: float

class ResponseProductos(Response):
    id:int
    proteina_g: float
    grasa_g: float
    carbohidratos:float


