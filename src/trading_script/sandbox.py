# Used for testing. Will not be in final product.
import requests

r = requests.get('http://127.0.0.1:8000/api/v1/trades/')

x = 5

y = f'x is equal to {x}'

print(y)
