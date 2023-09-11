from carga import carga
from extraer import extraer_info_nutricional
from utils import conseguir_urls




def main():
    """ Main loop for the scraper """
    
    URLS = conseguir_urls() # Gets a list of all the URLS to scrape

    Tabla_Nutricional_Productos = extraer_info_nutricional(URLS) # Scrapes the URLS and gets the Nutritional Information and stores it into a Pandas DataFrame
    
    carga("productos",Tabla_Nutricional_Productos) # Creates a conection with the table "productos" in PostreSQL, and loads the Pandas DataFrame


if __name__ == "__main__":
    main()