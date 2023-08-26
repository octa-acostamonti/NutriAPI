from carga import carga
from extraer import extraer_info_nutricional
from utils import conseguir_urls

def main():
    
    URLS = conseguir_urls()
    info_extraeida = extraer_info_nutricional(URLS)
    carga("productos",info_extraeida)


if __name__ == "__main__":
    main()
    


