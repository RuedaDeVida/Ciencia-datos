import pandas as pd
from sklearn import datasets
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Cargar el conjunto de datos Iris

iris = datasets.load_iris()

# Convertirlo en un DataFrame de Pandas

df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['species'] = pd.Categorical.from_codes(iris.target, iris.target_names)

# Mostrar las primeras filas del conjunto de datos

print(df.head())

# Dividir los datos en características (X) y etiquetas (y)

X = df.drop('species', axis=1)
y = df['species']

# Dividir los datos en un conjunto de entrenamiento (80%) y un conjunto de prueba (20%)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Tamaño del conjunto de entrenamiento:", X_train.shape)
print("Tamaño del conjunto de prueba:", X_test.shape)


logreg = LogisticRegression(max_iter=200)

logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)

print("Predicciones:", y_pred[:5])


accuracy = accuracy_score(y_test, y_pred)
print(f"Precisión del modelo: {accuracy:.4f}")


conf_matrix = confusion_matrix(y_test, y_pred)
print("\nMatriz de Confusión:")
print(conf_matrix)


class_report = classification_report(y_test, y_pred)
print("\nInforme de Clasificación:")
print(class_report)



label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y_test)


colors = ['red', 'green', 'blue']
species_labels = label_encoder.classes_


plt.figure(figsize=(8, 6))


plt.scatter(X_test.iloc[:, 0], X_test.iloc[:, 1], c=y_encoded, cmap='viridis', marker='x', label='Predicción')
plt.scatter(X_test.iloc[:, 0], X_test.iloc[:, 1], c=y_test.map({'setosa': 0, 'versicolor': 1, 'virginica': 2}),
            cmap='coolwarm', marker='o', label='Real')

plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])
plt.title("Predicciones vs Clases Reales")
plt.legend()
plt.show()

# Visualizar las predicciones vs las clases reales
""" plt.figure(figsize=(8, 6))
plt.scatter(X_test.iloc[:, 0], X_test.iloc[:, 1], c=y_pred, cmap='viridis', marker='x', label='Predicción')
plt.scatter(X_test.iloc[:, 0], X_test.iloc[:, 1], c=y_test, cmap='coolwarm', marker='o', label='Real')
plt.xlabel(iris.feature_names[0])
plt.ylabel(iris.feature_names[1])
plt.title("Predicciones vs Clases Reales")
plt.legend()
plt.show() """

# Cargar el conjunto de datos Iris
iris = datasets.load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['species'] = iris.target
df['species'] = df['species'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})


plt.figure(figsize=(10, 6))
sns.scatterplot(x='sepal length (cm)', y='sepal width (cm)', hue='species', data=df, palette="Set1", s=100)
plt.title('Sepal Length vs Sepal Width')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Sepal Width (cm)')
plt.legend(title='Species')
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))
sns.histplot(df['sepal length (cm)'], kde=True, bins=20, color='purple')
plt.title('Distribución de Longitud del Sépalo')
plt.xlabel('Sepal Length (cm)')
plt.ylabel('Frecuencia')
plt.grid(True)
plt.show()


correlation_matrix = df.iloc[:, :-1].corr() 
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=1, cbar_kws={'shrink': 0.8})
plt.title('Matriz de Correlación de las Características')
plt.show()


plt.figure(figsize=(10, 6))
sns.boxplot(x='species', y='sepal length (cm)', data=df, palette='Set2')
plt.title('Distribución de Longitud del Sépalo por Especie')
plt.xlabel('Especie')
plt.ylabel('Sepal Length (cm)')
plt.grid(True)
plt.show()