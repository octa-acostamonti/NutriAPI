# NutriScraper
NutriScraper is a Python web scraper that extracts nutritional information of food products from the website FatSecret.com.ar. It retrieves data such as product name, brand, serving size, calories, fat, carbohydrates, and protein. The scraper can extract data from multiple pages and consolidate the information into a single Pandas DataFrame.

### USAGE
To use NutriScraper, clone this repository and install the required packages using pip.
```

import pandas as pd

from NutriScraper import Scraper

url = "https://www.fatsecret.com.ar/calor%C3%ADas-nutrici%C3%B3n/search?q=leche"
data = Scraper(url)

print(data.head())


```
The output should be a Pandas DataFrame with the nutritional information of the food products found in the search results.

"As of now, it only works with the page 'FatSecret.com.ar.' This is because my objective is to create a complete DataFrame filled with all the products and their corresponding nutritional facts, and then analyze the best products in terms of price, protein, and carbohydrates."


I am constantly working on this project. My idea is to make a full Data Engineer, Data Analytic, Data Science and Machine Learning Project. This will take a long time so I will keep you updated everytime I make progress. : )
