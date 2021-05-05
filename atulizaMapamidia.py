import pandas as pd
import json
import re


df = pd.read_json('arquivo.json')

df_dsName = df.distinguishedName

x = 0
name = []
while x < len(df_dsName):
    y = df_dsName[x].split(',')
    name.append(y)
    x = x + 1

name = pd.DataFrame(name)
name.columns = ['cn', 'cidade', 'setor', 'empresa', 'dc', 'dc', 'none']
name = name.drop(['dc', 'dc', 'none'], axis=1)

name['cn'] = name['cn'].map(lambda x: str(x)[3:])
name['cidade'] = name['cidade'].map(lambda x: str(x)[3:])
name['setor'] = name['setor'].map(lambda x: str(x)[3:])
name['empresa'] = name['empresa'].map(lambda x: str(x)[3:])

df = df.drop(['nome', 'nomeCompleto', 'distinguishedName', 'foto', 'gerente'], axis=1)

new_df = pd.concat([df, name], axis=1)

lista = []
lista2 = []
y = 0

for i in new_df.cidade:
    if re.search('\\bRádio\\b', i):
        x = str(i)[:-6]
        lista.append(x)
        lista2.append('Rádio')
    else:
        lista.append(i)
        lista2.append(new_df.empresa[y])
    y = y + 1

cidades = pd.DataFrame(lista)
cidades.columns = ['cidade']

empresas = pd.DataFrame(lista2)
empresas.columns = ['empresa']

new_df.cidade = cidades.cidade
new_df.empresa = empresas.empresa

new_df.columns = ['nomeUsuario', 'cargo', 'email', 'departamento', 'nomeCompleto', 'cidade', 'depDescricao', 'area']


def inseredadosNulos(data):
    lista = []
    for i in data:
        lista.append('None')
    dataframe = pd.DataFrame(lista)
    dataframe.columns = ['coluna']
    return dataframe.coluna


def insereDados(data, texto):
    lista = []
    x = 0
    for i in data['cargo']:
        if re.search('\\b{}\\b'.format(texto), i):
            lista.append(data['nomeCompleto'][x])
        else:
            lista.append(x)
        x = x + 1
    return lista


def insereDiretor(data, texto):
    lista = []
    for i in data:
        lista.append(texto)
    dataframe = pd.DataFrame(lista)
    dataframe.columns = ['coluna']
    return dataframe.coluna


def criaSubset(data, texto):
    df = data[data.depDescricao == '{}'.format(texto)]
    df = df.reset_index()
    df = df.drop(columns=['index'])
    return df


def criaSubsetVariante(data, texto):
    df = data[data.departamento == '{}'.format(texto)]
    df = df.reset_index()
    df = df.drop(columns=['index'])
    return df


# Tratamento dos cargos de Admin
admin = criaSubset(new_df, 'Administrativo')
admin['coordenador'] = inseredadosNulos(admin)
admin['gerente'] = inseredadosNulos(admin)
lista = insereDados(new_df, 'Diretor Administrativo e Financeiro')
admin['manager'] = admin.nomeCompleto.apply(lambda x: 'Diretor' if x in lista else 'None')
admin2 = admin.set_index('manager')
admin['diretor'] = admin.manager.apply(lambda x: admin2.nomeCompleto['Diretor'] if x != 'Diretor' else None)
admin = admin.drop(columns=['manager'])


# Tratamento dos cargos de programação
programacao = criaSubset(new_df, 'Programacao')
programacao['coordenador'] = inseredadosNulos(programacao)
programacao['gerente'] = inseredadosNulos(programacao)
lista = insereDados(programacao, 'Diretor')
programacao['manager'] = programacao.nomeCompleto.apply(lambda x: 'Diretor' if x in lista else 'None')
programacao2 = programacao.set_index('manager')
programacao['diretor'] = programacao.manager.apply(lambda x: programacao2.nomeCompleto['Diretor'] if x != 'Diretor' else None)
programacao = programacao.drop(columns=['manager'])


# Tratamento dos cargos de vendas
vendas = criaSubsetVariante(new_df, 'Comercial')
vendas['coordenador'] = inseredadosNulos(vendas)
vendas['gerente'] = inseredadosNulos(vendas)
vendas['diretor'] = insereDiretor(vendas, 'Ribeiro')


# Tratamento dos cargos de jornalismo
jornalismo = criaSubset(new_df, 'Jornalismo')
jornalismo['coordenador'] = inseredadosNulos(jornalismo)
jornalismo['gerente'] = inseredadosNulos(jornalismo)
lista = insereDados(jornalismo, 'Diretor de Jornalismo e Esporte')
jornalismo['manager'] = jornalismo.nomeCompleto.apply(lambda x: 'Diretor' if x in lista else 'None')
jornalismo2 = jornalismo.set_index('manager')
jornalismo['diretor'] = jornalismo.manager.apply(lambda x: jornalismo2.nomeCompleto['Diretor'] if x != 'Diretor' else None)
jornalismo = jornalismo.drop(columns=['manager'])


# Tratamento dos cargos de marketing
marketing = criaSubsetVariante(new_df, 'Marketing')
marketing['coordenador'] = inseredadosNulos(marketing)
marketing['gerente'] = inseredadosNulos(marketing)
marketing['diretor'] = insereDiretor(marketing, 'Antônio Alves (Tunico)')


