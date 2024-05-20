import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# print (plt.__version__)
# print (pd.__version__)

# Abrindo o arquivo de dados
enem_data=pd.read_csv('MICRODADOS_ENEM_2022 - Copia.csv', sep=',', encoding='latin-1')

#---------------------------------------------------TIRANDO OS OUTLIERS DAS NOTAS-------------------------------------------------------------------------------------------------------------------------

# nlinhas = len(enem_data)

# print(f"O arquivo tem {nlinhas} linhas.")

# colunas_vazias = ['NU_NOTA_REDACAO']

# colunas_media = ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT','NU_NOTA_REDACAO']

# enem_data.dropna(subset=colunas_vazias, inplace=True)

# nlinhas = len(enem_data)

# print(f"O arquivo tem {nlinhas} linhas.")

# enem_data.to_csv('MICRODADOS_ENEM_2022 - Copia.csv', index=False)

#----------------------------------------------------CRIANDO UMA COLUNA COM NOTA TOTAL-----------------------------------------------------------------------------------------------------------------

# Calcule a média das colunas restantes e crie a nova coluna
# enem_data['MEDIA_TOTAL'] = enem_data[colunas_media].mean(axis=1)

# Supondo que você queira limitar as casas decimais a 2 para a coluna 'nome_da_coluna'
# enem_data['MEDIA_TOTAL'] = enem_data['MEDIA_TOTAL_'].apply(lambda x: round(x, 1))

# # Opcionalmente, exclua a coluna original e mantenha a arredondada
# enem_data.drop('MEDIA_TOTAL_', axis=1, inplace=True)

# # Visualize o resultado
# print(enem_data.head())

# enem_data.to_csv('MICRODADOS_ENEM_2022 - Copia.csv', index=False)

st.header('Gráfico de barras')

#---------------------------------1--------------------------GERAR O GRÁFICO DE BARRAS------------------------------------------------------------------------------------------------------------  

categoria_idade = {
    1:'Menor que 17 anos', 
    2:'17 anos', 
    3:'18 anos', 
    4:'19 anos', 
    5:'20 anos', 
    6:'21 anos', 
    7:'22 anos', 
    8:'23 anos', 
    9:'24 anos', 
    10:'25 anos', 
    11:'Entre 26 e 30 anos', 
    12:'Entre 31 e 35 anos', 
    13:'Entre 36 e 40 anos', 
    14:'Entre 41 e 45 anos', 
    15:'Entre 46 e 50 anos', 
    16:'Entre 51 e 55 anos', 
    17:'Entre 56 e 60 anos', 
    18:'Entre 61 e 65 anos', 
    19:'Entre 66 e 70 anos', 
    20:'Maior que 70 anos'
}

st.subheader('Média de Notas por Faixa Etária e Estado')

# Ordenar os estados em ordem alfabética
estados_unicos = sorted(enem_data['SG_UF_PROVA'].unique())

estados_selecionados = st.multiselect('Selecione o Estado:', estados_unicos)

# Limitar a seleção a no máximo 5 estados
if len(estados_selecionados) > 5:
    st.error("Por favor, selecione no máximo 5 estados.")
else:
    if len(estados_selecionados) > 0:
        # Filtrar os dados com base nos estados selecionados
        dados_filtrados = enem_data[enem_data['SG_UF_PROVA'].isin(estados_selecionados)]
        
        # Substituir os números pelas frases na coluna 'TP_FAIXA_ETARIA'
        dados_filtrados['TP_FAIXA_ETARIA'] = dados_filtrados['TP_FAIXA_ETARIA'].replace(categoria_idade)
        
        # Ordenar as categorias por ordem personalizada
        categorias_ordenadas = list(categoria_idade.values())
        
        # Agrupar os dados filtrados por estado e faixa etária e calcular a média das notas
        grouped_data = dados_filtrados.groupby(['SG_UF_PROVA', 'TP_FAIXA_ETARIA'])['MEDIA_TOTAL'].mean().unstack()
        grouped_data = grouped_data.reindex(categorias_ordenadas, axis=1)
        
        # Criar a figura do gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Definir a largura das barras
        n = len(estados_selecionados)
        bar_width = 0.8 / n  # Afinar as barras conforme o número de estados selecionados
        x = np.arange(len(categorias_ordenadas))
        
        # Plotar as barras para cada estado
        for i, estado in enumerate(estados_selecionados):
            ax.bar(x + i * bar_width, grouped_data.loc[estado], width=bar_width, label=estado)
        
        # Configurar o título do gráfico, rótulos dos eixos e legenda
        ax.set_title('Média de Notas por Faixa Etária e Estado')
        ax.set_xlabel('Faixa Etária')
        ax.set_ylabel('Média da Nota Total')
        ax.set_xticks(x + bar_width * (n - 1) / 2)
        ax.set_xticklabels(categorias_ordenadas, rotation=90)
        
        # Colocar a legenda fora do gráfico
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        
        # Ajustar o layout para não cortar a legenda
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
    else:
        st.write("Por favor, selecione pelo menos um estado.")

#---------------------------------2------------------------------------------------------------------------------------------------------------------------------------------------------------
# Subtítulo para o segundo gráfico
st.subheader('Média de Notas por Faixa Etária e Raça/Cor')

# Dicionário de categorias de raça/cor
categoria_raca_cor = {
    0: 'Não declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena'
}

# Substituir os números pelas frases na coluna 'TP_COR_RACA'
enem_data['TP_COR_RACA'] = enem_data['TP_COR_RACA'].replace(categoria_raca_cor)

# Ordenar as raças/cor em ordem alfabética
racas_unicas = sorted(enem_data['TP_COR_RACA'].unique())
racas_selecionadas = st.multiselect('Selecione a Raça/Cor:', racas_unicas)

if len(racas_selecionadas) > 0:
    # Filtrar os dados com base nas raças selecionadas
    dados_filtrados_raca = enem_data[enem_data['TP_COR_RACA'].isin(racas_selecionadas)]
    
    # Substituir os números pelas frases na coluna 'TP_FAIXA_ETARIA'
    dados_filtrados_raca['TP_FAIXA_ETARIA'] = dados_filtrados_raca['TP_FAIXA_ETARIA'].replace(categoria_idade)
    
    # Ordenar as categorias por ordem personalizada
    categorias_ordenadas = list(categoria_idade.values())
    
    # Agrupar os dados filtrados por raça/cor e faixa etária e calcular a média das notas
    grouped_data_raca = dados_filtrados_raca.groupby(['TP_COR_RACA', 'TP_FAIXA_ETARIA'])['MEDIA_TOTAL'].mean().unstack()
    grouped_data_raca = grouped_data_raca.reindex(categorias_ordenadas, axis=1)
    
    # Criar a figura do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Definir a largura das barras e as posições no eixo x
    bar_width = 0.15
    x = range(len(categorias_ordenadas))
    
    # Plotar as barras para cada raça/cor
    for i, raca_cor in enumerate(racas_selecionadas):
        ax.bar([p + bar_width * i for p in x], grouped_data_raca.loc[raca_cor], width=bar_width, label=raca_cor)
    
    # Configurar o título do gráfico, rótulos dos eixos e legenda
    ax.set_title('Média de Notas por Faixa Etária e Raça/Cor')
    ax.set_xlabel('Faixa Etária')
    ax.set_ylabel('Média da Nota Total')
    ax.set_xticks([p + bar_width * (len(racas_selecionadas) - 1) / 2 for p in x])
    ax.set_xticklabels(categorias_ordenadas, rotation=90)
    
    # Colocar a legenda fora do gráfico
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Ajustar o layout para não cortar a legenda
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
else:
    st.write("Por favor, selecione pelo menos uma raça/cor.")

#---------------------------------3------------------------------------------------------------------------------------------------------------------------------------------------------------

# Dicionário de categorias de sexo
categoria_sexo = {
    'M': 'Masculino',
    'F': 'Feminino'
}

# Subtítulo para o gráfico
st.subheader('Média de Notas por Faixa Etária e Sexo')

# Substituir os números pelas frases na coluna 'TP_SEXO'
enem_data['TP_SEXO'] = enem_data['TP_SEXO'].replace(categoria_sexo)

# Ordenar os sexos em ordem alfabética
sexos_unicos = sorted(enem_data['TP_SEXO'].unique())
sexos_selecionados = st.multiselect('Selecione o Sexo:', sexos_unicos)

if len(sexos_selecionados) > 0:
    # Filtrar os dados com base nos sexos selecionados
    dados_filtrados_sexo = enem_data[enem_data['TP_SEXO'].isin(sexos_selecionados)]
    
    # Substituir os números pelas frases na coluna 'TP_FAIXA_ETARIA'
    dados_filtrados_sexo['TP_FAIXA_ETARIA'] = dados_filtrados_sexo['TP_FAIXA_ETARIA'].replace(categoria_idade)
    
    # Ordenar as categorias por ordem personalizada
    categorias_ordenadas = list(categoria_idade.values())
    
    # Agrupar os dados filtrados por sexo e faixa etária e calcular a média das notas
    grouped_data_sexo = dados_filtrados_sexo.groupby(['TP_SEXO', 'TP_FAIXA_ETARIA'])['MEDIA_TOTAL'].mean().unstack()
    grouped_data_sexo = grouped_data_sexo.reindex(categorias_ordenadas, axis=1)
    
    # Criar a figura do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Definir a largura das barras e as posições no eixo x
    bar_width = 0.35
    x = range(len(categorias_ordenadas))
    
    # Plotar as barras para cada sexo
    for i, sexo in enumerate(sexos_selecionados):
        ax.bar([p + bar_width * i for p in x], grouped_data_sexo.loc[sexo], width=bar_width, label=sexo)
    
    # Configurar o título do gráfico, rótulos dos eixos e legenda
    ax.set_title('Média de Notas por Faixa Etária e Sexo')
    ax.set_xlabel('Faixa Etária')
    ax.set_ylabel('Média da Nota Total')
    ax.set_xticks([p + bar_width * (len(sexos_selecionados) - 1) / 2 for p in x])
    ax.set_xticklabels(categorias_ordenadas, rotation=90)
    
    # Colocar a legenda fora do gráfico
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Ajustar o layout para não cortar a legenda
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
else:
    st.write("Por favor, selecione pelo menos um sexo.")

#---------------------------------4------------------------------------------------------------------------------------------------------------------------------------------------------------

