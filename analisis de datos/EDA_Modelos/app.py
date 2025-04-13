import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar el conjunto de datos Iris desde seaborn
#(aquí deberá cargar su conjunto de datos)
data = sns.load_dataset('iris')
# Ver las primeras filas del conjunto de datos
print(data.head())

# Descripción general del conjunto de datos
print(data.describe())

# Generar boxplots para cada una de las características del conjunto de datos
plt.figure(figsize=(12, 8))
# Boxplot de todas las columnas numéricas
sns.boxplot(data=data[['sepal_length', 'sepal_width',
'petal_length', 'petal_width']])
plt.title("Boxplot de las características del Iris")
plt.show()

# Histograma de las características numéricas
data[['sepal_length', 'sepal_width', 'petal_length',
'petal_width']].hist(bins=15, figsize=(12, 8))
plt.suptitle("Histogramas de las características del Iris")
plt.show()

# Pairplot para ver la relación entre las características numéricas
sns.pairplot(data, hue='species')
plt.suptitle("Pairplot de las características del Iris", y=1.02)
plt.show()

# Calcular la matriz de correlación
correlation_matrix = data.corr()
# Mostrar la matriz de correlación con un mapa de calor
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title("Mapa de calor de la correlación entre características")
plt.show()

# Gráfico de caja para comparar la longitud del sépalo entre las especies
plt.figure(figsize=(8, 6))
sns.boxplot(x='species', y='sepal_length', data=data)
plt.title("Comparación de la longitud del sépalo por especie")
plt.show()