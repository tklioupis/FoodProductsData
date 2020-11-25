'''
FoodProductsData project for Python For Everybody Online Course!

Theodoros Lioupis
tklioupis@gmail.com
https://github.com/tklioupis
https://www.linkedin.com/in/theodoros-lioupis-2225621a9/
'''

import openfoodfacts
import sqlite3
import time

#Creating the database
conn = sqlite3.connect('FoodProducts.sqlite')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Products
    (id INTEGER UNIQUE, name TEXT, brand TEXT, barcode INTEGER UNIQUE)''')

#Connection to the data source server
login_session_object = openfoodfacts.utils.login_into_OFF()
print("Connecting...")
time.sleep(3)
    
#Reading the data and storing them to the database
for product in openfoodfacts.products.search_all({}):
    #print(product.keys())
    #break
    try:
        name = product['product_name']
        brand = product['brands']
        barcode = product['code']
        countries = product['countries']
        intags = product['ingredients_analysis_tags']
    except:
        continue
    print('--------------------------------NEW PRODUCT--------------------------------')
    print(name, brand, '('+ barcode + ')')
    print('Countries: ', countries)
    print(intags, '\n')


