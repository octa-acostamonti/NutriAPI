import requests
from bs4 import BeautifulSoup
import pandas as pd 




def extraer_info_nutricional(URLS: list):
    """ Extraction and Transformation Process of the Nutritional Facts. Asks for the a list of URLS"""

    result = [] # Initialize a empty list to store the results
    
    num_pagina=0 # Initialize a page counter for reference

    for url in URLS: 
       # Loop for each url in URLS list
       
        num_pagina += 1 # Sums 1 to the page counter

        page = requests.get(url) # Sends a request to the urls

        pagesoup = BeautifulSoup(page.content, "html.parser") # Parses to text the content of the url

        tabla = pagesoup.find("td", class_="leftCell") # The content we want to find is inside a table with the tag 'td', class 'leftCell'

        productos = tabla.find_all("a", class_="prominent") # The name of the products is in the tag 'a', class 'prominent'

        marcas = tabla.find_all("a", class_="brand") # The brand information is in the tag 'a', class 'brand'


        # The amount, calories, fat, carbs and protein are in the same tag and same class so, we only extract the info once

        nutritional_info = tabla.find_all("div", class_="smallText greyText greyLink")
        
        for producto, marca, info in zip(productos, marcas, nutritional_info):
            info_texto = info.text.replace("\r", "").replace("\n", "").replace("\t", "") # replace unnecesary text
            info_partes = info_texto.split("|") # split categories by '|'

            # We map the information into a dictionary and clean the data to get correct datatypes
            producto_info = {
                "Producto": producto.text,
                "Marca": marca.text.replace("(", "").replace(")", "") if len(marca.text) > 0 else None,
                "Cantidad(g)": info_partes[0].replace("\r", "").replace("\n", "").replace("\t", "").split("-", 1)[0],
                "Caloria(kcal)": info_partes[0].replace("\r", "").replace("\n", "").replace("\t", "").split("-", 1)[-1].split("|")[0].strip().replace("Calorías:", "").strip(),
                "Grasa(g)": info_partes[1].replace("\r", "").replace("\n", "").replace("\t", "").split("|", 1)[-1].split("|")[0].strip().replace("Grasa:", "").strip(),
                "Carbohidrato(g)": info_partes[2].replace("\r", "").replace("\n", "").replace("\t", "").split("|", 2)[-1].split("|")[0].strip().replace("Carbh:", "").strip(),
                "Proteina(g)": info_partes[3].replace("\r", "").replace("\n", "").replace("\t", "").split("|", 3)[-1].split("|")[0].strip().replace("Prot:", "").split("g", 1)[0].strip()
            }
            
            # We further clean the rows to get the correct dtypes

            producto_info["Proteina(g)"] = producto_info["Proteina(g)"].replace(",", ".").replace("g", "")
            producto_info["Grasa(g)"] = producto_info["Grasa(g)"].replace(",", ".").replace("g", "")
            producto_info["Carbohidrato(g)"] = producto_info["Carbohidrato(g)"].replace(",", ".").replace("g", "")
            producto_info["Caloria(kcal)"] = producto_info["Caloria(kcal)"].replace("kcal", "")
            producto_info["Cantidad(g)"] = producto_info["Cantidad(g)"].split('(')[-1].replace(")", "").replace("g", "")
            
            # we append the data into the list we innitialize in the begginig
            result.append(producto_info)

        # print the extraction page for reference
        print(f"Extraccion completa de la página:{num_pagina}")
    
    # We ingest the data into a Pandas DataFrame
    Tabla_Nutricional_Productos = pd.DataFrame(result)

    # Transform columns datatypes
    Tabla_Nutricional_Productos["Caloria(kcal)"] = Tabla_Nutricional_Productos["Caloria(kcal)"].astype("Int64")
    Tabla_Nutricional_Productos[["Grasa(g)","Carbohidrato(g)","Proteina(g)"]] = Tabla_Nutricional_Productos[["Grasa(g)","Carbohidrato(g)","Proteina(g)"]].astype("Float64")
    
    # return the dataframe
    return Tabla_Nutricional_Productos
