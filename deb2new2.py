import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import re

# Show all rows
pd.set_option('display.max_rows', None)

# Show all columns
pd.set_option('display.max_columns', None)


#read the file in the directory
deb2 = pd.read_excel("p2_deb.xlsx")






# 1 Proporção de Escaladores que já se lesionaram vs Frequenica de escalada


# Definir a ordem desejada para as categorias de frequência de escalada, sem o outlier
ordem_freq = [
    "Menos de uma vez por semana",
    "Uma vez por semana",
    "De 2 a 3 vezes por semana",
    "De 4 a 5 vezes por semana"
]

# Filtrar os dados para remover o outlier "Mais de 5 vezes na semana"
deb2_filtrado = deb2[deb2['freq_esc'].isin(ordem_freq)]

# Garantir que a coluna freq_esc siga a ordem definida no conjunto filtrado
deb2_filtrado['freq_esc'] = pd.Categorical(deb2_filtrado['freq_esc'], categories=ordem_freq, ordered=True)

# Calcular a proporção de lesão dentro de cada grupo de frequência de escalada
freq_lesionou = deb2_filtrado.groupby(['freq_esc', 'ja_lesionou']).size().unstack(fill_value=0)
freq_lesionou = freq_lesionou.loc[freq_lesionou.sum(axis=1) > 0]  # Remover categorias sem valores
freq_lesionou = freq_lesionou.div(freq_lesionou.sum(axis=1), axis=0)  # Converter para proporções

# Plotar o gráfico de barras empilhado com proporções
ax = freq_lesionou.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'], figsize=(10, 6), width=0.7)

# Personalizar o gráfico
plt.title('Proporção de Incidência de Lesão por Frequência de Escalada (Excluindo Outlier)')
plt.ylabel('Proporção de Escaladores')
plt.xlabel('Frequência de Escalada')
plt.xticks(rotation=45, ha='right')

# Adicionar uma nota na legenda sobre o valor atípico
handles, labels = ax.get_legend_handles_labels()
labels = ['Não', 'Sim', 'Outlier: Mais de 5 vezes na semana']
plt.legend(handles=handles, labels=labels, title='Já se lesionou', loc='upper left', bbox_to_anchor=(1, 1))

# Ajustar o layout para melhor visualização
plt.tight_layout()

# Mostrar o gráfico
plt.show()


#______________________________________________________

# 2 Proporção de Incidência de Lesão por Tempo de Sono

# Definir a ordem desejada para as categorias de tempo de sono
ordem_sono = [
    "Menos de 6", "6 horas", "7 horas", 
    "Entre 7 e 8 horas", "8 horas", "9 horas"
]

# Garantir que a coluna h_dorme siga essa ordem
deb2['h_dorme'] = pd.Categorical(deb2['h_dorme'], categories=ordem_sono, ordered=True)

# Calcular a proporção de lesões dentro de cada grupo de tempo de sono
sono_lesionou = deb2.groupby(['h_dorme', 'ja_lesionou']).size().unstack(fill_value=0)
sono_lesionou = sono_lesionou.div(sono_lesionou.sum(axis=1), axis=0)  # Converter para proporções

# Plotar o gráfico de barras empilhado com proporções
sono_lesionou.plot(kind='bar', stacked=True, color=['skyblue', 'salmon'], figsize=(10, 6))

# Personalizar o gráfico
plt.title('Proporção de Incidência de Lesão por Tempo de Sono')
plt.xlabel('')
plt.ylabel('Proporção de Escaladores')
plt.xticks(rotation=45)
plt.legend(title='Já se lesionou', labels=['Não', 'Sim'])
plt.tight_layout()

# Mostrar o gráfico
plt.show()

#____________________________________________________

# 3 Distribuição do Tempo para a Primeira Lesão por Tempo de Escalada

# Ordens definidas para as categorias de tempo de escalada e tempo para a primeira lesão
ordem_tempo_esc = [
    "Menos de um ano", "1 - 2 anos", "3 - 5 anos", "6 - 10 anos", 
    "11 - 20 anos", "Mais de 20 anos", "Mais de 30 anos"
]

ordem_primeira_lesao = [
    "Menos de um ano", "De 1 a 2 anos", "De 3 a 5 anos", "Mais de 5 anos"
]

# Garantir que as colunas sigam a ordem especificada
deb2['tempo_esc'] = pd.Categorical(deb2['tempo_esc'], categories=ordem_tempo_esc, ordered=True)
deb2['primeira_lesao_esc'] = pd.Categorical(deb2['primeira_lesao_esc'], categories=ordem_primeira_lesao, ordered=True)

# Contar a frequência de cada combinação de tempo de escalada e tempo para a primeira lesão
contagem_lesao = pd.crosstab(deb2['tempo_esc'], deb2['primeira_lesao_esc'])

# Plotar o heatmap com matplotlib
plt.figure(figsize=(10, 6))
plt.imshow(contagem_lesao, cmap="YlGnBu", aspect='auto')