# Dicionário de tipos de escola
tipos_escola = {
    1: "Não Respondeu",
    2: "Pública",
    3: "Privada"
}

# Subtítulo para o gráfico
st.subheader('Média de Notas por Faixa Etária e Tipo de Escola')

# Substituir os números pelas frases na coluna 'TP_ESCOLA'
enem_data['TP_ESCOLA'] = enem_data['TP_ESCOLA'].replace(tipos_escola)

# Ordenar os tipos de escola em ordem alfabética
escolas_unicas = sorted(enem_data['TP_ESCOLA'].unique())
escolas_selecionadas = st.multiselect('Selecione o Tipo de Escola:', escolas_unicas)

if len(escolas_selecionadas) > 0:
    # Filtrar os dados com base nos tipos de escola selecionados
    dados_filtrados_escola = enem_data[enem_data['TP_ESCOLA'].isin(escolas_selecionadas)]
    
    # Substituir os números pelas frases na coluna 'TP_FAIXA_ETARIA'
    dados_filtrados_escola['TP_FAIXA_ETARIA'] = dados_filtrados_escola['TP_FAIXA_ETARIA'].replace(categoria_idade)
    
    # Ordenar as categorias por ordem personalizada
    categorias_ordenadas = list(categoria_idade.values())
    
    # Agrupar os dados filtrados por tipo de escola e faixa etária e calcular a média das notas
    grouped_data_escola = dados_filtrados_escola.groupby(['TP_ESCOLA', 'TP_FAIXA_ETARIA'])['MEDIA_TOTAL'].mean().unstack()
    grouped_data_escola = grouped_data_escola.reindex(categorias_ordenadas, axis=1)
    
    # Criar a figura do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Definir a largura das barras e as posições no eixo x
    bar_width = 0.25
    x = range(len(categorias_ordenadas))
    
    # Plotar as barras para cada tipo de escola
    for i, escola in enumerate(escolas_selecionadas):
        ax.bar([p + bar_width * i for p in x], grouped_data_escola.loc[escola], width=bar_width, label=escola)
    
    # Configurar o título do gráfico, rótulos dos eixos e legenda
    ax.set_title('Média de Notas por Faixa Etária e Tipo de Escola')
    ax.set_xlabel('Faixa Etária')
    ax.set_ylabel('Média da Nota Total')
    ax.set_xticks([p + bar_width * (len(escolas_selecionadas) - 1) / 2 for p in x])
    ax.set_xticklabels(categorias_ordenadas, rotation=90)
    
    # Colocar a legenda fora do gráfico
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Ajustar o layout para não cortar a legenda
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
else:
    st.write("Por favor, selecione pelo menos um tipo de escola.")

#---------------------------------5------------------------------------------------------------------------------------------------------------------------------------------------------------

faixas_etarias_descricao = {
    1: 'Menor de 17 anos',
    2: '17 anos',
    3: '18 anos',
    4: '19 anos',
    5: '20 anos',
    6: '21 anos',
    7: '22 anos',
    8: '23 anos',
    9: '24 anos',
    10: '25 anos',
    11: 'Entre 26 e 30 anos',
    12: 'Entre 31 e 35 anos',
    13: 'Entre 36 e 40 anos',
    14: 'Entre 41 e 45 anos',
    15: 'Entre 46 e 50 anos',
    16: 'Entre 51 e 55 anos',
    17: 'Entre 56 e 60 anos',
    18: 'Entre 61 e 65 anos',
    19: 'Entre 66 e 70 anos',
    20: 'Maior de 70 anos'
}

# Subtítulo para o gráfico
st.subheader('Média de Notas por Estado e Faixa Etária')

# Multiselect com as opções de faixas etárias e suas descrições
faixas_etaria_multiselect_key = "faixa_etaria_multiselect"
faixas_etarias_selecionadas = st.multiselect('Selecione a Faixa Etária (máximo 3 seleções):', 
                                             list(faixas_etarias_descricao.items()), 
                                             format_func=lambda x: x[1],
                                             key=faixas_etaria_multiselect_key)

# Verificar se o número de faixas etárias selecionadas excede 3
if len(faixas_etarias_selecionadas) > 3:
    st.warning("Por favor, selecione no máximo 3 faixas etárias.")
else:
    if len(faixas_etarias_selecionadas) > 0:
        # Filtrar os dados com base nas faixas etárias selecionadas
        dados_filtrados_faixa_etaria = enem_data[enem_data['TP_FAIXA_ETARIA'].isin([x[0] for x in faixas_etarias_selecionadas])]
        
        # Agrupar os dados filtrados por estado e faixa etária e calcular a média das notas
        grouped_data_faixa_etaria = dados_filtrados_faixa_etaria.groupby(['SG_UF_PROVA', 'TP_FAIXA_ETARIA'])['MEDIA_TOTAL'].mean().unstack()
        
        # Criar a figura do gráfico
        fig, ax = plt.subplots(figsize=(12, 6))  # Ajuste do tamanho do gráfico
        
        # Largura das barras e quantidade de faixas etárias
        n = len(faixas_etarias_selecionadas)
        bar_width = 0.8 / len(faixas_etarias_selecionadas)  # Ajuste do espaçamento entre as barras
        bar_positions = np.arange(len(grouped_data_faixa_etaria.index))
        
        # Plotar as barras para cada faixa etária
        for i, faixa_etaria in enumerate(faixas_etarias_selecionadas):
            ax.bar(bar_positions + i * bar_width, 
                   grouped_data_faixa_etaria[faixa_etaria[0]], 
                   width=bar_width, 
                   label=faixa_etaria[1])
        
        # Configurar o título do gráfico, rótulos dos eixos e legenda
        ax.set_title('Média de Notas por Estado e Faixa Etária')
        ax.set_xlabel('Estado')
        ax.set_ylabel('Média da Nota Total')
        ax.legend(title='Faixa Etária', loc='upper left', bbox_to_anchor=(1, 1))
        ax.set_xticks(bar_positions + bar_width * (n - 1) / 2)  # Posicionamento dos ticks do eixo x
        ax.set_xticklabels(grouped_data_faixa_etaria.index, rotation=45)  # Definindo os estados no eixo x
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
    else:
        st.write("Por favor, selecione pelo menos uma faixa etária.")

#-------------------------------6--------------------------------------------------------------------------------------------------------------------------------------------------------------

# Subtítulo para o segundo gráfico
st.subheader('Média de Notas por Estado e Raça/Cor')

# Dicionário de categorias de raça/cor
categoria_raca_cor = {
    0: 'Não declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena'
}

# Substituir os números pelas frases na coluna 'TP_COR_RACA'
enem_data['TP_COR_RACA'] = enem_data['TP_COR_RACA'].replace(categoria_raca_cor)

# Ordenar as raças/cor em ordem alfabética
racas_unicas = sorted(enem_data['TP_COR_RACA'].unique())
racas_selecionadas = st.multiselect('Selecione a Raça / cor', racas_unicas)

if len(racas_selecionadas) > 0:
    # Filtrar os dados com base nas raças selecionadas
    dados_filtrados_raca = enem_data[enem_data['TP_COR_RACA'].isin(racas_selecionadas)]
    
    # Obter os estados únicos e ordená-los
    estados_unicos = sorted(dados_filtrados_raca['SG_UF_PROVA'].unique())
    
    # Agrupar os dados filtrados por raça/cor e estado e calcular a média das notas
    grouped_data_raca = dados_filtrados_raca.groupby(['TP_COR_RACA', 'SG_UF_PROVA'])['MEDIA_TOTAL'].mean().unstack()
    
    # Criar a figura do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Definir a largura das barras e as posições no eixo x
    bar_width = 0.15
    x = range(len(estados_unicos))
    
    # Plotar as barras para cada raça/cor
    for i, raca_cor in enumerate(racas_selecionadas):
        ax.bar([p + bar_width * i for p in x], grouped_data_raca.loc[raca_cor], width=bar_width, label=raca_cor)
    
    # Configurar o título do gráfico, rótulos dos eixos e legenda
    ax.set_title('Média de Notas por Estado e Raça/Cor')
    ax.set_xlabel('Estado')
    ax.set_ylabel('Média da Nota Total')
    ax.set_xticks([p + bar_width * (len(racas_selecionadas) - 1) / 2 for p in x])
    ax.set_xticklabels(estados_unicos, rotation=90)
    
    # Colocar a legenda fora do gráfico
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Ajustar o layout para não cortar a legenda
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
else:
    st.write("Por favor, selecione pelo menos uma raça/cor.")


#-------------------------------7-------------------------------------------------------------------------------------------------------------------------------------------------------------

# Dicionário de categorias de sexo
categoria_sexo = {
    'M': 'Masculino',
    'F': 'Feminino'
}

# Subtítulo para o gráfico
st.subheader('Média de Notas por Estado e Sexo')

# Substituir os códigos pelas frases na coluna 'TP_SEXO'
enem_data['TP_SEXO'] = enem_data['TP_SEXO'].replace(categoria_sexo)

# Ordenar os sexos em ordem alfabética
sexos_unicos = sorted(enem_data['TP_SEXO'].unique())
sexos_selecionados = st.multiselect('Selecione o  Sexo:', sexos_unicos)

if len(sexos_selecionados) > 0:
    # Filtrar os dados com base nos sexos selecionados
    dados_filtrados_sexo = enem_data[enem_data['TP_SEXO'].isin(sexos_selecionados)]
    
    # Obter os estados únicos e ordená-los
    estados_unicos = sorted(dados_filtrados_sexo['SG_UF_PROVA'].unique())
    
    # Agrupar os dados filtrados por sexo e estado e calcular a média das notas
    grouped_data_sexo = dados_filtrados_sexo.groupby(['TP_SEXO', 'SG_UF_PROVA'])['MEDIA_TOTAL'].mean().unstack()
    
    # Criar a figura do gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Definir a largura das barras e as posições no eixo x
    bar_width = 0.35
    x = range(len(estados_unicos))
    
    # Plotar as barras para cada sexo
    for i, sexo in enumerate(sexos_selecionados):
        ax.bar([p + bar_width * i for p in x], grouped_data_sexo.loc[sexo], width=bar_width, label=sexo)
    
    # Configurar o título do gráfico, rótulos dos eixos e legenda
    ax.set_title('Média de Notas por Estado e Sexo')
    ax.set_xlabel('Estado')
    ax.set_ylabel('Média da Nota Total')
    ax.set_xticks([p + bar_width * (len(sexos_selecionados) - 1) / 2 for p in x])
    ax.set_xticklabels(estados_unicos, rotation=90)
    
    # Colocar a legenda fora do gráfico
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Ajustar o layout para não cortar a legenda
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
else:
    st.write("Por favor, selecione pelo menos um sexo.")

