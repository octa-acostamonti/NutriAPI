"""

IMPORTAMOS LAS LIBRERIAS NECESARIAS

"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

"""

DEFINIR VARIABLE PARA CONSEGUIR TODAS LAS URLS DE LA PÁGINA

"""
# Lista vacia que contenga todas las URLS de la página
URLS = [] 

# Definimos la URL_BASE, la cual es la misma para todas las paginas
URL_BASE = "https://www.fatsecret.com.ar/calor%C3%ADas-nutrici%C3%B3n/search?q=9+de+Oro&pg=" # Definimos la URL_BASE, la cual es la misma para todas las paginas

# Hacemos un loop que agregue a la URL_BASE el numero de página.
for num in range(0,271):

    URL = URL_BASE + str(num) 
    URLS.append(URL) # Agregamos a la lista vacia las URLS de todas las página

"""
CREAMOS EL DATAFRAME QUE CONTENERA LOS PRODUCTOS
"""
Tabla_Nutricional_Productos = pd.DataFrame()

"""
LOOP PRINCIPAL PARA CONSEGUIR LA INFORMACIÓN NUTRICIONAL
"""
def main():
    global Tabla_Nutricional_Productos
    
    for url in URLS:
    
        page = requests.get(url)

        pagesoup = BeautifulSoup(page.content, "html.parser")

        tabla = pagesoup.find("td",class_="leftCell")

        Productos = tabla.find_all("a",class_="prominent")
        Producto = [caracter.text for caracter in Productos]
        print("Productos conseguido...")
        
        Marcas = tabla.find_all("a",class_="brand")
        Marca = [caracter.text.replace("(","").replace(")","") if len(caracter.text) > 0 else None for caracter in Marcas]
        print("Marca conseguida...")
        
        Cantidades = tabla.find_all("div",class_="smallText greyText greyLink")
        Cantidad = [caracter.text.replace("\r", "").replace("\n", "").replace("\t", "").split("-", 1)[0] for caracter in Cantidades]
        print("Cantidad  conseguida...")   
        
        Calorias = tabla.find_all("div", class_="smallText greyText greyLink")
        Caloria = [caracter.text.replace("\r", "").replace("\n", "").replace("\t", "").split("-", 1)[-1].split("|")[0].strip().replace("Calorías:", "").strip() 
            for caracter in Calorias]
        print("Calorias conseguida...")    
        
        Grasas = tabla.find_all("div", class_="smallText greyText greyLink")
        Grasa = [caracter.text.replace("\r", "").replace("\n", "").replace("\t", "").split("|", 1)[-1].split("|")[0].strip().replace("Grasa:", "").strip() 
            for caracter in Grasas]
        print("Grasas conseguida...")    
        
        Carbohidratos = tabla.find_all("div", class_="smallText greyText greyLink")
        Carbohidrato = [caracter.text.replace("\r", "").replace("\n", "").replace("\t", "").split("|", 2)[-1].split("|")[0].strip().replace("Carbh:", "").strip()
            for caracter in Carbohidratos]
        print("Carbohidratos conseguida...")    
        
        Proteinas = tabla.find_all("div", class_="smallText greyText greyLink")
        Proteina = [caracter.text.replace("\r", "").replace("\n", "").replace("\t", "").split("|", 3)[-1].split("|")[0].strip().replace("Prot:", "").split("g", 1)[0] + "g".strip() 
            for caracter in Proteinas]
        print("Proteina  conseguida...")
        
        
        if not Tabla_Nutricional_Productos.empty:
            columnas = ["Producto","Marca","Cantidad","Caloria","Grasa","Carbohidrato","Proteina"]
            data_ = list(zip(Producto, Marca, Cantidad, Caloria, Grasa, Carbohidrato, Proteina))
            df = pd.DataFrame(columns=columnas,data=data_)
            Tabla_Nutricional_Productos = pd.concat([Tabla_Nutricional_Productos,df],ignore_index=True)
        else:
            columnas = ["Producto","Marca","Cantidad","Caloria","Grasa","Carbohidrato","Proteina"]
            data_ = list(zip(Producto, Marca, Cantidad, Caloria, Grasa, Carbohidrato, Proteina))
            Tabla_Nutricional_Productos = pd.DataFrame(columns=columnas,data=data_)

    return Tabla_Nutricional_Productos.to_csv("Tabla_Nutricional_Productos.csv")

main()


    