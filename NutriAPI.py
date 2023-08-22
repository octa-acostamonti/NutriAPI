import requests
import pandas as pd
from bs4 import BeautifulSoup


URLS = []

URL_BASE = "https://www.fatsecret.com.ar/calor%C3%ADas-nutrici%C3%B3n/search?q=9+de+Oro&pg=" 


for num in range(0,271):

    URL = URL_BASE + str(num) 
    URLS.append(URL) 


Tabla_Nutricional_Productos = pd.DataFrame()


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
        
        # Chequear si se puede mejorar este codigo. La 'class_' es la misma para las 4 propiedades, por lo que quiza pueda hacer algo como:
        """ 
        Productos = tabla.find_all('div',class_='smallText greyText greyLink')
        
        Cantidades = [cantidad.text.replace(...) for cantidad in Productos]

        Calorias = [caloria.text.replace(...) for caloria in Productos]

        Grasas = [grasa.text.replace(...) for grasa in Productos]

        Carbohidratos = [carbohidrato.text.replace(...) for carbohidrato in Productos]

        Proteinas = [proteina.text.replace(...) for proteina in Productos]
        
        """

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


        if not Tabla_Nutricional_Productos.empty:
            columnas = ["Producto","Marca","Cantidad(g)","Caloria(kcal)","Grasa(g)","Carbohidrato(g)","Proteina(g)"]
            data_ = list(zip(Producto, Marca, Cantidad, Caloria, Grasa, Carbohidrato, Proteina))
            df = pd.DataFrame(columns=columnas,data=data_)
            Tabla_Nutricional_Productos = pd.concat([Tabla_Nutricional_Productos,df],ignore_index=True)
        else:
            columnas = ["Producto","Marca","Cantidad(g)","Caloria(kcal)","Grasa(g)","Carbohidrato(g)","Proteina(g)"]
            data_ = list(zip(Producto, Marca, Cantidad, Caloria, Grasa, Carbohidrato, Proteina))
            Tabla_Nutricional_Productos = pd.DataFrame(columns=columnas,data=data_)

    
    print(Tabla_Nutricional_Productos.head(4))
    Tabla_Nutricional_Productos["Caloria(kcal)"] = Tabla_Nutricional_Productos["Caloria(kcal)"].astype("Int64")
    Tabla_Nutricional_Productos["Grasa(g)"] = Tabla_Nutricional_Productos["Grasa(g)"].astype("Float64")
    Tabla_Nutricional_Productos["Carbohidrato(g)"] = Tabla_Nutricional_Productos["Carbohidrato(g)"].astype("Float64")
    Tabla_Nutricional_Productos["Proteina(g)"] = Tabla_Nutricional_Productos["Proteina(g)"].astype("Float64")
    print(Tabla_Nutricional_Productos.head(4))
    return Tabla_Nutricional_Productos.to_csv("Tabla_Nutricional_Productos.csv")


if __name__ == "__main__":
    main()


