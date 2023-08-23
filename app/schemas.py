from pydantic import BaseModel


class Response(BaseModel):
    """ Configuracion de la respuesta base """
    producto: str
    marca: str
    cantidad: str
    class Config:
        from_attributes = True


class ResponseProteina(Response):
    """ Configuracion de la respuesta de proteinas con herencia de la respuesta base """
    proteina_g: float

class ResponseGrasa(Response):
    """ Configuracion de la respuesta de grasas con herencia de la respuesta base """
    grasa_g: float

class ResponseCarbohidratos(Response):
    """ Configuracion de la respuesta de carbohidratos con herencia de la respuesta base """
    carbohidrato_g: float

class ResponseProductos(Response):
    """ Configuracion de la respuesta de los productos con herencia de la respuesta base """
    id:int
    proteina_g: float
    grasa_g: float
    carbohidratos:float


