import pandas as pd
data = {
'Empleado': ['Ana', 'Luis', 'Carlos'],
'Satisfacción': [7, 8, 5],
'Áreas de mejora': ['Comunicación', 'Gestión del tiempo',
'Liderazgo']
}
df = pd.DataFrame(data)
print(df)

df_filtrado = df[df['Satisfacción'] > 6]
print(df_filtrado)

mean_satisfaction = df['Satisfacción'].mean()
print(f"Promedio de satisfacción: {mean_satisfaction}")