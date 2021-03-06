# -*- coding: utf-8 -*-
"""TratamentoDeDados_Pandas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1WWTXf7I0KPJRbxMKQcIojnvYIbBktkhS
"""

import pandas as pd

"""# **Leitura de Arquivos**

## Arquivos CSV e TXT

pd.read_csv('nome_do_arquivo.extensao', sep = 'caracter que sepada os dados', skiprows = numero de linhas a serem puladas)
"""

df_materiais = pd.read_csv('materiais.csv',sep=';')

df_pedidos = pd.read_csv('pedidos.txt',sep='|',skiprows=2, encoding = 'latin-1')

"""## Arquivos XLSX

pd.read_excel('nome_do_arquivo.extensao', sheet_name='nome da aba', skiprows = numero de linhas a serem puladas)
"""

df_vendas1 = pd.read_excel('vendas_1.xlsx',sheet_name='vendas')

df_vendas2 = pd.read_excel('vendas_2.xlsx',sheet_name='vendas')

"""# **Tratamento de Dados**

## Renomeando colunas

df.rename(columns={'coluna_antiga':'coluna_nova', 'coluna_antiga2': 'coluna_nova2'})
"""

df_materiais = df_materiais.rename(columns = {'Material':'material','Texto breve material':'texto_breve'})

"""df.columns = ['coluna_nova','coluna_nova2',...]"""

df_pedidos.columns = ['fornecedor','material','qtd_pedido','texto_breve','qtd_estoque']

df_vendas1.columns = ['data','material','qtd_vendas']

df_vendas2.columns = ['data','material','qtd_vendas']

"""## Verificar tipos de dados

### Verificar tipos

df.dtypes
| df['coluna'].dtype
"""

df_materiais.dtypes

df_pedidos.dtypes

df_vendas1.dtypes

df_vendas2.dtypes

"""### Alterando tipode de uma coluna

df['coluna'].astype() (int ou float ou str)
"""

df_pedidos['qtd_pedido'] = df_pedidos['qtd_pedido'].astype(int)

"""## Eliminando Dados

df.drop(['coluna2','coluna3'],axis='columns')

df.drop([1,2],axis='index')
"""

df_materiais = df_materiais.drop(['texto_breve'],axis='columns')

"""df[['coluna2','coluna1']].copy()"""

df_pedidos = df_pedidos[['material','qtd_pedido','qtd_estoque']].copy()

df_vendas1 = df_vendas1[['material','qtd_vendas']].copy()

df_vendas2 = df_vendas2[['material','qtd_vendas']].copy()

"""# Concatenar tabelas (Juntar tabelas)"""

df_vendas1.dtypes

df_vendas2.dtypes

"""pd.concat([df_vendas1,df_vendas2])"""

df_vendas1.shape

df_vendas2.shape

df_vendas = pd.concat([df_vendas1,df_vendas2])

df_vendas = df_vendas.reset_index(drop=True)

"""# **Correlação de Tabelas**

## Agrupamento de dados

df.groupby(['colunas a serem agrupadas']).agg({'coluna1':'sum','coluna2':'mean','coluna3':'max', 'coluna4':'min','coluna5':'first'}).reset_index()

1. lista = [colunas a serem agrupadas]
2. dict = {'coluna_x':'funcao'}

Agora para aqueles materiais(linhas) iguais  que estao se repetindo após a concatenação, vamos somar os seus valores e tranformar em unico registro (linha).

Vamos usar o **groupby** para agrupar e **sum** para somar
"""

df_pedidos = df_pedidos.groupby(['material']).agg({'qtd_pedido':'sum','qtd_estoque':'sum'}).reset_index()

df_vendas = df_vendas.groupby(['material']).agg({'qtd_vendas':'sum'}).reset_index()

df_vendas.head()

"""## Merge de tabelas

Utilizado para unir duas tabelas através de uma ou
mais colunas em comum

pd.merge(df_tabela_esquerda,df_tabela_direita, on=['colunas em comum'], how='método de correlação (priorização')

how poder ser: left (esquerda), rigth (direita), inner (apenas itens em comum), outer (todos os itens)
"""