#-------------------------------8-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dicionário de tipos de escola
tipos_escola = {
    1: "Não Respondeu",
    2: "Pública",
    3: "Privada"
}

# Subtítulo para o gráfico
st.subheader('Média de Notas por Estado e Tipo de Escola')

# Substituir os números pelas frases na coluna 'TP_ESCOLA'
enem_data['TP_ESCOLA'] = enem_data['TP_ESCOLA'].replace(tipos_escola)

# Ordenar os tipos de escola em ordem alfabética
escolas_unicas = sorted(enem_data['TP_ESCOLA'].unique())
escolas_selecionadas = st.multiselect('Selecione o Tipo de  Escola:', escolas_unicas)

if len(escolas_selecionadas) > 0:
    # Filtrar os dados com base nos tipos de escola selecionados
    dados_filtrados_escola = enem_data[enem_data['TP_ESCOLA'].isin(escolas_selecionadas)]
    
    # Obter os estados únicos e ordená-los
    estados_unicos = sorted(dados_filtrados_escola['SG_UF_PROVA'].unique())
    
    # Agrupar os dados filtrados por tipo de escola e estado e calcular a média das notas
    grouped_data_escola = dados_filtrados_escola.groupby(['TP_ESCOLA', 'SG_UF_PROVA'])['MEDIA_TOTAL'].mean().unstack()
    
    # Criar a figura do gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Definir a largura das barras e as posições no eixo x
    bar_width = 0.25
    x = range(len(estados_unicos))
    
    # Plotar as barras para cada tipo de escola
    for i, escola in enumerate(escolas_selecionadas):
        ax.bar([p + bar_width * i for p in x], grouped_data_escola.loc[escola], width=bar_width, label=escola)
    
    # Configurar o título do gráfico, rótulos dos eixos e legenda
    ax.set_title('Média de Notas por Estado e Tipo de Escola')
    ax.set_xlabel('Estado')
    ax.set_ylabel('Média da Nota Total')
    ax.set_xticks([p + bar_width * (len(escolas_selecionadas) - 1) / 2 for p in x])
    ax.set_xticklabels(estados_unicos, rotation=90)
    
    # Colocar a legenda fora do gráfico
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Ajustar o layout para não cortar a legenda
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
else:
    st.write("Por favor, selecione pelo menos um tipo de escola.")

#-------------------------------9-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dicionário de categorias de cor/raça
categoria_cor = {
    0: 'Não declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena'
}

st.subheader('Média de Notas por Cor/Raça e Estado')

# Ordenar os estados em ordem alfabética
estados_unicos = sorted(enem_data['SG_UF_PROVA'].unique())

estados_selecionados = st.multiselect('Selecione o  Estado:', estados_unicos)

# Limitar a seleção a no máximo 5 estados
if len(estados_selecionados) > 5:
    st.error("Por favor, selecione no máximo 5 estados.")
else:
    if len(estados_selecionados) > 0:
        # Filtrar os dados com base nos estados selecionados
        dados_filtrados = enem_data[enem_data['SG_UF_PROVA'].isin(estados_selecionados)]
        
        # Substituir os números pelas frases na coluna 'TP_COR_RACA'
        dados_filtrados['TP_COR_RACA'] = dados_filtrados['TP_COR_RACA'].replace(categoria_cor)
        
        # Ordenar as categorias por ordem personalizada
        categorias_ordenadas = list(categoria_cor.values())
        
        # Agrupar os dados filtrados por estado e cor/raça e calcular a média das notas
        grouped_data = dados_filtrados.groupby(['SG_UF_PROVA', 'TP_COR_RACA'])['MEDIA_TOTAL'].mean().unstack()
        grouped_data = grouped_data.reindex(categorias_ordenadas, axis=1)
        
        # Criar a figura do gráfico
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Definir a largura das barras
        n = len(estados_selecionados)
        bar_width = 0.8 / n  # Afinar as barras conforme o número de estados selecionados
        x = np.arange(len(categorias_ordenadas))
        
        # Plotar as barras para cada estado
        for i, estado in enumerate(estados_selecionados):
            ax.bar(x + i * bar_width, grouped_data.loc[estado], width=bar_width, label=estado)
        
        # Configurar o título do gráfico, rótulos dos eixos e legenda
        ax.set_title('Média de Notas por Cor/Raça e Estado')
        ax.set_xlabel('Cor/Raça')
        ax.set_ylabel('Média da Nota Total')
        ax.set_xticks(x + bar_width * (n - 1) / 2)
        ax.set_xticklabels(categorias_ordenadas, rotation=90)
        
        # Colocar a legenda fora do gráfico
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        
        # Ajustar o layout para não cortar a legenda
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
    else:
        st.write("Por favor, selecione pelo menos um estado.")

#-----------------------------10---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dicionário de categorias de sexo
categoria_sexo = {
    'M': 'Masculino',
    'F': 'Feminino'
}

# Dicionário de categorias de raça
categoria_raca = {
    0: 'Não declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena'
}

# Subtítulo para o gráfico
st.subheader('Média de Notas por Raça e Sexo')

# Substituir os números pelas frases na coluna 'TP_SEXO'
enem_data['TP_SEXO'] = enem_data['TP_SEXO'].replace(categoria_sexo)

# Ordenar os sexos em ordem alfabética
sexos_unicos = sorted(enem_data['TP_SEXO'].unique())
sexos_selecionados = st.multiselect('Selecione  o  Sexo:', sexos_unicos)

if len(sexos_selecionados) > 0:
    # Filtrar os dados com base nos sexos selecionados
    dados_filtrados_sexo = enem_data[enem_data['TP_SEXO'].isin(sexos_selecionados)]
    
    # Substituir os números pelas frases na coluna 'TP_COR_RACA'
    dados_filtrados_sexo['TP_COR_RACA'] = dados_filtrados_sexo['TP_COR_RACA'].replace(categoria_raca)
    
    # Ordenar as categorias por ordem personalizada
    categorias_ordenadas = list(categoria_raca.values())
    
    # Agrupar os dados filtrados por sexo e raça e calcular a média das notas
    grouped_data_sexo = dados_filtrados_sexo.groupby(['TP_SEXO', 'TP_COR_RACA'])['MEDIA_TOTAL'].mean().unstack()
    grouped_data_sexo = grouped_data_sexo.reindex(categorias_ordenadas, axis=1)
    
    # Criar a figura do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Definir a largura das barras e as posições no eixo x
    bar_width = 0.35
    x = range(len(categorias_ordenadas))
    
    # Plotar as barras para cada sexo
    for i, sexo in enumerate(sexos_selecionados):
        ax.bar([p + bar_width * i for p in x], grouped_data_sexo.loc[sexo], width=bar_width, label=sexo)
    
    # Configurar o título do gráfico, rótulos dos eixos e legenda
    ax.set_title('Média de Notas por Raça e Sexo')
    ax.set_xlabel('Raça')
    ax.set_ylabel('Média da Nota Total')
    ax.set_xticks([p + bar_width * (len(sexos_selecionados) - 1) / 2 for p in x])
    ax.set_xticklabels(categorias_ordenadas, rotation=90)
    
    # Colocar a legenda fora do gráfico
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Ajustar o layout para não cortar a legenda
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
else:
    st.write("Por favor, selecione pelo menos um sexo.")

# st_conclusao = ["Já concluí o Ensino Médio","Estou cursando e concluirei o Ensino Médio em 2022","Estou cursando e concluirei o Ensino Médio após 2022","Não concluí e não estou cursando o Ensino Médio"]

#-----------------------------11--------------------------------------------------------------------------------------------------------------------------------------------------------------
tipos_escola = {
    1: "Não Respondeu",
    2: "Pública",
    3: "Privada"
}

# Subtítulo para o gráfico
st.subheader('Média de Notas por Raça e Tipo de Escola')

# Substituir os números pelas frases na coluna 'TP_ESCOLA'
enem_data['TP_ESCOLA'] = enem_data['TP_ESCOLA'].replace(tipos_escola)

# Ordenar os tipos de escola em ordem alfabética
escolas_unicas = sorted(enem_data['TP_ESCOLA'].unique())
escolas_selecionadas = st.multiselect('Selecione  o Tipo de Escola:', escolas_unicas)

if len(escolas_selecionadas) > 0:
    # Filtrar os dados com base nos tipos de escola selecionados
    dados_filtrados_escola = enem_data[enem_data['TP_ESCOLA'].isin(escolas_selecionadas)]
    
    # Substituir os números pelas frases na coluna 'TP_COR_RACA'
    dados_filtrados_escola['TP_COR_RACA'] = dados_filtrados_escola['TP_COR_RACA'].replace(categoria_raca)
    
    # Ordenar as categorias por ordem personalizada
    categorias_ordenadas = list(categoria_raca.values())
    
    # Agrupar os dados filtrados por tipo de escola e raça e calcular a média das notas
    grouped_data_escola = dados_filtrados_escola.groupby(['TP_ESCOLA', 'TP_COR_RACA'])['MEDIA_TOTAL'].mean().unstack()
    grouped_data_escola = grouped_data_escola.reindex(categorias_ordenadas, axis=1)
    
    # Criar a figura do gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Definir a largura das barras e as posições no eixo x
    bar_width = 0.25
    x = range(len(categorias_ordenadas))
    
    # Plotar as barras para cada tipo de escola
    for i, escola in enumerate(escolas_selecionadas):
        ax.bar([p + bar_width * i for p in x], grouped_data_escola.loc[escola], width=bar_width, label=escola)
    
    # Configurar o título do gráfico, rótulos dos eixos e legenda
    ax.set_title('Média de Notas por Raça e Tipo de Escola')
    ax.set_xlabel('Raça')
    ax.set_ylabel('Média da Nota Total')
    ax.set_xticks([p + bar_width * (len(escolas_selecionadas) - 1) / 2 for p in x])
    ax.set_xticklabels(categorias_ordenadas, rotation=90)
    
    # Colocar a legenda fora do gráfico
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    
    # Ajustar o layout para não cortar a legenda
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
else:
    st.write("Por favor, selecione pelo menos um tipo de escola.")

