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
count = 0
count_new = 0
count_old = 0
try:
    numOfProducts = int(input('Number of products to retreive: '))
except:
    print('Number of products set to 20000')
    numOfProducts = 20000
    time.sleep(5)
print('Checking the already retreived data...')
time.sleep(1)
for product in openfoodfacts.products.search_all({}): 
    #programm exits if the number of products we want to retreive has been reached
    if count == numOfProducts: 
        print('I retreived: ', count_new, 'products!')
        print(count_old, 'products already existed!')
        quit() 
    #getting some values of a specific product
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
    #check if the product already exists, if yes then skip to the next
    cur.execute('''SELECT name FROM Products WHERE barcode = (?) ''', (barcode,))
    try:
        row = cur.fetchone()
        if row is not None : 
            print('Product already retreived!')
            count += 1
            count_old += 1
            continue
    except:
        row = None
    #print the values
    print('--------------------------------NEW PRODUCT--------------------------------')
    print(name, brand, '('+ barcode + ')')
    print('Countries: ', countries)
    print(intags, '\n')
    #store the values in the database
    cur.execute('''INSERT OR IGNORE INTO Products (name, brand, barcode, countries, ingredient_tags)
        VALUES ( ?, ?, ?, ?, ?)''', (name, brand, barcode, countries, intags))
    count += 1
    count_new += 1
    #commit every 50 rounds, pause for every 100 rounds
    if count % 50 == 0: 
        conn.commit()
    if count % 100 == 0 : 
        print('4 seconds pause')
        print('Remaining new products to retreive: ', (numOfProducts - count))
        time.sleep(4)

conn.commit()
cur.close()



