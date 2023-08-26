import requests
import pandas as pd
from bs4 import BeautifulSoup
from carga_datos import carga

Tabla_Nutricional_Productos = pd.DataFrame()

def conseguir_urls():
    """ Conseguir las URLS de la página fatsecret.com.ar y almacenarlas en una lista """
    
    URLS = []
    
    URL_BASE = "https://www.fatsecret.com.ar/calor%C3%ADas-nutrici%C3%B3n/search?q=9+de+Oro&pg=" 

    for num in range(0,271): # '271' es el numero maximo de páginas de la URL BASE

        URL = URL_BASE + str(num) 
        URLS.append(URL) 
    return URLS

def extraer_info_nutricional(URLS):
    todos_productos = []
    for url in URLS:
        page = requests.get(url)
        pagesoup = BeautifulSoup(page.content,"html.parser")
        tabla = pagesoup.find("td",class_="leftCell")

        productos = tabla.find_all("div",class_="smallText greyText greyLink")
        todos_productos.extend(productos)
        return todos_productos
    

def main():
    global Tabla_Nutricional_Productos
    
    URLS = conseguir_urls()
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

        Proteina = [p.replace(",", ".").replace("g", "") for p in Proteina]
        Grasa = [g.replace(",", ".").replace("g", "") for g in Grasa]
        Carbohidrato = [c.replace(",", ".").replace("g", "") for c in Carbohidrato]
        Caloria = [c.replace("kcal", "") for c in Caloria]
        Cantidad = [c.split('(')[-1].replace(")", "").replace("g", "") for c in Cantidad]
        

        if Tabla_Nutricional_Productos.empty:
        # Si no existe; Crear el DataFrame con las columnas pertinentes.
            columnas = ["Producto","Marca","Cantidad(g)","Caloria(kcal)","Grasa(g)","Carbohidrato(g)","Proteina(g)"]
            data_ = list(zip(Producto, Marca, Cantidad, Caloria, Grasa, Carbohidrato, Proteina))
            Tabla_Nutricional_Productos = pd.DataFrame(columns=columnas, data=data_)
            print("Creado el DataFrame")
        else:
        # Una vez existe; Ingestar la data al DataFrame ya creado.
            new_data = list(zip(Producto, Marca, Cantidad, Caloria, Grasa, Carbohidrato, Proteina))
            new_df = pd.DataFrame(columns=Tabla_Nutricional_Productos.columns, data=new_data)
            Tabla_Nutricional_Productos = pd.concat([Tabla_Nutricional_Productos, new_df], ignore_index=True)
            print("Data Ingestada")

    Tabla_Nutricional_Productos["Caloria(kcal)"] = Tabla_Nutricional_Productos["Caloria(kcal)"].astype("Int64")
    Tabla_Nutricional_Productos["Grasa(g)"] = Tabla_Nutricional_Productos["Grasa(g)"].astype("Float64")
    Tabla_Nutricional_Productos["Carbohidrato(g)"] = Tabla_Nutricional_Productos["Carbohidrato(g)"].astype("Float64")
    Tabla_Nutricional_Productos["Proteina(g)"] = Tabla_Nutricional_Productos["Proteina(g)"].astype("Float64")
    carga("productos",Tabla_Nutricional_Productos)

    return Tabla_Nutricional_Productos.to_csv("Tabla_Nutricional_Productos.csv")


if __name__ == "__main__":
    main()
    