#---------------------------------20------------------------------------------------------------------------------------------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Abrindo o arquivo de dados
enem_data = pd.read_csv('MICRODADOS_ENEM_2022 - Copia.csv', sep=',', encoding='latin-1')

# Subtítulo para o gráfico
st.subheader('Média de Notas por Tipo de Escola e Sexo')

# Multiselect com as opções de sexo
sexo_multiselect_key = "sexo_multiselect"
sexos_selecionados = st.multiselect('Selecione o Sexo:', ['M', 'F'], key=sexo_multiselect_key)

# Dicionário para mapeamento do tipo de escola
tipo_escola_dict = {
    1: 'Não Respondeu',
    2: 'Pública',
    3: 'Privada'
}

# Verificar se pelo menos um sexo foi selecionado
if len(sexos_selecionados) > 0:
    # Filtrar os dados com base nos sexos selecionados
    dados_filtrados_sexo = enem_data[enem_data['TP_SEXO'].isin(sexos_selecionados)]
    
    # Agrupar os dados filtrados por tipo de escola e sexo, e calcular a média das notas
    grouped_data = dados_filtrados_sexo.groupby(['TP_ESCOLA', 'TP_SEXO'])['MEDIA_TOTAL'].mean().unstack()
    
    # Mapear os tipos de escola usando o dicionário
    grouped_data.index = grouped_data.index.map(tipo_escola_dict)
    
    # Preencher valores ausentes com 0
    grouped_data = grouped_data.reindex(columns=sexos_selecionados, fill_value=0)
    
    # Criar a figura do gráfico
    fig, ax = plt.subplots(figsize=(12, 6))  # Ajuste do tamanho do gráfico
    
    # Definir a largura das barras
    bar_width = 0.35
    
    # Definir a posição das barras
    indices = np.arange(len(grouped_data.index))
    
    # Plotar as barras para cada sexo selecionado
    for i, sexo in enumerate(sexos_selecionados):
        ax.bar(indices + i * bar_width, grouped_data[sexo], bar_width, label=f'Sexo {sexo}')
    
    # Configurar o título do gráfico, rótulos dos eixos e legenda
    ax.set_title('Média de Notas por Tipo de Escola e Sexo')
    ax.set_xlabel('Tipo de Escola')
    ax.set_ylabel('Média da Nota Total')
    ax.set_xticks(indices + bar_width / 2 * (len(sexos_selecionados) - 1))
    ax.set_xticklabels(grouped_data.index)
    ax.legend()
    
    # Mostrar o gráfico no Streamlit
    st.pyplot(fig)
else:
    st.write("Por favor, selecione pelo menos um sexo.")

#--------------------------------21-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Subtítulo para o gráfico
st.subheader('Quantidade de Pessoas por Faixa Etária e Estado')

# Dicionário para mapeamento da faixa etária
faixa_etaria_dict = {
    1: 'Menor de 17 anos',
    2: '17 anos',
    3: '18 anos',
    4: '19 anos',
    5: '20 anos',
    6: '21 anos',
    7: '22 anos',
    8: '23 anos',
    9: '24 anos',
    10: '25 anos',
    11: 'Entre 26 e 30 anos',
    12: 'Entre 31 e 35 anos',
    13: 'Entre 36 e 40 anos',
    14: 'Entre 41 e 45 anos',
    15: 'Entre 46 e 50 anos',
    16: 'Entre 51 e 55 anos',
    17: 'Entre 56 e 60 anos',
    18: 'Entre 61 e 65 anos',
    19: 'Entre 66 e 70 anos',
    20: 'Maior de 70 anos'
}

# Ordenar os estados em ordem alfabética
estados_unicos = sorted(enem_data['SG_UF_PROVA'].unique())

# Multiselect para selecionar os estados
estados_selecionados = st.multiselect('Selecione o Estado:', estados_unicos, key='estado_multiselect')

# Limitar a seleção a no máximo 3 estados
if len(estados_selecionados) > 3:
    st.error("Por favor, selecione no máximo 3 estados.")
else:
    if len(estados_selecionados) > 0:
        # Filtrar os dados com base nos estados selecionados
        dados_filtrados = enem_data[enem_data['SG_UF_PROVA'].isin(estados_selecionados)]
        
        # Substituir os números pelas frases na coluna 'TP_FAIXA_ETARIA'
        dados_filtrados['TP_FAIXA_ETARIA'] = dados_filtrados['TP_FAIXA_ETARIA'].replace(faixa_etaria_dict)
        
        # Agrupar os dados filtrados por estado e faixa etária e contar a quantidade de pessoas
        grouped_data = dados_filtrados.groupby(['SG_UF_PROVA', 'TP_FAIXA_ETARIA']).size().unstack(fill_value=0)
        
        # Reordenar as faixas etárias conforme o dicionário
        categorias_ordenadas = list(faixa_etaria_dict.values())
        grouped_data = grouped_data.reindex(columns=categorias_ordenadas)
        
        # Criar a figura do gráfico
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Definir a largura das barras
        n = len(estados_selecionados)
        bar_width = 0.8 / n  # Afinar as barras conforme o número de estados selecionados
        x = np.arange(len(categorias_ordenadas))
        
        # Plotar as barras para cada estado
        for i, estado in enumerate(estados_selecionados):
            bars = ax.bar(x + i * bar_width, grouped_data.loc[estado], bar_width, label=estado)
            
            # Adicionar os valores das colunas acima das barras com rotação de 90 graus
            for bar in bars:
                height = bar.get_height()
                if not np.isnan(height):  # Verificar se o valor não é NaN
                    ax.annotate(f'{int(height)}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 1),  # 1 point vertical offset to reduce overlap
                                textcoords='offset points',
                                ha='center', va='bottom', rotation=90)
        
        # Configurar o título do gráfico, rótulos dos eixos e legenda
        ax.set_title('Quantidade de Pessoas por Faixa Etária e Estado')
        ax.set_xlabel('Faixa Etária')
        ax.set_ylabel('Quantidade de Pessoas')
        ax.set_xticks(x + bar_width * (n - 1) / 2)
        ax.set_xticklabels(categorias_ordenadas, rotation=90)
        
        # Ajustar os limites do eixo y para garantir que os números não saiam pela parte superior
        max_height = grouped_data.max().max()
        ax.set_ylim(0, max_height * 1.1)
        
        # Colocar a legenda fora do gráfico
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        
        # Ajustar o layout para não cortar a legenda
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
    else:
        st.write("Por favor, selecione pelo menos um estado.")
#--------------------------------22-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Subtítulo para o gráfico
st.subheader('Quantidade de Pessoas por Faixa Etária e Raça/Cor')

# Dicionário para mapeamento de raça/cor
raca_cor_dict = {
    0: 'Não declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena'
}

# Ordenar as raças/cores em ordem dos valores do dicionário
racas_unicas = [raca_cor_dict[key] for key in sorted(raca_cor_dict.keys())]

# Multiselect para selecionar as raças/cores
racas_selecionadas = st.multiselect('Selecione a Raça/Cor:', racas_unicas)

# Limitar a seleção a no máximo 3 raças
if len(racas_selecionadas) > 3:
    st.error("Por favor, selecione no máximo 3 raças/cores.")
else:
    if len(racas_selecionadas) > 0:
        # Converter as raças selecionadas para os respectivos valores numéricos
        racas_selecionadas_numericas = [key for key, value in raca_cor_dict.items() if value in racas_selecionadas]
        
        # Filtrar os dados com base nas raças selecionadas
        dados_filtrados = enem_data[enem_data['TP_COR_RACA'].isin(racas_selecionadas_numericas)]
        
        # Substituir os números pelas frases na coluna 'TP_FAIXA_ETARIA'
        dados_filtrados['TP_FAIXA_ETARIA'] = dados_filtrados['TP_FAIXA_ETARIA'].replace(faixa_etaria_dict)
        
        # Substituir os números pelas frases na coluna 'TP_COR_RACA'
        dados_filtrados['TP_COR_RACA'] = dados_filtrados['TP_COR_RACA'].replace(raca_cor_dict)
        
        # Agrupar os dados filtrados por raça/cor e faixa etária e contar a quantidade de pessoas
        grouped_data = dados_filtrados.groupby(['TP_COR_RACA', 'TP_FAIXA_ETARIA']).size().unstack(fill_value=0)
        
        # Reordenar as faixas etárias conforme o dicionário
        categorias_ordenadas = list(faixa_etaria_dict.values())
        grouped_data = grouped_data.reindex(columns=categorias_ordenadas)
        
        # Criar a figura do gráfico
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Definir a largura das barras
        n = len(racas_selecionadas)
        bar_width = 0.8 / n  # Afinar as barras conforme o número de raças selecionadas
        x = np.arange(len(categorias_ordenadas))
        
        # Plotar as barras para cada raça/cor
        for i, raca in enumerate(racas_selecionadas):
            bars = ax.bar(x + i * bar_width, grouped_data.loc[raca], bar_width, label=raca)
            
            # Adicionar os valores das colunas acima das barras com rotação de 90 graus
            for bar in bars:
                height = bar.get_height()
                if not np.isnan(height):  # Verificar se o valor não é NaN
                    ax.annotate(f'{int(height)}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 1),  # 1 point vertical offset to reduce overlap
                                textcoords='offset points',
                                ha='center', va='bottom', rotation=90)
        
        # Configurar o título do gráfico, rótulos dos eixos e legenda
        ax.set_title('Quantidade de Pessoas por Faixa Etária e Raça/Cor')
        ax.set_xlabel('Faixa Etária')
        ax.set_ylabel('Quantidade de Pessoas')
        ax.set_xticks(x + bar_width * (n - 1) / 2)
        ax.set_xticklabels(categorias_ordenadas, rotation=90)
        
        # Ajustar os limites do eixo y para garantir que os números não saiam pela parte superior
        max_height = grouped_data.max().max()
        ax.set_ylim(0, max_height * 1.1)
        
        # Colocar a legenda fora do gráfico
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        
        # Ajustar o layout para não cortar a legenda
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
    else:
        st.write("Por favor, selecione pelo menos uma raça/cor.")
#--------------------------------23-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Subtítulo para o gráfico
st.subheader('Quantidade de Pessoas por Faixa Etária e Gênero')

