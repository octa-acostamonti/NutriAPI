def conseguir_urls():
    """ Get all of the pages of the page fatsecret.com.ar and append them into a list """
    
    URLS = []
    
    URL_BASE = "https://www.fatsecret.com.ar/calor%C3%ADas-nutrici%C3%B3n/search?q=9+de+Oro&pg=" 

    for num in range(0,276): # '276' is the max page on fatsecret.com.ar

        URL = URL_BASE + str(num) 
        URLS.append(URL) 
    return URLS