# Adicionar rótulos nos eixos
plt.xticks(range(len(contagem_lesao.columns)), contagem_lesao.columns, rotation=45, ha='right')
plt.yticks(range(len(contagem_lesao.index)), contagem_lesao.index)
plt.colorbar(label='Número de Escaladores')

# Adicionar contagens nas células
for i in range(len(contagem_lesao.index)):
    for j in range(len(contagem_lesao.columns)):
        plt.text(j, i, contagem_lesao.iloc[i, j], ha='center', va='center', color='black')

# Título e ajustes finais
plt.title('Distribuição do Tempo para a Primeira Lesão por Tempo de Escalada')
plt.xlabel('Tempo para a Primeira Lesão')
plt.ylabel('Tempo de Escalada')
plt.tight_layout()

# Mostrar o gráfico
plt.show()
#___________________________________________________

# 4 Distribuição de Consumo de Ultraprocessados por Padrão Alimentar

# Substituir o valor na coluna 'padrao_alimentar'
deb2['padrao_alimentar'] = deb2['padrao_alimentar'].replace(
    'Onívoro (se alimenta tanto de matéria vegetal como animal)', 'Onívoro'
)

# Contar a frequência de cada combinação entre padrão alimentar e consumo de ultraprocessados
freq_data = pd.crosstab(deb2['padrao_alimentar'], deb2['ultra_process'])

# Plotar o heatmap com matplotlib
plt.figure(figsize=(10, 6))
plt.imshow(freq_data, cmap="YlGnBu", aspect='auto')

# Adicionar rótulos nos eixos
plt.xticks(range(len(freq_data.columns)), freq_data.columns, rotation=45)
plt.yticks(range(len(freq_data.index)), freq_data.index)
plt.colorbar(label='Número de Escaladores')

# Anotar as contagens nas células
for i in range(len(freq_data.index)):
    for j in range(len(freq_data.columns)):
        plt.text(j, i, freq_data.iloc[i, j], ha='center', va='center', color='black')

# Título e ajustes finais
plt.title('Distribuição de Consumo de Ultraprocessados por Padrão Alimentar')
plt.xlabel('Consumo de Ultraprocessados')
plt.ylabel('Padrão Alimentar')
plt.tight_layout()

# Mostrar o gráfico
plt.show()

#__________________________________________

# 5 Incidência Proporcional de Lesão por Gênero

# Calcular a tabela de contingência normalizada para proporções
freq_genero_lesao = pd.crosstab(deb2['genero'], deb2['ja_lesionou'], normalize='index') * 100

# Plotar o gráfico de barras empilhadas com proporções
freq_genero_lesao.plot(kind='bar', stacked=True, figsize=(8, 6), color=['#66c2a5', '#fc8d62'])

# Personalizar o gráfico
plt.title('Incidência Proporcional de Lesão por Gênero')
plt.xlabel('')
plt.ylabel('Proporção de Escaladores (%)')
plt.legend(title='Já se lesionou', labels=['Não', 'Sim'])
plt.xticks(rotation=0)
plt.tight_layout()

# Mostrar o gráfico
plt.show()

#______________________________________________

# 6 Proporção de Frequência de Escalada por Gênero

# Definir a ordem crescente para 'freq_esc'
ordem_freq_esc = [
    'Menos de uma vez por semana', 
    'Uma vez por semana', 
    'De 2 a 3 vezes por semana', 
    'De 4 a 5 vezes por semana', 
    'Mais de 5 vezes na semana'
]

deb2['freq_esc'] = pd.Categorical(deb2['freq_esc'], categories=ordem_freq_esc, ordered=True)

# Calcular a tabela de contingência normalizada para proporções
freq_genero_freq_esc = pd.crosstab(deb2['genero'], deb2['freq_esc'], normalize='index') * 100