# Dicionário para mapeamento de gênero
genero_dict = {
    'M': 'Masculino',
    'F': 'Feminino'
}

# Ordenar os gêneros em ordem dos valores do dicionário
generos_unicos = [genero_dict[key] for key in sorted(genero_dict.keys())]

# Multiselect para selecionar o gênero
generos_selecionados = st.multiselect('Selecione o Gênero:', generos_unicos)

# Limitar a seleção a no máximo 2 gêneros
if len(generos_selecionados) > 2:
    st.error("Por favor, selecione no máximo 2 gêneros.")
else:
    if len(generos_selecionados) > 0:
        # Converter os gêneros selecionados para os respectivos valores numéricos
        generos_selecionados_numericos = [key for key, value in genero_dict.items() if value in generos_selecionados]
        
        # Filtrar os dados com base nos gêneros selecionados
        dados_filtrados = enem_data[enem_data['TP_SEXO'].isin(generos_selecionados_numericos)]
        
        # Substituir os números pelas frases na coluna 'TP_FAIXA_ETARIA'
        dados_filtrados['TP_FAIXA_ETARIA'] = dados_filtrados['TP_FAIXA_ETARIA'].replace(faixa_etaria_dict)
        
        # Substituir os números pelas frases na coluna 'TP_SEXO'
        dados_filtrados['TP_SEXO'] = dados_filtrados['TP_SEXO'].replace(genero_dict)
        
        # Agrupar os dados filtrados por gênero e faixa etária e contar a quantidade de pessoas
        grouped_data = dados_filtrados.groupby(['TP_SEXO', 'TP_FAIXA_ETARIA']).size().unstack(fill_value=0)
        
        # Reordenar as faixas etárias conforme o novo dicionário
        categorias_ordenadas = list(faixa_etaria_dict.values())
        grouped_data = grouped_data.reindex(columns=categorias_ordenadas)
        
        # Criar a figura do gráfico
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Definir a largura das barras
        n = len(generos_selecionados)
        bar_width = 0.8 / n  # Afinar as barras conforme o número de gêneros selecionados
        x = np.arange(len(categorias_ordenadas))
        
        # Plotar as barras para cada gênero
        for i, genero in enumerate(generos_selecionados):
            bars = ax.bar(x + i * bar_width, grouped_data.loc[genero], bar_width, label=genero)
            
            # Adicionar os valores das colunas acima das barras com rotação de 90 graus
            for bar in bars:
                height = bar.get_height()
                if not np.isnan(height):  # Verificar se o valor não é NaN
                    ax.annotate(f'{int(height)}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 1),  # 1 point vertical offset to reduce overlap
                                textcoords='offset points',
                                ha='center', va='bottom', rotation=90)
        
        # Configurar o título do gráfico, rótulos dos eixos e legenda
        ax.set_title('Quantidade de Pessoas por Faixa Etária e Gênero')
        ax.set_xlabel('Faixa Etária')
        ax.set_ylabel('Quantidade de Pessoas')
        ax.set_xticks(x + bar_width * (n - 1) / 2)
        ax.set_xticklabels(categorias_ordenadas, rotation=90)
        
        # Ajustar os limites do eixo y para garantir que os números não saiam pela parte superior
        max_height = grouped_data.max().max()
        ax.set_ylim(0, max_height * 1.1)
        
        # Colocar a legenda fora do gráfico
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        
        # Ajustar o layout para não cortar a legenda
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
    else:
        st.write("Por favor, selecione pelo menos um gênero.")
#--------------------------------24-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Subtítulo para o gráfico
st.subheader('Quantidade de Pessoas por Faixa Etária e Tipo de Escola')

# Dicionário para mapeamento de tipo de escola
tipo_escola_dict = {
    1: 'Não Respondeu',
    2: 'Pública',
    3: 'Privada'
}

# Ordenar os tipos de escola em ordem dos valores do dicionário
tipos_escola_unicos = [tipo_escola_dict[key] for key in sorted(tipo_escola_dict.keys())]

# Multiselect para selecionar o tipo de escola
tipos_escola_selecionados = st.multiselect('Selecione o Tipo de Escola:', tipos_escola_unicos)

# Limitar a seleção a no máximo 3 tipos de escola
if len(tipos_escola_selecionados) > 3:
    st.error("Por favor, selecione no máximo 3 tipos de escola.")
else:
    if len(tipos_escola_selecionados) > 0:
        # Converter os tipos de escola selecionados para os respectivos valores numéricos
        tipos_escola_selecionados_numericos = [key for key, value in tipo_escola_dict.items() if value in tipos_escola_selecionados]
        
        # Filtrar os dados com base nos tipos de escola selecionados
        dados_filtrados = enem_data[enem_data['TP_ESCOLA'].isin(tipos_escola_selecionados_numericos)]
        
        # Substituir os números pelas frases na coluna 'TP_FAIXA_ETARIA'
        dados_filtrados['TP_FAIXA_ETARIA'] = dados_filtrados['TP_FAIXA_ETARIA'].replace(faixa_etaria_dict)
        
        # Substituir os números pelas frases na coluna 'TP_ESCOLA'
        dados_filtrados['TP_ESCOLA'] = dados_filtrados['TP_ESCOLA'].replace(tipo_escola_dict)
        
        # Agrupar os dados filtrados por tipo de escola e faixa etária e contar a quantidade de pessoas
        grouped_data = dados_filtrados.groupby(['TP_ESCOLA', 'TP_FAIXA_ETARIA']).size().unstack(fill_value=0)
        
        # Reordenar as faixas etárias conforme o novo dicionário
        categorias_ordenadas = list(faixa_etaria_dict.values())
        grouped_data = grouped_data.reindex(columns=categorias_ordenadas)
        
        # Criar a figura do gráfico
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Definir a largura das barras
        n = len(tipos_escola_selecionados)
        bar_width = 0.8 / n  # Afinar as barras conforme o número de tipos de escola selecionados
        x = np.arange(len(categorias_ordenadas))
        
        # Plotar as barras para cada tipo de escola
        for i, tipo_escola in enumerate(tipos_escola_selecionados):
            bars = ax.bar(x + i * bar_width, grouped_data.loc[tipo_escola], bar_width, label=tipo_escola)
            
            # Adicionar os valores das colunas acima das barras com rotação de 90 graus
            for bar in bars:
                height = bar.get_height()
                if not np.isnan(height):  # Verificar se o valor não é NaN
                    ax.annotate(f'{int(height)}',
                                xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 1),  # 1 point vertical offset to reduce overlap
                                textcoords='offset points',
                                ha='center', va='bottom', rotation=90)
        
        # Configurar o título do gráfico, rótulos dos eixos e legenda
        ax.set_title('Quantidade de Pessoas por Faixa Etária e Tipo de Escola')
        ax.set_xlabel('Faixa Etária')
        ax.set_ylabel('Quantidade de Pessoas')
        ax.set_xticks(x + bar_width * (n - 1) / 2)
        ax.set_xticklabels(categorias_ordenadas, rotation=90)
        
        # Ajustar os limites do eixo y para garantir que os números não saiam pela parte superior
        max_height = grouped_data.max().max()
        ax.set_ylim(0, max_height * 1.1)
        
        # Colocar a legenda fora do gráfico
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
        
        # Ajustar o layout para não cortar a legenda
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
    else:
        st.write("Por favor, selecione pelo menos um tipo de escola.")
#--------------------------------25-------------------------------------------------------------------------------------------------------------------------------------------------------------

# Subtítulo para o gráfico
st.subheader('Quantidade de Pessoas por Estado e Faixa Etária')

# Ordenar as faixas etárias em ordem dos valores do dicionário
faixas_unicas = [faixa_etaria_dict[key] for key in sorted(faixa_etaria_dict.keys())]

# Multiselect para selecionar as faixas etárias
faixas_selecionadas = st.multiselect('Selecione até 3 Faixas Etárias:', faixas_unicas, key="faixas")

if len(faixas_selecionadas) > 3:
    st.error("Por favor, selecione no máximo 3 faixas etárias.")
else:
    if len(faixas_selecionadas) == 0:
        st.write("Por favor, selecione pelo menos uma faixa etária.")
    else:
        # Filtrar os dados com base nas faixas etárias selecionadas
        dados_filtrados = enem_data[enem_data['TP_FAIXA_ETARIA'].isin([key for key, value in faixa_etaria_dict.items() if value in faixas_selecionadas])]
        
        # Criar uma tabela dinâmica (pivot table) para contar o número de pessoas por estado e faixa etária
        pivot_table = dados_filtrados.pivot_table(index='SG_UF_PROVA', columns='TP_FAIXA_ETARIA', aggfunc='size', fill_value=0)
        
        # Reordenar as faixas etárias conforme o dicionário
        pivot_table = pivot_table.rename(columns=faixa_etaria_dict)
        
        # Plotar o gráfico de barras
        fig, ax = plt.subplots(figsize=(12, 8))
        pivot_table.plot(kind='bar', ax=ax, stacked=False)
        
        # Adicionar os valores das colunas acima das barras com rotação de 90 graus
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f'{int(height)}', 
                            xy=(p.get_x() + p.get_width() / 2, height),
                            xytext=(0, 3), 
                            textcoords='offset points',
                            ha='center', va='bottom', rotation=90)
        
        # Configurar o título do gráfico e rótulos dos eixos
        ax.set_title('Quantidade de Pessoas por Estado e Faixa Etária')
        ax.set_xlabel('Estado')
        ax.set_ylabel('Quantidade de Pessoas')
        
        # Colocar a legenda fora do gráfico
        ax.legend(title='Faixa Etária', loc='upper left', bbox_to_anchor=(1, 1))
        
        # Rotacionar os rótulos dos estados
        ax.set_xticklabels(pivot_table.index, rotation=90)
        
        # Ajustar o layout para não cortar a legenda
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        
        # Ajustar o espaço entre as barras
        ax.margins(y=0.1)
        
        # Definir o limite do eixo y para evitar que as colunas de maiores valores vazem pela parte de cima do gráfico
        max_height = pivot_table.max().max()
        ax.set_ylim(0, max_height * 1.1)
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
#--------------------------------26-------------------------------------------------------------------------------------------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Abrindo o arquivo de dados
enem_data = pd.read_csv('MICRODADOS_ENEM_2022 - Copia.csv', sep=',', encoding='latin-1')

# Subtítulo para o gráfico
st.subheader('Quantidade de Pessoas por Estado e Raça/Cor')

