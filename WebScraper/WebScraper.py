import requests
import pandas as pd
from bs4 import BeautifulSoup



def Scraper(url_):
    url_ = requests.get(url_).text
    pagsigSoup = BeautifulSoup(url_,"html.parser") 
    paginassiguiente = pagsigSoup.find("div", class_="searchResultsPaging")
    paginassiguiente = paginassiguiente.find_all("a")
    pagsig = []
    base_url = "https://www.fatsecret.com.ar"
    for link in paginassiguiente[1:-1]:
        pagsig.append(base_url + link['href'])

    Tabla_Nutricional_Productos = pd.DataFrame()
    
    for i in range(0,(len(pagsig))):
        url = pagsig[i]
        page = requests.get(url).text
        pageSoup = BeautifulSoup(page, "html.parser")
        tabla = pageSoup.find("td", class_="leftCell")
        # Encontrar todos los Nombres de Productos
        Productos = tabla.find_all("a",class_="prominent")
        Producto = []
        for caracter in Productos:
            Producto.append(caracter.text)
        Marcas = tabla.find_all("a",class_="brand")
        Marca = []
        for caracter in Marcas:
            marca_texto = caracter.text.replace("(", "").replace(")", "")
            Marca.append(marca_texto)

        # Check if there are as many brands as products
        if len(Marca) < len(Producto):
            # Append None for missing brands
            Marca += [None] * (len(Producto) - len(Marca))
        # Encontrar las cantidades
        Cantidades = tabla.find_all("div",class_="smallText greyText greyLink")
        Cantidad = []
        for caracter in Cantidades:
            cantidad_texto = caracter.text.replace("\r", "").replace("\n", "").replace("\t", "")
            cantidad_texto = cantidad_texto.split("-", 1)[0]
            Cantidad.append(cantidad_texto)
        # Encontrar las Calorias
        Calorias = tabla.find_all("div", class_="smallText greyText greyLink")
        Caloria = []
        for caracter in Calorias:
            calorias_texto = caracter.text.replace("\r", "").replace("\n", "").replace("\t", "")
            calorias_texto = calorias_texto.split("-", 1)[-1].split("|")[0].strip().replace("Calorías:", "")
            Caloria.append(calorias_texto.strip())
        # Encontrar las Grasas
        Grasas = tabla.find_all("div", class_="smallText greyText greyLink")
        Grasa = []
        for caracter in Grasas:
            grasas_texto = caracter.text.replace("\r", "").replace("\n", "").replace("\t", "")
            grasas_texto = grasas_texto.split("|", 1)[-1].split("|")[0].strip().replace("Grasa:", "")
            Grasa.append(grasas_texto.strip())
        # Encontrar los Carbohidratos
        Carbohidratos = tabla.find_all("div", class_="smallText greyText greyLink")
        Carbohidrato = []
        for caracter in Carbohidratos:
            carbohidratos_texto = caracter.text.replace("\r", "").replace("\n", "").replace("\t", "")
            carbohidratos_texto = carbohidratos_texto.split("|", 2)[-1].split("|")[0].strip().replace("Carbh:", "")
            Carbohidrato.append(carbohidratos_texto.strip())
        # Encontrar las Proteinas
        Proteinas = tabla.find_all("div", class_="smallText greyText greyLink")
        Proteina = []
        for caracter in Proteinas:
            proteinas_texto = caracter.text.replace("\r", "").replace("\n", "").replace("\t", "")
            proteinas_texto = proteinas_texto.split("|", 3)[-1].split("|")[0].strip().replace("Prot:", "")
            proteinas_texto = proteinas_texto.split("g", 1)[0] + "g"
            Proteina.append(proteinas_texto.strip())
        
        
        if not Tabla_Nutricional_Productos.empty:
            columnas = ["Producto","Marca","Cantidad","Caloria","Grasa","Carbohidrato","Proteina"]
            data_ = list(zip(Producto, Marca, Cantidad, Caloria, Grasa, Carbohidrato, Proteina))
            df = pd.DataFrame(columns=columnas,data=data_)
            Tabla_Nutricional_Productos = pd.concat([Tabla_Nutricional_Productos,df],ignore_index=True)
        else:
            columnas = ["Producto","Marca","Cantidad","Caloria","Grasa","Carbohidrato","Proteina"]
            data_ = list(zip(Producto, Marca, Cantidad, Caloria, Grasa, Carbohidrato, Proteina))
            Tabla_Nutricional_Productos = pd.DataFrame(columns= columnas,data=data_)
            
    return Tabla_Nutricional_Productos