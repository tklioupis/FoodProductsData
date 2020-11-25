import openfoodfacts

login_session_object = openfoodfacts.utils.login_into_OFF()

for product in openfoodfacts.products.search_all({}):
    try:
        print('--------------------------------------------------------------------------')
        print (product['product_name'])
        print(product['brands'])
        print('--------------------------------------------------------------------------')
    except:
        continue