# Dicionário para mapeamento de raça/cor
raca_cor_dict = {
    0: 'Não declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena'
}

# Ordenar as raças/cores em ordem dos valores do dicionário
racas_unicas = [raca_cor_dict[key] for key in sorted(raca_cor_dict.keys())]

# Multiselect para selecionar as raças/cores
racas_selecionadas = st.multiselect('Selecione até 3 Raças/Cores:', racas_unicas, key="racas")

if len(racas_selecionadas) > 3:
    st.error("Por favor, selecione no máximo 3 raças/cores.")
else:
    if len(racas_selecionadas) == 0:
        st.write("Por favor, selecione pelo menos uma raça/cor.")
    else:
        # Filtrar os dados com base nas raças selecionadas
        dados_filtrados = enem_data[enem_data['TP_COR_RACA'].isin([key for key, value in raca_cor_dict.items() if value in racas_selecionadas])]
        
        # Criar uma tabela dinâmica (pivot table) para contar o número de pessoas por estado e raça/cor
        pivot_table = dados_filtrados.pivot_table(index='SG_UF_PROVA', columns='TP_COR_RACA', aggfunc='size', fill_value=0)
        
        # Reordenar as raças/cores conforme o dicionário
        pivot_table = pivot_table.rename(columns=raca_cor_dict)
        
        # Plotar o gráfico de barras
        fig, ax = plt.subplots(figsize=(12, 8))
        pivot_table.plot(kind='bar', ax=ax, stacked=False)
        
        # Adicionar os valores das colunas acima das barras com rotação de 90 graus
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                fontsize = 10 - len(racas_selecionadas)  # Ajuste do tamanho da fonte
                ax.annotate(f'{int(height)}', 
                            xy=(p.get_x() + p.get_width() / 2, height),
                            xytext=(0, 3), 
                            textcoords='offset points',
                            ha='center', va='bottom', rotation=90, fontsize=fontsize)
        
        # Configurar o título do gráfico e rótulos dos eixos
        ax.set_title('Quantidade de Pessoas por Estado e Raça/Cor')
        ax.set_xlabel('Estado')
        ax.set_ylabel('Quantidade de Pessoas')
        
        # Colocar a legenda fora do gráfico
        ax.legend(title='Raça/Cor', loc='upper left', bbox_to_anchor=(1, 1))
        
        # Rotacionar os rótulos dos estados
        ax.set_xticklabels(pivot_table.index, rotation=90)
        
        # Ajustar o layout para não cortar a legenda
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        
        # Ajustar o espaço entre as barras
        ax.margins(y=0.1)
        
        # Definir o limite do eixo y para evitar que as colunas de maiores valores vazem pela parte de cima do gráfico
        max_height = pivot_table.max().max()
        ax.set_ylim(0, max_height * 1.1)
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)

#--------------------------------27-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Subtítulo para o gráfico
st.subheader('Quantidade de Pessoas por Estado e Sexo')

# Ordenar os sexos em ordem dos valores do dicionário
sexos_unicos = [genero_dict[key] for key in sorted(genero_dict.keys())]

# Multiselect para selecionar os sexos
sexos_selecionados = st.multiselect('Selecione até 2 Sexos:', sexos_unicos, key="sexos")

if len(sexos_selecionados) > 2:
    st.error("Por favor, selecione no máximo 2 sexos.")
else:
    if len(sexos_selecionados) == 0:
        st.write("Por favor, selecione pelo menos um sexo.")
    else:
        # Mapear os sexos selecionados de volta para os valores do dicionário
        sexos_selecionados = [key for key, value in genero_dict.items() if value in sexos_selecionados]
        
        # Filtrar os dados com base nos sexos selecionados
        dados_filtrados = enem_data[enem_data['TP_SEXO'].isin(sexos_selecionados)]
        
        # Criar uma tabela dinâmica (pivot table) para contar o número de pessoas por estado e sexo
        pivot_table = dados_filtrados.pivot_table(index='SG_UF_PROVA', columns='TP_SEXO', aggfunc='size', fill_value=0)
        
        # Reordenar os sexos conforme o dicionário
        pivot_table = pivot_table.rename(columns=genero_dict)
        
        # Plotar o gráfico de barras
        fig, ax = plt.subplots(figsize=(12, 8))
        pivot_table.plot(kind='bar', ax=ax, stacked=False)
        
        # Adicionar os valores das colunas acima das barras com rotação de 90 graus
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f'{int(height)}', 
                            xy=(p.get_x() + p.get_width() / 2, height),
                            xytext=(0, 3), 
                            textcoords='offset points',
                            ha='center', va='bottom', rotation=90)
        
        # Configurar o título do gráfico e rótulos dos eixos
        ax.set_title('Quantidade de Pessoas por Estado e Sexo')
        ax.set_xlabel('Estado')
        ax.set_ylabel('Quantidade de Pessoas')
        
        # Colocar a legenda fora do gráfico
        ax.legend(title='Sexo', loc='upper left', bbox_to_anchor=(1, 1))
        
        # Rotacionar os rótulos dos estados
        ax.set_xticklabels(pivot_table.index, rotation=90)
        
        # Ajustar o layout para não cortar a legenda
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        
        # Ajustar o espaço entre as barras
        ax.margins(y=0.1)
        
        # Definir o limite do eixo y para evitar que as colunas de maiores valores vazem pela parte de cima do gráfico
        max_height = pivot_table.max().max()
        ax.set_ylim(0, max_height * 1.1)
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)
#--------------------------------28-------------------------------------------------------------------------------------------------------------------------------------------------------------

# Subtítulo para o gráfico
st.subheader('Quantidade de Pessoas por Estado e Tipo de Escola')

# Ordenar os tipos de escola em ordem dos valores do dicionário
tipos_escola_unicos = [tipo_escola_dict[key] for key in sorted(tipo_escola_dict.keys())]

# Multiselect para selecionar os tipos de escola
tipos_escola_selecionados = st.multiselect('Selecione o Tipo de Escola:', tipos_escola_unicos, key="tipos_escola")

if len(tipos_escola_selecionados) > 3:
    st.error()
else:
    if len(tipos_escola_selecionados) == 0:
        st.write("Por favor, selecione pelo menos um tipo de escola.")
    else:
        # Mapear os tipos de escola selecionados de volta para os valores do dicionário
        tipos_escola_selecionados = [key for key, value in tipo_escola_dict.items() if value in tipos_escola_selecionados]
        
        # Filtrar os dados com base nos tipos de escola selecionados
        dados_filtrados = enem_data[enem_data['TP_ESCOLA'].isin(tipos_escola_selecionados)]
        
        # Criar uma tabela dinâmica (pivot table) para contar o número de pessoas por estado e tipo de escola
        pivot_table = dados_filtrados.pivot_table(index='SG_UF_PROVA', columns='TP_ESCOLA', aggfunc='size', fill_value=0)
        
        # Reordenar os tipos de escola conforme o dicionário
        pivot_table = pivot_table.rename(columns=tipo_escola_dict)
        
        # Plotar o gráfico de barras
        fig, ax = plt.subplots(figsize=(12, 8))
        pivot_table.plot(kind='bar', ax=ax, stacked=False)
        
        # Adicionar os valores das colunas acima das barras com rotação de 90 graus
        for p in ax.patches:
            height = p.get_height()
            if height > 0:
                ax.annotate(f'{int(height)}', 
                            xy=(p.get_x() + p.get_width() / 2, height),
                            xytext=(0, 3), 
                            textcoords='offset points',
                            ha='center', va='bottom', rotation=90)
        
        # Configurar o título do gráfico e rótulos dos eixos
        ax.set_title('Quantidade de Pessoas por Estado e Tipo de Escola')
        ax.set_xlabel('Estado')
        ax.set_ylabel('Quantidade de Pessoas')
        
        # Colocar a legenda fora do gráfico
        ax.legend(title='Tipo de Escola', loc='upper left', bbox_to_anchor=(1, 1))
        
        # Rotacionar os rótulos dos estados
        ax.set_xticklabels(pivot_table.index, rotation=90)
        
        # Ajustar o layout para não cortar a legenda
        plt.tight_layout(rect=[0, 0, 0.85, 1])
        
        # Ajustar o espaço entre as barras
        ax.margins(y=0.1)
        
        # Definir o limite do eixo y para evitar que as colunas de maiores valores vazem pela parte de cima do gráfico
        max_height = pivot_table.max().max()
        ax.set_ylim(0, max_height * 1.1)
        
        # Mostrar o gráfico no Streamlit
        st.pyplot(fig)

#--------------------------------29-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dicionário de cores para cada estado
cores_estados = {
    'AC': 'blue',
    'AL': 'red',
    'AP': 'green',
    'AM': 'orange',
    'BA': 'purple',
    'CE': 'brown',
    'DF': 'pink',
    'ES': 'gray',
    'GO': 'olive',
    'MA': 'cyan',
    'MT': 'magenta',
    'MS': 'lime',
    'MG': 'teal',
    'PA': 'navy',
    'PB': 'peru',
    'PR': 'rosybrown',
    'PE': 'slategray',
    'PI': 'springgreen',
    'RJ': 'tan',
    'RN': 'tomato',
    'RS': 'violet',
    'RO': 'yellow',
    'RR': 'chocolate',
    'SC': 'orchid',
    'SP': 'darkorange',
    'SE': 'skyblue',
    'TO': 'salmon',
}

st.subheader('Gráfico de dispersão por estado')

# Seleção dos estados
selecao_opcao = st.multiselect('Selecione os estados (até 5)', ['AC',
    'AL',
    'AP',
    'AM',
    'BA',
    'CE',
    'DF',
    'ES',
    'GO',
    'MA',
    'MT',
    'MS',
    'MG',
    'PA',
    'PB',
    'PR',
    'PE',
    'PI',
    'RJ',
    'RN',
    'RS',
    'RO',
    'RR',
    'SC',
    'SP',
    'SE',
    'TO'])

# Limitando a seleção a no máximo 5 estados
if len(selecao_opcao) > 5:
    st.warning("Por favor, selecione no máximo 5 estados.")
    selecao_opcao = selecao_opcao[:5]

