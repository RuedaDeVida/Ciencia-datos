import matplotlib.pyplot as plt
import pandas as pd

data = {
'Empleado': ['Ana', 'Luis', 'Carlos'],
'Satisfacción': [7, 8, 5],
'Áreas de mejora': ['Comunicación', 'Gestión del tiempo',
'Liderazgo']
}

df = pd.DataFrame(data)
print(df)

empleados = df['Empleado']
satisfaccion = df['Satisfacción']
plt.bar(empleados, satisfaccion, color='blue')
plt.title('Nivel de Satisfacción de los Empleados')
plt.xlabel('Empleado')
plt.ylabel('Satisfacción')
plt.show()

plt.plot(empleados, satisfaccion, marker='o', color='green')
plt.title('Satisfacción de los Empleados a lo largo del tiempo')
plt.xlabel('Empleado')
plt.ylabel('Satisfacción')
plt.show()