# This will be the Log of the changes I make


21/4/2023

Added nutri.ipynb 
Deleted aaa.ipynb

Scraper_v3 coming soon...

22/4/2023

Scraper_v3 added.

The feature that was added is that the optimal page to search for the maximum amount of products is 7, or pg=6 in the HTML code. But you can only access to page 6,or pg=5 in the main product page. So the code looks if the product page has a pg=6(this is done by searching if the page has de NoResult tag/class) and if dont, it searches the max page the product has. i.e: vinagre has a maximum page of 2. So it first checks for the pg=6, (page 7), and then it looks for its max page. Then it scrapes normally.
