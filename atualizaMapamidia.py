import os

url = 'https://api-ad-auth.irede.net/Usuario/GetAdUsers'

arquivo = os.system("curl -o 'arquivo.json' https://api-ad-auth.irede.net/Usuario/GetAdUsers")

#curl -o "arquivo-teste.json" https://api-ad-auth.irede.net/Usuario/GetAdUsers?carregarGerente=true -H "Accept: application/json"