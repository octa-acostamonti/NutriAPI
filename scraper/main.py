from carga import carga
from extraer import extraer_info_nutricional
from utils import conseguir_urls
from cProfile import Profile



def main():
    """ Main loop for the scraper """

    import pstats

    with Profile() as pr:
        

    
        URLS = conseguir_urls() # Gets a list of all the URLS to scrape

        Tabla_Nutricional_Productos = extraer_info_nutricional(URLS) # Scrapes the URLS and gets the Nutritional Information and stores it into a Pandas DataFrame
    
        carga("productos",Tabla_Nutricional_Productos) # Creates a conection with the table "productos" in PostreSQL, and loads the Pandas DataFrame

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.dump_stats(filename='stats.prof')


if __name__ == "__main__":
    main()

    