# Plotar o gráfico de barras empilhadas com proporções
freq_genero_freq_esc.plot(kind='bar', stacked=True, figsize=(12, 10), color=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854'])

# Personalizar o gráfico
plt.title('Proporção de Frequência de Escalada por Gênero')
plt.xlabel('Gênero')
plt.ylabel('Proporção de Escaladores (%)')
plt.legend(title='Frequência de Escalada')
plt.xticks(rotation=0)
plt.tight_layout()

# Mostrar o gráfico
plt.show()

#____________________________________________

# 7 Proporção de Escala com Dor por Gênero

# Definir a ordem crescente para 'escala_com_dor'
ordem_escala_com_dor = [
    'Não escalo com dor', 
    '10% do tempo escalo com alguma dor', 
    '25% do tempo escalo com alguma dor', 
    '50% do tempo escalo com alguma dor', 
    '75% do tempo escalo com alguma dor', 
    '90% ou mais do tempo escalo com alguma dor'
]

deb2['escala_com_dor'] = pd.Categorical(deb2['escala_com_dor'], categories=ordem_escala_com_dor, ordered=True)

# Calcular a tabela de contingência normalizada para proporções
freq_genero_escala_com_dor = pd.crosstab(deb2['genero'], deb2['escala_com_dor'], normalize='index') * 100

# Plotar o gráfico de barras empilhadas com proporções (barras mais finas)
ax = freq_genero_escala_com_dor.plot(kind='bar', stacked=True, figsize=(10, 6), width=0.6, color=['#66c2a5', '#fc8d62', '#8da0cb', '#e78ac3', '#a6d854', '#ff7f00'])

# Personalizar o gráfico
plt.title('Proporção de Escala com Dor por Gênero')
plt.xlabel('Gênero')
plt.ylabel('Proporção de Escaladores (%)')
plt.xticks(rotation=0)

# Adicionar a legenda no meio das barras
plt.legend(title='Escala com Dor', loc='center left', bbox_to_anchor=(0.85, 0.5), title_fontsize=10, fontsize=9)

# Ajustar layout para que as legendas não sobreponham
plt.tight_layout()

# Mostrar o gráfico
plt.show()

#_________________________________________________

# 8 Proporção de genero vs ja se lesionou

# Calculando a proporção para cada gênero
proportional_data = deb2.groupby(['genero', 'ja_lesionou']).size().unstack()
proportional_data = proportional_data.div(proportional_data.sum(axis=1), axis=0)

# Criando o gráfico de barras com proporções
proportional_data.plot(kind='bar', figsize=(8, 6), stacked=False, color=['salmon', 'skyblue'])

# Adicionando título e legendas
plt.title('Proporção de Lesões por Gênero', fontsize=16)
plt.xlabel('Gênero', fontsize=12)
plt.ylabel('Proporção', fontsize=12)
plt.xticks(rotation=0)
plt.legend(title='Já lesionou', loc='upper right')
plt.tight_layout()

# Exibindo o gráfico
plt.show()



# 8 Correlação entre Gênero e Diagnóstico Médico entre os escaladores Lesionados

# Exemplo de dados
data = {
    'genero': ['Feminino', 'Masculino', 'Masculino', 'Feminino', 'Feminino', 'Masculino', 'Feminino'],
    'diagnostico_medico': ['Sim', 'Não', 'Sim', 'Sim', 'Não', 'Não', 'Sim']
}
deb2 = pd.DataFrame(data)

# Criar tabela de frequência cruzada entre gênero e diagnóstico
cross_tab = pd.crosstab(deb2['genero'], deb2['diagnostico_medico'], normalize='index') * 100

# Criar gráfico de barras empilhadas
fig, ax = plt.subplots(figsize=(8, 5))

bars = cross_tab.plot(kind='bar', stacked=True, ax=ax, color=['salmon', 'skyblue'], edgecolor='black')

# Adicionar porcentagens dentro das barras
for bar_group in bars.containers:
    for bar in bar_group:
        height = bar.get_height()
        if height > 0:  # Mostrar apenas se houver valor
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_y() + height / 2,
                f'{height:.1f}%',
                ha='center',
                va='center',
                color='black',
                fontsize=10
            )

# Configurar o gráfico
ax.set_title("Correlação entre Gênero e Diagnóstico Médico entre os escaladores Lesionados", fontsize=14)
ax.set_xlabel("")
ax.set_ylabel("Porcentagem")
ax.legend(title="Diagnóstico Médico", loc='center')
ax.spines['top'].set_visible(False)  # Remover linha superior
ax.spines['right'].set_visible(False)  # Remover linha lateral direita
ax.spines['left'].set_visible(False)  # Remover linha lateral esquerda
ax.get_yaxis().set_visible(False)  # Esconder escala vertical

# Ajustar rótulos do eixo X para horizontal
ax.set_xticklabels(cross_tab.index, rotation=0)

# Mostrar o gráfico
plt.show()






## 8 simples - Distribuição de Diagnósticos Médicos em Escaladores lesionados

# Contar valores únicos na coluna
diagnostico_counts = deb2['diagnostico_medico'].value_counts()
total = diagnostico_counts.sum()

# Criar o gráfico de barras
fig, ax = plt.subplots()
bars = ax.bar(diagnostico_counts.index, diagnostico_counts.values, color=['steelblue', 'tomato'])

# Adicionar porcentagens dentro das barras
for bar in bars:
    height = bar.get_height()
    percentage = f'{(height / total) * 100:.1f}%'
    ax.text(bar.get_x() + bar.get_width() / 2, height - (height * 0.1), percentage,
            ha='center', va='bottom', color='black', fontsize=10)

# Configurar o gráfico
ax.set_title("Distribuição de Diagnósticos Médicos em Escaladores lesionados", fontsize=14)
ax.set_xlabel("")
ax.set_ylabel("Frequência")
ax.spines['top'].set_visible(False)  # Remover linha superior
ax.spines['right'].set_visible(False)  # Remover linha lateral direita
ax.spines['left'].set_visible(False)  # Remover linha lateral esquerda
ax.get_yaxis().set_visible(False)  # Esconder escala vertical

# Mostrar o gráfico
plt.show()






















































































































































