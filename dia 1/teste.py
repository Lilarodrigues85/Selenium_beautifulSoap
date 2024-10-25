import requests

response = requests.get('https://www.google.com/')

print('Status code:', response.status_code)
print(response.headers)

print(response.content)