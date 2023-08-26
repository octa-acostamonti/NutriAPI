# LOG

21/4/2023

* Added nutri.ipynb 
* Deleted aaa.ipynb

* Scraper_v3 coming soon...

22/4/2023

* Scraper_v3 added.

The feature that was added is that the optimal page to search for the maximum amount of products is 7, or pg=6 in the HTML code. But you can only access to page 6,or pg=5 in the main product page. So the code looks if the product page has a pg=6(this is done by searching if the page has de NoResult tag/class) and if doesnt, it searches the max page the product has. i.e: vinagre has a maximum page of 2. So it first checks for the pg=6, (page 7), and then it looks for itss max page. Then it scrapes normally.


25/04/2023

* Added a Notebook file where im conducting some analysis on the results im getting as it for now, and where Im conducting some normalization of the data.

28/4/2023

Started learning about Selenium. Theres a dropdown menu on the Carrefour web page that doesnt let me excract with BS4 the data. I want to extract the name of the elements in the dropdown menu to then search them and extract each product name and its price. The product name will then be searched in the fatsecret.com web page, and then it will be added to the Pandas DataFrame and listed with its respective price.


5/5/2023

I found what I think is a bug in "fatsecret.com.ar". I had this problem where I had to enter every category of product I wanted to scrape, but due to how the database of the page was made, generally speaking, the items appeared to be pretty "random" or not labeled correctly. So for days I was able to extract only between 600 and 700 products. Today I found a section of the page that is supposedly of a brand (the brand is real) but had what I think is every or almost every item on their database. So I scraped that section of the page and got 2701 products. This is a huge improvment towards the goal.

8/8/2023

* Eliminated the two folders that contained the .py,.ipynb and CSVs files
* Added the new NutriAPI notebook
* Added the new NutriAPI.py File
* Added the new Tabla_Nutricion_Productos CSV file

All of this changes were comitted to enhance the code and put into action better coding practices.

16/8/2023

Started with the creation of the API using the Python framework FastAPI.

* Added app folder 
* Created main.py file 
* Created __init__.py file

17/8/2023

I added a normalization part to the code so that the outputed CSV has clear datatypes.

* Modified NutriAPI.py with the normalization code
* Modified NutriAPI.ipynb, where I practiced the code to clean the rows
* The CSV got modified due to the changes in the code

18/8/2023

Modified README to later explain the API

19/8/2023

* Added database.py to the app folder
* Added models.py to the app folder
* Modified main.py file in the app folder

database.py:
   * Creates the connection to the PostgreSQL database that contains the information of the products for the API

models.py:
   * Creates the models of the tables that are hosted in PostgreSQL for the API

main.py changes: 
   * Created a connection with the PostgreSQL that contains the information of the products for the API 
   * Created the dependency to call the database when requested 
   * Created the "proteinas" endpoint which gives: "producto", "marca", "proteina" and "cantidad" 
   * Created the "grasas" endpoint which gives: "producto", "marca", "grasa" and "cantidad" 
   * Created the "carbohidratos" endpoint which gives: "producto", "marca", "carbohidrato" and "cantidad" 
   * Created the "productos" endpoint which gives: "id","producto", "marca", "cantidad" ,"grasa", "carbohidratos" and "proteina" 
   * Created the "sqlalchemytest" endpoint which is a test for the conection to the database 

20/8/2023

* Added schemas.py to the app folder
* Modified models.py to better fit constrains
* Modified the response of the endpoints using the schemas.py file

23/8/2023

* Added config.py file
* Modified database.py using config.py
* Modified .gitignore

25/8/2023

* Added scraper folder
* Moved NutriAPI.py, NutriAPI.ipynb and Tabla_Nutricional_Productos.csv to scraper folder
* Added carga_datos.py

carga_datos.py:
   * Generates a conection to PostreSQL
   * Has a function to conect to the database and upload the data automaticly
