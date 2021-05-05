import os

url = 'https://api-ad-auth.irede.net/Usuario/GetAdUsers'

arquivo = os.system("curl -o 'arquivo.json' {} -H 'Accept: application/json'".format(url))

#curl -o "arquivo-teste.json" https://api-ad-auth.irede.net/Usuario/GetAdUsers?carregarGerente=true -H "Accept: application/json"