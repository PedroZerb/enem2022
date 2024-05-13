#
#
# Base de dados de pinguins do Ártico:
# Estudo Dra. Palmer, 2001
# Base de Dados no Github:
# https://gist.github.com/slopp/ce3b90b9168f2f921784de84fa445651
#
# Artigo:
# https://lauranavarroviz.wordpress.com/2020/08/01/palmer-penguins/

#v4: acréscimos em relação a versão v3:
# 1: permite o usuário selecionar qualquer número de espécies de pinguim para análise de correlação

# Importando bibliotecas
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Título
st.title('Análise de dados do ENEM de 2022')

# Subtítulo
st.markdown("Utilize este App e construa suas próprias análises de dados!")

st.subheader('Gráfico de dispersão')

selecao_opcao = st.sidebar.multiselect('Selecione os estados', ['AC','CE','DF','ES','GO','MA','MG','MS','MT','PA','PB','PE','PI','PR','RJ','RN','RO','RR','RS','SC','SE','SP'], default='AC')

print(type(selecao_opcao), selecao_opcao)
selecao_var_x = st.selectbox('Selecione a variável para o eixo X', ['NOTA CIÊNCIAS DA NATUREZA','NOTA CIÊNCIAS HUMANAS','NOTA LINGUAGENS E CÓDIGOS','NOTA MATEMÁTICA', 'NOTA REDACÃO', 'NOTA TOTAL'])

selecao_var_y = st.selectbox('Selecione a variável para o eixo Y', ['NOTA CIÊNCIAS DA NATUREZA','NOTA CIÊNCIAS HUMANAS','NOTA LINGUAGENS E CÓDIGOS','NOTA MATEMÁTICA', 'NOTA REDACÃO', 'NOTA TOTAL'])

visualizar_toda_escala = st.checkbox('Visualizar toda a escala do gráfico')

# lendo o arquivo de dados penguins.csv
df = pd.read_csv('PlanilhaEnemCorreta.csv')

# A função plt.subplots () sem parâmetros retorna uma figura e um eixo. A fig e o ax retornados são atribuídos a variáveis fig e ax, respectivamente.

# A variável fig é um objeto de figura. A figura é a imagem final que pode conter um ou mais eixos. Você pode pensar na figura como um contêiner que contém esses eixos.

# A variável ax é um objeto de eixos. Um objeto de eixos é um gráfico individual com um eixo x, um eixo y e o espaço onde você pode desenhar linhas ou pontos.

# Após essa linha, você pode usar o objeto ax para desenhar gráficos, definir rótulos, etc. e usar o objeto fig para salvar a figura em um arquivo, alterar o tamanho da figura e assim por diante.


# criando um gráfico de dispersão
fig, ax = plt.subplots()
for sel_epc in selecao_opcao:
    df1 = df[df.SG_UF_PROVA == sel_epc]
    ax.scatter(df1[selecao_var_x], df1[selecao_var_y], alpha=0.8)
if visualizar_toda_escala:
    ax.set_xlim(0, 1.1*df[selecao_var_x].max())
    ax.set_ylim(0, 1.1*df[selecao_var_y].max())
ax.set_xlabel(selecao_var_x)
ax.set_ylabel(selecao_var_y) 
ax.legend(selecao_opcao)   
ax.grid(True)

ax.set_title(f'Dispersão {selecao_var_x} x {selecao_var_y} para os estados:'+' '.join(selecao_opcao))
# Fixed the issue by closing the opening parenthesis in the set_title function call.
st.pyplot(fig)


st.header('Gráfico de barras')

selecao_var_barra_x = st.selectbox('Selecione a variável para o eixo X', ['FAIXA ETÁRIA','SEXO','COR OU RACA','SITUACÃO DE CONCLUSÃO','ANO QUE CONCLUIU','ESCOLA,ENSINO','ESTADO DA ESCOLA','DEPENDÊNCIA ADM DA ESCOLA',
'LOCALIZACAO DA ESCOLA', 'PRESENCA CIÊNCIAS DA NATUREZA','PRESENCA CIÊNCIAS HUMANAS','PRESENCA LINGUAGENS E CÓDIGOS','PRESENCA MATEMÁTICA','CÓDIGO DA PROVA CIÊNCIAS DA NATUREZA',
'CÓDIGO DA PROVA CIÊNCIAS HUMANAS','CÓDIGO DA PROVA LINGUAGENS E CÓDIGOS','CÓDIGO DA PROVA MATEMÁTICA','LÍNGUA ESTRANGEIRA','STATUS DA REDACÃO', 'FAIXA SALARIAL', 'POSSUI INTERNET EM CASA'])

selecao_var_barra_y = st.selectbox('Selecione a variável para o eixo Y', ['NOTA CIÊNCIAS DA NATUREZA','NOTA CIÊNCIAS HUMANAS','NOTA LINGUAGENS E CÓDIGOS','NOTA MATEMÁTICA','NOTA TOTAL', 'NOTA REDACÃO'])

# Filtrando o DataFrame com base na seleção em selecao_opcao
df_filtrado = df[df['SG_UF_PROVA'].isin(selecao_opcao)]

# Criando um gráfico de barras
fig, ax = plt.subplots()

# Agrupando os dados filtrados pelo selecao_var_barra_x e calculando a média do selecao_var_barra_y
grouped_data = df_filtrado.groupby(selecao_var_barra_x)[selecao_var_barra_y].mean()

# Plotando o gráfico de barras
grouped_data.plot(kind='bar', ax=ax)

# Adicionando rótulos e título
ax.set_xlabel(selecao_var_barra_x)
ax.set_ylabel(selecao_var_barra_y)
ax.set_title(f'Média de {selecao_var_barra_y} por {selecao_var_barra_x} pelo(s) estado(s) '+' '.join(selecao_opcao))

# Mostrando o gráfico
st.pyplot(fig)