df_relatorio = pd.merge(df_materiais,df_pedidos, on=['material'], how='left')

df_relatorio = pd.merge(df_relatorio,df_vendas, on=['material'], how='left')

"""### Tratando o pós merge

df.fillna(qualquer valor para substituir os NaN)

df['coluna'] = df['coluna'].fillna(qualquer valor para substituir os NaN)
"""

df_relatorio.head(3)

df_relatorio = df_relatorio.fillna(0)

df_relatorio.head(2)

df_relatorio[['qtd_pedido','qtd_estoque','qtd_vendas']] = df_relatorio[['qtd_pedido','qtd_estoque','qtd_vendas']].astype(int)

"""# **Regra de Negócio**

## Operações entre colunas (sem condicional)
"""

df_relatorio['qtd_loja'] = df_relatorio['qtd_pedido'] + df_relatorio['qtd_estoque']

df_relatorio = df_relatorio[['material','qtd_loja','qtd_vendas']].copy()

"""## Operações entre colunas (com condicional)"""

def calcular_porcentagem(loja,vendas):
  if (vendas!=0):
    porcentagem = loja/vendas
    return porcentagem
  elif ((vendas==0) and (loja!=0)):
    return 1.2
  else:
    return 0

"""A partir dessa função vamos criar uma nova coluna, a coluna porcentagem. E para aplicar a função para todas as linhas do df_relatorio vamos usar lambda.

df.apply(lambda row: funcao(row['coluna_x'] (paramêtro) ,row['coluna_y'] (paramêtro), axis='columns')
"""

df_relatorio['porcentagem'] = df_relatorio.apply(lambda row: calcular_porcentagem(row['qtd_loja'],row['qtd_vendas']), axis='columns')

"""O **row** serve para aplicar a coluna que deve ser passada como paramêtro para a função que criamos, **calcular_porcentagem**

Agora vamos criar uma nova coluna, a coluna status. Também vamos usar lambda p/ aplicar a função de status que vamos criar p/ todas as linhas do df_relatorio.
"""

def verificar_status(porc):
  if (porc>=1.2):
    return 'alerta'
  else:
    return ''

df_relatorio['status'] = df_relatorio.apply(lambda row: verificar_status(row['porcentagem']), axis='columns')

"""Veja que aqui só usamos uma coluna, porque a nossa função status só utiliza um paramêtro. Entao só passamos uma coluna como paramêtro.

# **Filtro de dados**

df[(condicao do filtro)]

and - &
or - |

Vamos filtrar, visualizar apenas os valores da coluna status que sejam diferentes de alerta e (and) e os valores em que a coluna de loja sejam diferentes de  0.
"""

# Apenas para visualizar possibilidade

df_relatorio[(df_relatorio['status']!='alerta') & (df_relatorio['qtd_loja']!=0)].head(5)

"""# **Ordenar dados**

df.sort_values([colunas a serem ordenadas], ascending=True) - crescente

df.sort_values([colunas a serem ordenadas], ascending=False) - decrescente
"""

# Apenas para visualizar possibilidade

df_relatorio.sort_values(['qtd_loja'], ascending=False)

"""# **Exportanto Dados**

df.to_csv('nome_do_arquivo.csv', sep='caracter para separar os dados', index=False)
"""

df_relatorio.to_csv('Relatório_Final.csv',sep=';',index=False)

"""Vamos agora exportar para excel, o tipo de exportação mais utilizado

writer = pd.ExcelWriter('Relatório Final.xlsx')

df.to_excel(writer, sheet_name='nome_aba1', index=False)
df.to_excel(writer, sheet_name='nome_aba2',index=False)

writer.save()
"""

writer = pd.ExcelWriter('Relatório Final.xlsx')

df_relatorio.to_excel(writer, sheet_name='relatorio', index=False)

writer.save()

"""O index = False retira o index do nosso arquivo em excel

Podemos colocar um executavel do python em uma mesma pasta com os arquivos que foram utilizados para criar nosso conjunto de dados. Assim poderiamos alterar os arquivos e ao dar dois cliques no executavel (esse notebook que criamos) ele já atualiza um novo conjunto de dados.
"""