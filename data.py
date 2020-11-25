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

#Connection to the data source server
login_session_object = openfoodfacts.utils.login_into_OFF()
print("Connecting...")
time.sleep(1)

#Creating the database
conn = sqlite3.connect('FoodProducts.sqlite')
cur = conn.cursor()
answer = input('Do you want to delete the existing Database? (yes or no): ')
if answer == 'yes':
    cur.execute('''DROP TABLE IF EXISTS Products''')
cur.execute('''CREATE TABLE IF NOT EXISTS Products
    (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT, brand TEXT, barcode INTEGER UNIQUE, countries TEXT, ingredient_tags TEXT)''')
    
#Reading the data and storing them to the database
id = None
count = 0
cur.execute('SELECT max(id) FROM Products')
try:
    row = cur.fetchone()
    if row is None :
        id = 1
    else:
        id = row[0]
except:
    id = 1
if id is None : id = 1

print('Waiting to find unretreived data...')
time.sleep(1)
for product in openfoodfacts.products.search_all({}):   
    try:
        name = product['product_name']
        brand = product['brands']
        barcode = product['code']
        countries = product['countries']
        intags = ''
        for tag in product['ingredients_analysis_tags']:
            intags += tag
            intags += ' ' 
    except:
        continue
    print('--------------------------------NEW PRODUCT--------------------------------')
    print(name, brand, '('+ barcode + ')')
    print('Countries: ', countries)
    print(intags, '\n')
    
   
    cur.execute('''INSERT OR IGNORE INTO Products (name, brand, barcode, countries, ingredient_tags)
        VALUES ( ?, ?, ?, ?, ?)''', (name, brand, barcode, countries, intags))
    count += 1
    if count % 50 == 0: 
        conn.commit()
    if count % 100 == 0 : 
        print('4 seconds pause')
        time.sleep(4)
    id += 1

conn.commit()
cur.close()



