# -*- coding: utf-8 -*-
"""LSS_Atividade_2403

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PyzeTRd96jWTYklDNmiYcaqRXF3gMGKU
"""

# Importar bibliotecas
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import shapiro



# Definir constantes
ALPHA = 0.05

# Carregar os dados
df = pd.read_excel('encoded_cleaned_test_gitup.xlsx')

# Verificar se há valores NaN no dataframe e remover linhas com NaN
print("Valores NaN no dataframe:")
print(df.isna().sum())
df = df.dropna()

# Calcular o IQR para cada coluna e filtrar outliers
Q1 = df.quantile(0.25)
Q3 = df.quantile(0.75)
IQR = Q3 - Q1
df_no_outliers = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR))).any(axis=1)]

# Medir: Calcular estatísticas descritivas para o tempo de entrega
time_taken_mean_no_outliers = df_no_outliers["Time_taken(min)"].mean()
time_taken_median_no_outliers = df_no_outliers["Time_taken(min)"].median()
time_taken_std_no_outliers = df_no_outliers["Time_taken(min)"].std()
print("*"*50)
print(f"Média do tempo de entrega: {time_taken_mean_no_outliers:.2f}")
print(f"Mediana do tempo de entrega: {time_taken_median_no_outliers:.2f}")
print(f"Desvio padrão do tempo de entrega: {time_taken_std_no_outliers:.2f}")
print("*"*50)

# Analisar: Visualizar a distribuição do tempo de entrega e verificar se há outliers
sns.boxplot(x=df_no_outliers["Time_taken(min)"])
plt.show()

# Calcular as correlações no dataframe sem outliers
correlations_no_outliers = df_no_outliers.corr()["Time_taken(min)"].sort_values(ascending=False)
print("Correlações entre 'Time_taken(min)' e outras colunas numéricas (sem outliers):")
print(correlations_no_outliers)

print("""
Positivamente correlacionadas: As variáveis 'multiple_deliveries' (0,317), 'Delivery_person_Age' (0,287), 'Delivery_location_latitude' (0,072) e 'Restaurant_latitude' (0,071) têm correlação positiva com o tempo de entrega.\n Isso significa que, à medida que o valor dessas variáveis aumenta, o tempo de entrega também tende a aumentar.

Negativamente correlacionadas: As variáveis 'Delivery_person_Ratings' (-0,337), 'Vehicle_condition' (-0,249), 'City' (-0,219), 'Road_traffic_density' (-0,192), 'Weatherconditions' (-0,155), 'Type_of_vehicle' (-0,082), 'Delivery_location_longitude' (-0,008) e 'Restaurant_longitude' (-0,012) têm correlação negativa com o tempo de entrega. \n Isso significa que, à medida que o valor dessas variáveis aumenta, o tempo de entrega tende a diminuir.

Baixa correlação: A variável 'Type_of_order' (0,017) tem uma correlação próxima a zero, o que indica que não há uma relação linear clara entre essa variável e o tempo de entrega.")

""")


#Converter a coluna 'Festival' em uma coluna numérica (por exemplo, 0 para 'Não' e 1 para 'Sim')
df_no_outliers['Festival'] = df_no_outliers['Festival'].map({'Não': 0, 'Sim': 1})


#Selecionar as colunas numéricas para a análise de regressão
X = df_no_outliers[[
'Delivery_location_latitude',
'Restaurant_latitude',
'Delivery_location_longitude',
'Restaurant_longitude',
'Delivery_person_Ratings',
'Type_of_order',
'Vehicle_condition',
'Weatherconditions',
'Delivery_person_Age',
'multiple_deliveries',
'Road_traffic_density'
]]
y = df_no_outliers['Time_taken(min)']

#Adicionar uma constante ao conjunto de recursos (necessário para a regressão linear múltipla)
X = sm.add_constant(X)

#Ajustar o modelo de regressão linear múltipla
model = sm.OLS(y, X).fit()

print(model.summary())

print("\n")
print("*"*50)
print("Análise da Regressão nos Outliers:")
print("""
R-squared e Adj. R-squared: O valor de R-squared é 0,410, o que indica que aproximadamente 41% da variabilidade na variável dependente (Time_taken(min)) pode ser explicada pelas variáveis independentes no modelo. \n O valor ajustado de R-squared, que leva em consideração o número de variáveis e o tamanho da amostra, também é próximo de 0,410, indicando um ajuste razoável do modelo.

P>|t|: Essa coluna indica a significância das variáveis independentes no modelo. Valores menores que 0,05 sugerem que a variável é estatisticamente significativa. \nNesse caso, Delivery_person_Ratings, Vehicle_condition, Weatherconditions, Delivery_person_Age, multiple_deliveries e Road_traffic_density são estatisticamente significativos, pois seus valores P são menores que 0,05.

Coeficientes: Os coeficientes mostram a relação entre a variável dependente e cada variável independente, mantendo outras constantes. \n Por exemplo, um aumento de uma unidade no Delivery_person_Ratings está associado a uma diminuição de 8,8666 unidades no tempo de entrega (Time_taken(min)), mantendo constantes todas as outras variáveis.
""")

#Realizar o teste de Shapiro-Wilk na coluna 'Time_taken(min)'
shapiro_test = shapiro(df_no_outliers['Time_taken(min)'])

print("\n")
print("="*50)
print("Teste de Normalidade:")
print("Estatística de Shapiro-Wilk:", shapiro_test[0])
print("Valor-p de Shapiro-Wilk:", shapiro_test[1])
print("\n")
print("="*50)

#Analisar o resultado do teste de normalidade
print("Como o valor-p é menor que 0,05 (ou 5%), rejeitamos a hipótese nula. Isso significa que há evidências suficientes para afirmar que a coluna 'Time_taken(min)' não tem uma distribuição normal.")