selecao_var_x = st.selectbox('Selecione a variável para o eixo X', ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'])

selecao_var_y = st.selectbox('Selecione a variável para o eixo Y', ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'])

visualizar_toda_escala = st.checkbox('Visualizar toda a escala do gráfico')

# Criando um gráfico de dispersão
fig, ax = plt.subplots()
for sel_epc in selecao_opcao:
    df1 = enem_data[(enem_data.SG_UF_PROVA == sel_epc) & (enem_data[selecao_var_x] != 0) & (enem_data[selecao_var_y] != 0)]
    ax.scatter(df1[selecao_var_x], df1[selecao_var_y], alpha=0.5, label=sel_epc, color=cores_estados[sel_epc])
if visualizar_toda_escala:
    ax.set_xlim(0, 1.1*enem_data[selecao_var_x].max())
    ax.set_ylim(0, 1.1*enem_data[selecao_var_y].max())
ax.set_xlabel(selecao_var_x)
ax.set_ylabel(selecao_var_y) 
ax.legend(title='Estados', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

ax.set_title(f'Dispersão {selecao_var_x} x {selecao_var_y} para os estados: {" ".join(selecao_opcao)}')

st.pyplot(fig)

#--------------------------------30-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dicionário de cor/raça
cor_raca_dict = {
    0: 'Não declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena'
}

st.subheader('Gráfico de dispersão por Cor/Raça')

# Seleção das cor/raça
selecao_opcao = st.multiselect('Selecione as cor/raça (até 5)', cor_raca_dict.keys(), format_func=lambda x: cor_raca_dict[x], key='cor_raca_multiselect')

# Limitando a seleção a no máximo 5 cor/raça
if len(selecao_opcao) > 5:
    st.warning("Por favor, selecione no máximo 5 opções.")
    selecao_opcao = selecao_opcao[:5]

selecao_var_x = st.selectbox('Selecione a variável para o eixo X', ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_x_selectbox')

selecao_var_y = st.selectbox('Selecione a variável para o eixo Y', ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_y_selectbox')

visualizar_toda_escala = st.checkbox('Visualizar toda a escala do gráfico', key='escala_checkbox')

# Criando um gráfico de dispersão
fig, ax = plt.subplots()
for cor_raca in selecao_opcao:
    df1 = enem_data[(enem_data['TP_COR_RACA'] == cor_raca) & (enem_data[selecao_var_x] != 0) & (enem_data[selecao_var_y] != 0)]
    ax.scatter(df1[selecao_var_x], df1[selecao_var_y], alpha=0.5, label=cor_raca_dict[cor_raca])
if visualizar_toda_escala:
    ax.set_xlim(0, 1.1*enem_data[selecao_var_x].max())
    ax.set_ylim(0, 1.1*enem_data[selecao_var_y].max())
ax.set_xlabel(selecao_var_x)
ax.set_ylabel(selecao_var_y) 
ax.legend(title='Cor/Raça', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

ax.set_title(f'Dispersão {selecao_var_x} x {selecao_var_y} para as Cor/Raça selecionadas')

st.pyplot(fig)

#--------------------------------31-------------------------------------------------------------------------------------------------------------------------------------------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Abrindo o arquivo de dados
enem_data = pd.read_csv('MICRODADOS_ENEM_2022 - Copia.csv', sep=',', encoding='latin-1')

# Dicionário de tipos de escola
tipo_escola_dict = {
    1: 'Não Respondeu',
    2: 'Pública',
    3: 'Privada'
}

st.subheader('Gráfico de dispersão por Tipo de Escola')

# Seleção do tipo de escola
selecao_opcao = st.multiselect('Selecione o tipo de escola', tipo_escola_dict.keys(), format_func=lambda x: tipo_escola_dict[x], key='tipo_escola_multiselect')

# Limitando a seleção a no máximo 5 tipos de escola
if len(selecao_opcao) > 5:
    st.warning("Por favor, selecione no máximo 5 opções.")
    selecao_opcao = selecao_opcao[:5]

selecao_var_x = st.selectbox('Selecione a variável para o eixo X', ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_x_selectbox_tipo_escola')

selecao_var_y = st.selectbox('Selecione a variável para o eixo Y', ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_y_selectbox_tipo_escola')

visualizar_toda_escala = st.checkbox('Visualizar toda a escala do gráfico', key='escala_checkbox_tipo_escola')

# Criando um gráfico de dispersão
fig, ax = plt.subplots()
for tipo_escola in selecao_opcao:
    df1 = enem_data[(enem_data['TP_ESCOLA'] == tipo_escola) & (enem_data[selecao_var_x] != 0) & (enem_data[selecao_var_y] != 0)]
    ax.scatter(df1[selecao_var_x], df1[selecao_var_y], alpha=0.5, label=tipo_escola_dict[tipo_escola])
if visualizar_toda_escala:
    ax.set_xlim(0, 1.1*enem_data[selecao_var_x].max())
    ax.set_ylim(0, 1.1*enem_data[selecao_var_y].max())
ax.set_xlabel(selecao_var_x)
ax.set_ylabel(selecao_var_y) 
ax.legend(title='Tipo de Escola', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

ax.set_title(f'Dispersão {selecao_var_x} x {selecao_var_y} para os tipos de escola selecionados')

st.pyplot(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dicionário de sexo
sexo_dict = {
    'M': 'Masculino',
    'F': 'Feminino'
}

st.subheader('Gráfico de dispersão por Sexo')

# Seleção do sexo
selecao_opcao = st.multiselect('Selecione o Sexo', sexo_dict.keys(), format_func=lambda x: sexo_dict[x], key='sexo_multiselect_unique')

# Limitando a seleção a no máximo 2 sexos
if len(selecao_opcao) > 2:
    st.warning("Por favor, selecione no máximo 2 opções.")
    selecao_opcao = selecao_opcao[:2]

selecao_var_x = st.selectbox('Selecione a variável para o eixo X', ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_x_selectbox_sexo_unique')

selecao_var_y = st.selectbox('Selecione a variável para o eixo Y', ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_y_selectbox_sexo_unique')

visualizar_toda_escala = st.checkbox('Visualizar toda a escala do gráfico', key='escala_checkbox_sexo_unique')

# Criando um gráfico de dispersão
fig, ax = plt.subplots()
for sexo in selecao_opcao:
    df1 = enem_data[(enem_data['TP_SEXO'] == sexo) & (enem_data[selecao_var_x] != 0) & (enem_data[selecao_var_y] != 0)]
    ax.scatter(df1[selecao_var_x], df1[selecao_var_y], alpha=0.5, label=sexo_dict[sexo])
if visualizar_toda_escala:
    ax.set_xlim(0, 1.1*enem_data[selecao_var_x].max())
    ax.set_ylim(0, 1.1*enem_data[selecao_var_y].max())
ax.set_xlabel(selecao_var_x)
ax.set_ylabel(selecao_var_y) 
ax.legend(title='Sexo', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

ax.set_title(f'Dispersão {selecao_var_x} x {selecao_var_y} para os Sexos selecionados')

st.pyplot(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Dicionário para mapeamento da faixa etária
faixa_etaria_dict = {
    1: 'Menor de 17 anos',
    2: '17 anos',
    3: '18 anos',
    4: '19 anos',
    5: '20 anos',
    6: '21 anos',
    7: '22 anos',
    8: '23 anos',
    9: '24 anos',
    10: '25 anos',
    11: 'Entre 26 e 30 anos',
    12: 'Entre 31 e 35 anos',
    13: 'Entre 36 e 40 anos',
    14: 'Entre 41 e 45 anos',
    15: 'Entre 46 e 50 anos',
    16: 'Entre 51 e 55 anos',
    17: 'Entre 56 e 60 anos',
    18: 'Entre 61 e 65 anos',
    19: 'Entre 66 e 70 anos',
    20: 'Maior de 70 anos'
}

st.subheader('Gráfico de dispersão por Faixa Etária')

# Seleção da faixa etária
selecao_opcao = st.multiselect('Selecione a Faixa Etária', faixa_etaria_dict.keys(), format_func=lambda x: faixa_etaria_dict[x], key='faixa_etaria_multiselect_unique')

# Limitando a seleção a no máximo 5 faixas etárias
if len(selecao_opcao) > 5:
    st.warning("Por favor, selecione no máximo 5 opções.")
    selecao_opcao = selecao_opcao[:5]

selecao_var_x = st.selectbox('Selecione a variável para o eixo X', ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_x_selectbox_faixa_etaria')

selecao_var_y = st.selectbox('Selecione a variável para o eixo Y', ['NU_NOTA_CN','NU_NOTA_CH','NU_NOTA_LC','NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_y_selectbox_faixa_etaria')

visualizar_toda_escala = st.checkbox('Visualizar toda a escala do gráfico', key='escala_checkbox_faixa_etaria')

# Criando um gráfico de dispersão
fig, ax = plt.subplots()
for faixa_etaria in selecao_opcao:
    df1 = enem_data[(enem_data['TP_FAIXA_ETARIA'] == faixa_etaria) & (enem_data[selecao_var_x] != 0) & (enem_data[selecao_var_y] != 0)]
    ax.scatter(df1[selecao_var_x], df1[selecao_var_y], alpha=0.5, label=faixa_etaria_dict[faixa_etaria])
if visualizar_toda_escala:
    ax.set_xlim(0, 1.1*enem_data[selecao_var_x].max())
    ax.set_ylim(0, 1.1*enem_data[selecao_var_y].max())
ax.set_xlabel(selecao_var_x)
ax.set_ylabel(selecao_var_y) 
ax.legend(title='Faixa Etária', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

ax.set_title(f'Dispersão {selecao_var_x} x {selecao_var_y} para as Faixas Etárias selecionadas')

st.pyplot(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Dicionário para mapeamento do ano de conclusão
ano_concluiu_dict = {
    0: 'Não informado',
    1: '2021',
    2: '2020',
    3: '2019',
    4: '2018',
    5: '2017',
    6: '2016',
    7: '2015',
    8: '2014',
    9: '2013',
    10: '2012',
    11: '2011',
    12: '2010',
    13: '2009',
    14: '2008',
    15: '2007',
    16: 'Antes de 2007'
}

st.subheader('Gráfico de dispersão por Ano de Conclusão')

# Seleção do ano de conclusão
selecao_opcao = st.multiselect('Selecione o Ano de Conclusão', ano_concluiu_dict.keys(), format_func=lambda x: ano_concluiu_dict[x], key='ano_concluiu_multiselect_unique')

# Limitando a seleção a no máximo 5 anos de conclusão
if len(selecao_opcao) > 5:
    st.warning("Por favor, selecione no máximo 5 opções.")
    selecao_opcao = selecao_opcao[:5]

selecao_var_x = st.selectbox('Selecione a variável para o eixo X', ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_x_selectbox_ano_concluiu')

selecao_var_y = st.selectbox('Selecione a variável para o eixo Y', ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_y_selectbox_ano_concluiu')

visualizar_toda_escala = st.checkbox('Visualizar toda a escala do gráfico', key='escala_checkbox_ano_concluiu')

# Criando um gráfico de dispersão
fig, ax = plt.subplots()
for ano_concluiu in selecao_opcao:
    df1 = enem_data[(enem_data['TP_ANO_CONCLUIU'] == ano_concluiu) & (enem_data[selecao_var_x] != 0) & (enem_data[selecao_var_y] != 0)]
    ax.scatter(df1[selecao_var_x], df1[selecao_var_y], alpha=0.5, label=ano_concluiu_dict[ano_concluiu])
if visualizar_toda_escala:
    ax.set_xlim(0, 1.1*enem_data[selecao_var_x].max())
    ax.set_ylim(0, 1.1*enem_data[selecao_var_y].max())
ax.set_xlabel(selecao_var_x)
ax.set_ylabel(selecao_var_y) 
ax.legend(title='Ano de Conclusão', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

ax.set_title(f'Dispersão {selecao_var_x} x {selecao_var_y} para os Anos de Conclusão selecionados')

st.pyplot(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Dicionário para mapeamento da renda
renda_dict = {
    'A': 'Nenhuma Renda',
    'B': 'Até R$ 1.212,00',
    'C': 'De R$ 1.212,01 até R$ 1.818,00',
    'D': 'De R$ 1.818,01 até R$ 2.424,00',
    'E': 'De R$ 2.424,01 até R$ 3.030,00',
    'F': 'De R$ 3.030,01 até R$ 3.636,00',
    'G': 'De R$ 3.636,01 até R$ 4.848,00',
    'H': 'De R$ 4.848,01 até R$ 6.060,00',
    'I': 'De R$ 6.060,01 até R$ 7.272,00',
    'J': 'De R$ 7.272,01 até R$ 8.484,00',
    'K': 'De R$ 8.484,01 até R$ 9.696,00',
    'L': 'De R$ 9.696,01 até R$ 10.908,00',
    'M': 'De R$ 10.908,01 até R$ 12.120,00',
    'N': 'De R$ 12.120,01 até R$ 14.544,00',
    'O': 'De R$ 14.544,01 até R$ 18.180,00',
    'P': 'De R$ 18.180,01 até R$ 24.240,00',
    'Q': 'Acima de R$ 24.240,00'
}

st.subheader('Gráfico de dispersão por Faixa de Renda')

# Seleção da faixa de renda
selecao_opcao = st.multiselect('Selecione a Faixa de Renda', renda_dict.keys(), format_func=lambda x: renda_dict[x], key='renda_multiselect_unique')

# Limitando a seleção a no máximo 5 faixas de renda
if len(selecao_opcao) > 5:
    st.warning("Por favor, selecione no máximo 5 opções.")
    selecao_opcao = selecao_opcao[:5]

selecao_var_x = st.selectbox('Selecione a variável para o eixo X', ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_x_selectbox_renda')

selecao_var_y = st.selectbox('Selecione a variável para o eixo Y', ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_y_selectbox_renda')

visualizar_toda_escala = st.checkbox('Visualizar toda a escala do gráfico', key='escala_checkbox_renda')

# Criando um gráfico de dispersão
fig, ax = plt.subplots()
for renda in selecao_opcao:
    df1 = enem_data[(enem_data['Q006'] == renda) & (enem_data[selecao_var_x] != 0) & (enem_data[selecao_var_y] != 0)]
    ax.scatter(df1[selecao_var_x], df1[selecao_var_y], alpha=0.5, label=renda_dict[renda])
if visualizar_toda_escala:
    ax.set_xlim(0, 1.1*enem_data[selecao_var_x].max())
    ax.set_ylim(0, 1.1*enem_data[selecao_var_y].max())
ax.set_xlabel(selecao_var_x)
ax.set_ylabel(selecao_var_y) 
ax.legend(title='Faixa de Renda', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

ax.set_title(f'Dispersão {selecao_var_x} x {selecao_var_y} para as Faixas de Renda selecionadas')

st.pyplot(fig)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dicionário para mapeamento do uso de internet em casa
internet_dict = {
    'A': 'Não',
    'B': 'Sim'
}

st.subheader('Gráfico de dispersão por acesso à Internet em casa')

# Seleção do acesso à internet
selecao_opcao = st.multiselect('Selecione o acesso à Internet em casa', internet_dict.keys(), format_func=lambda x: internet_dict[x], key='internet_multiselect_unique')

# Limitando a seleção a no máximo 2 opções
if len(selecao_opcao) > 2:
    st.warning("Por favor, selecione no máximo 2 opções.")
    selecao_opcao = selecao_opcao[:2]

selecao_var_x = st.selectbox('Selecione a variável para o eixo X', ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_x_selectbox_internet')

selecao_var_y = st.selectbox('Selecione a variável para o eixo Y', ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_y_selectbox_internet')

visualizar_toda_escala = st.checkbox('Visualizar toda a escala do gráfico', key='escala_checkbox_internet')

# Criando um gráfico de dispersão
fig, ax = plt.subplots()
for internet in selecao_opcao:
    df1 = enem_data[(enem_data['Q025'] == internet) & (enem_data[selecao_var_x] != 0) & (enem_data[selecao_var_y] != 0)]
    ax.scatter(df1[selecao_var_x], df1[selecao_var_y], alpha=0.5, label=internet_dict[internet])
if visualizar_toda_escala:
    ax.set_xlim(0, 1.1*enem_data[selecao_var_x].max())
    ax.set_ylim(0, 1.1*enem_data[selecao_var_y].max())
ax.set_xlabel(selecao_var_x)
ax.set_ylabel(selecao_var_y) 
ax.legend(title='Acesso à Internet', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

ax.set_title(f'Dispersão {selecao_var_x} x {selecao_var_y} para acesso à Internet selecionado')

st.pyplot(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Dicionário para mapeamento da localização da escola
localizacao_dict = {
    1: 'Urbana',
    2: 'Rural'
}

st.subheader('Gráfico de dispersão por localização da escola')

# Seleção da localização da escola
selecao_opcao = st.multiselect('Selecione a localização da escola', localizacao_dict.keys(), format_func=lambda x: localizacao_dict[x], key='localizacao_multiselect_unique')

# Limitando a seleção a no máximo 2 opções
if len(selecao_opcao) > 2:
    st.warning("Por favor, selecione no máximo 2 opções.")
    selecao_opcao = selecao_opcao[:2]

selecao_var_x = st.selectbox('Selecione a variável para o eixo X', ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_x_selectbox_localizacao')

selecao_var_y = st.selectbox('Selecione a variável para o eixo Y', ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_y_selectbox_localizacao')

visualizar_toda_escala = st.checkbox('Visualizar toda a escala do gráfico', key='escala_checkbox_localizacao')

# Criando um gráfico de dispersão
fig, ax = plt.subplots()
for localizacao in selecao_opcao:
    df1 = enem_data[(enem_data['TP_LOCALIZACAO_ESC'] == localizacao) & (enem_data[selecao_var_x] != 0) & (enem_data[selecao_var_y] != 0)]
    ax.scatter(df1[selecao_var_x], df1[selecao_var_y], alpha=0.5, label=localizacao_dict[localizacao])
if visualizar_toda_escala:
    ax.set_xlim(0, 1.1*enem_data[selecao_var_x].max())
    ax.set_ylim(0, 1.1*enem_data[selecao_var_y].max())
ax.set_xlabel(selecao_var_x)
ax.set_ylabel(selecao_var_y) 
ax.legend(title='Localização da Escola', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

ax.set_title(f'Dispersão {selecao_var_x} x {selecao_var_y} para localização da escola selecionada')

st.pyplot(fig)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dicionário para mapeamento da dependência administrativa da escola
dependencia_adm_dict = {
    1: 'Federal',
    2: 'Estadual',
    3: 'Municipal',
    4: 'Privada'
}

st.subheader('Gráfico de dispersão por dependência administrativa da escola')

# Seleção da dependência administrativa da escola
selecao_opcao = st.multiselect('Selecione a dependência administrativa da escola', dependencia_adm_dict.keys(), format_func=lambda x: dependencia_adm_dict[x], key='dependencia_adm_multiselect_unique')

# Limitando a seleção a no máximo 4 opções
if len(selecao_opcao) > 4:
    st.warning("Por favor, selecione no máximo 4 opções.")
    selecao_opcao = selecao_opcao[:4]

selecao_var_x = st.selectbox('Selecione a variável para o eixo X', ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_x_selectbox_dependencia_adm')

selecao_var_y = st.selectbox('Selecione a variável para o eixo Y', ['NU_NOTA_CN', 'NU_NOTA_CH', 'NU_NOTA_LC', 'NU_NOTA_MT', 'NU_NOTA_REDACAO', 'MEDIA_TOTAL'], key='var_y_selectbox_dependencia_adm')

visualizar_toda_escala = st.checkbox('Visualizar toda a escala do gráfico', key='escala_checkbox_dependencia_adm')

# Criando um gráfico de dispersão
fig, ax = plt.subplots()
for dependencia_adm in selecao_opcao:
    df1 = enem_data[(enem_data['TP_DEPENDENCIA_ADM_ESC'] == dependencia_adm) & (enem_data[selecao_var_x] != 0) & (enem_data[selecao_var_y] != 0)]
    ax.scatter(df1[selecao_var_x], df1[selecao_var_y], alpha=0.5, label=dependencia_adm_dict[dependencia_adm])
if visualizar_toda_escala:
    ax.set_xlim(0, 1.1*enem_data[selecao_var_x].max())
    ax.set_ylim(0, 1.1*enem_data[selecao_var_y].max())
ax.set_xlabel(selecao_var_x)
ax.set_ylabel(selecao_var_y)
ax.legend(title='Dependência Administrativa', bbox_to_anchor=(1.05, 1), loc='upper left')
ax.grid(True)

ax.set_title(f'Dispersão {selecao_var_x} x {selecao_var_y} para dependência administrativa selecionada')

st.pyplot(fig)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
