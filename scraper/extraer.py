import requests
from bs4 import BeautifulSoup
import pandas as pd 

def extraer_info_nutricional(URLS):
    result = []
    num_pagina=0

    for url in URLS:
        num_pagina += 1
        page = requests.get(url)
        pagesoup = BeautifulSoup(page.content, "html.parser")
        tabla = pagesoup.find("td", class_="leftCell")

        productos = tabla.find_all("a", class_="prominent")
        marcas = tabla.find_all("a", class_="brand")
        cantidades = tabla.find_all("div", class_="smallText greyText greyLink")
        calorias = tabla.find_all("div", class_="smallText greyText greyLink")
        grasas = tabla.find_all("div", class_="smallText greyText greyLink")
        carbohidratos = tabla.find_all("div", class_="smallText greyText greyLink")
        proteinas = tabla.find_all("div", class_="smallText greyText greyLink")

        for producto, marca, cantidad, caloria, grasa, carbohidrato, proteina in zip(productos, marcas, cantidades, calorias, grasas, carbohidratos, proteinas):
            producto_info = {
                "Producto": producto.text,
                "Marca": marca.text.replace("(", "").replace(")", "") if len(marca.text) > 0 else None,
                "Cantidad(g)": cantidad.text.replace("\r", "").replace("\n", "").replace("\t", "").split("-", 1)[0],
                "Caloria(kcal)": caloria.text.replace("\r", "").replace("\n", "").replace("\t", "").split("-", 1)[-1].split("|")[0].strip().replace("Calorías:", "").strip(),
                "Grasa(g)": grasa.text.replace("\r", "").replace("\n", "").replace("\t", "").split("|", 1)[-1].split("|")[0].strip().replace("Grasa:", "").strip(),
                "Carbohidrato(g)": carbohidrato.text.replace("\r", "").replace("\n", "").replace("\t", "").split("|", 2)[-1].split("|")[0].strip().replace("Carbh:", "").strip(),
                "Proteina(g)": proteina.text.replace("\r", "").replace("\n", "").replace("\t", "").split("|", 3)[-1].split("|")[0].strip().replace("Prot:", "").split("g", 1)[0].strip()
            }
            
            producto_info["Proteina(g)"] = producto_info["Proteina(g)"].replace(",", ".").replace("g", "")
            producto_info["Grasa(g)"] = producto_info["Grasa(g)"].replace(",", ".").replace("g", "")
            producto_info["Carbohidrato(g)"] = producto_info["Carbohidrato(g)"].replace(",", ".").replace("g", "")
            producto_info["Caloria(kcal)"] = producto_info["Caloria(kcal)"].replace("kcal", "")
            producto_info["Cantidad(g)"] = producto_info["Cantidad(g)"].split('(')[-1].replace(")", "").replace("g", "")
        
            result.append(producto_info)
        print(f"Extraccion completa de la página:{num_pagina}")
    
    Tabla_Nutricional_Productos = pd.DataFrame(result)
    Tabla_Nutricional_Productos["Caloria(kcal)"] = Tabla_Nutricional_Productos["Caloria(kcal)"].astype("Int64")
    Tabla_Nutricional_Productos["Grasa(g)"] = Tabla_Nutricional_Productos["Grasa(g)"].astype("Float64")
    Tabla_Nutricional_Productos["Carbohidrato(g)"] = Tabla_Nutricional_Productos["Carbohidrato(g)"].astype("Float64")
    Tabla_Nutricional_Productos["Proteina(g)"] = Tabla_Nutricional_Productos["Proteina(g)"].astype("Float64")

    return Tabla_Nutricional_Productos
