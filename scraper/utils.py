def conseguir_urls():
    """ Conseguir las URLS de la página fatsecret.com.ar y almacenarlas en una lista """
    
    URLS = []
    
    URL_BASE = "https://www.fatsecret.com.ar/calor%C3%ADas-nutrici%C3%B3n/search?q=9+de+Oro&pg=" 

    for num in range(0,271): # '271' es el numero maximo de páginas de la URL BASE

        URL = URL_BASE + str(num) 
        URLS.append(URL) 
    return URLS