# Tratamento dos cargos de engenharia
engenharia = criaSubset(new_df, 'Engenharia')
engenharia['coordenador'] = inseredadosNulos(engenharia)
engenharia['gerente'] = inseredadosNulos(engenharia)
lista = insereDados(engenharia, 'Diretor de Tecnologia')
engenharia['manager'] = engenharia.nomeCompleto.apply(lambda x: 'Diretor' if x in lista else 'None')
engenharia2 = engenharia.set_index('manager')
engenharia['diretor'] = engenharia.manager.apply(lambda x: engenharia2.nomeCompleto['Diretor'] if x != 'Diretor' else None)
engenharia = engenharia.drop(columns=['manager'])


# Tratamento dos cargos de RH
rh = criaSubset(new_df, 'Recursos Humanos')
lista = insereDados(rh, 'Coordenadora')
rh['manager2'] = rh.nomeCompleto.apply(lambda x: '{}'.format(x) if x in lista else 'None')

lista2 = []
for i in rh.manager2:
    if re.search('\\bNone\\b', i):
        continue
    else:
        lista2.append(i)

lista3 = []
for i in rh.manager2:
    if i == 'None':
        lista3.append(lista2)
    else:
        lista3.append('None')

coo = pd.DataFrame(lista3)
coo.columns=['col']
rh['coordenador'] = coo.col
rh = rh.drop(columns=['manager2'])
rh['gerente'] = inseredadosNulos(rh)
lista = insereDados(rh, 'Diretora')
rh['manager'] = rh.nomeCompleto.apply(lambda x: 'Diretora' if x in lista else 'None')
rh2 = rh.set_index('manager')
rh['diretor'] = rh.manager.apply(lambda x: rh2.nomeCompleto['Diretora'] if x != 'Diretora' else None)
rh = rh.drop(columns=['manager'])


# Tratamento dos cargos de OPEC
opec = criaSubset(new_df, 'Opec')
lista = insereDados(opec, 'Coordenadora')
opec['manager2'] = opec.nomeCompleto.apply(lambda x: '"{}"'.format(x) if x in lista else 'None')

lista2 = []
for i in opec.manager2:
    if re.search('\\bNone\\b', i):
        continue
    else:
        lista2.append(i)

lista3 = []
for i in opec.manager2:
    if i == 'None':
        lista3.append(lista2)
    else:
        lista3.append('None')

coo = pd.DataFrame(lista3)
coo.columns=['col1', 'col2', 'col3', 'col4']
opec['coordenador'] = pd.Series(coo.fillna('').values.tolist()).str.join(' ')
opec = opec.drop(columns=['manager2'])
lista = insereDados(opec, 'Gerente')
opec['manager'] = opec.nomeCompleto.apply(lambda x: 'Gerente' if x in lista else 'None')
opec2 = opec.set_index('manager')
opec['gerente'] = opec.manager.apply(lambda x: opec2.nomeCompleto['Gerente'] if x != 'Gerente' else None)
opec = opec.drop(columns=['manager'])
lista = insereDados(opec, 'Diretor')
opec['manager'] = opec.nomeCompleto.apply(lambda x: 'Diretor' if x in lista else 'None')
opec3 = opec.set_index('manager')
opec['diretor'] = opec.manager.apply(lambda x: opec3.nomeCompleto['Diretor'] if x != 'Diretor' else None)
opec = opec.drop(columns=['manager'])


# Tratamento dos cargos de TIC
tic = criaSubset(new_df, 'TIC')
lista = insereDados(tic, 'Coordenador')
tic['manager'] = tic.nomeCompleto.apply(lambda x: 'Coordenador' if x in lista else 'None')
tic3 = tic.set_index('manager')
tic['coordenador'] = tic.manager.apply(lambda x: tic3.nomeCompleto['Coordenador'] if x != 'Coordenador'  else None)
tic = tic.drop(columns=['manager'])
lista = insereDados(tic, 'Gerente')
tic['manager'] = tic.nomeCompleto.apply(lambda x: 'Gerente' if x in lista else 'None')
tic2 = tic.set_index('manager')
tic['gerente'] = tic.manager.apply(lambda x: tic2.nomeCompleto['Gerente'] if x != 'Gerente' else None)
tic = tic.drop(columns=['manager'])
tic['diretor'] = insereDiretor(tic, 'Luis Botelho')
tic['coordenador'][0] = 'None'


# Tratamentos dos cargos de negocios
negocios = criaSubsetVariante(new_df,'Negócios')
negocios['coordenador'] = inseredadosNulos(negocios)
negocios['gerente'] = inseredadosNulos(negocios)
lista = insereDados(negocios, 'Diretor')
negocios['manager'] = negocios.nomeCompleto.apply(lambda x: 'Diretor' if x in lista else 'None')
negocios2 = negocios.set_index('manager')
negocios['diretor'] = negocios.manager.apply(lambda x: negocios2.nomeCompleto['Diretor'] if x != 'Diretor' else None)
negocios = negocios.drop(columns=['manager'])


# Concatenando e gerando o arquivo json
dataframes = [admin, engenharia, jornalismo, marketing, negocios, opec, programacao, rh, tic, vendas]
chaves=['admin', 'engenharia', 'jornalismo', 'marketing', 'negocios', 'opec', 'programacao', 'rh', 'tic', 'vendas']
_df = pd.concat(dataframes, keys=chaves)

data = pd.DataFrame.to_json(_df, orient="index")
result = json.loads(data)
resultado = json.dumps(result, indent=4, ensure_ascii=False)

