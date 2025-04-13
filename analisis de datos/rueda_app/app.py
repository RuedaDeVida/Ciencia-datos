from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
# fin
from flask import Flask, render_template, request, redirect, send_file, render_template_string

import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

CAMPOS_PERSONALES = ['nombre', 'apellido', 'edad']

CATEGORIAS = [
    'salud', 'dinero', 'carrera', 'familia',
    'amor', 'amigos', 'diversion', 'crecimiento'
]

PREGUNTAS = {
    'salud': '¿Cómo te sientes físicamente?',
    'dinero': '¿Estás satisfecho con tu situación financiera?',
    'carrera': '¿Te sientes realizado profesionalmente?',
    'familia': '¿Tienes una buena relación con tu familia?',
    'amor': '¿Cómo está tu vida amorosa?',
    'amigos': '¿Tienes amigos en quienes confiar?',
    'diversion': '¿Disfrutas tiempo para ti y tus hobbies?',
    'crecimiento': '¿Estás aprendiendo y creciendo personalmente?'
}

@app.route('/')
def index():
    return render_template('formulario.html', categorias=CATEGORIAS, preguntas=PREGUNTAS)

@app.route('/guardar', methods=['POST'])
def guardar():
    datos = {campo: request.form[campo] for campo in CAMPOS_PERSONALES}
    datos.update({categoria: request.form[categoria] for categoria in CATEGORIAS})

    columnas = CAMPOS_PERSONALES + CATEGORIAS

    with open('datos_rueda.csv', mode='a', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=columnas)
        
        archivo.seek(0, 2)
        if archivo.tell() == 0:
            writer.writeheader()

        writer.writerow(datos)

    return redirect('/')


@app.route('/grafico')
def mostrar_grafico():
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')
    if df.empty:
        return 'No hay datos aún.'

    datos = df[CATEGORIAS].iloc[-1]
    categorias = list(datos.index)
    valores = datos.values.astype(float).tolist()
    valores += valores[:1]
    angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angulos, valores, color='blue', linewidth=2)
    ax.fill(angulos, valores, color='skyblue', alpha=0.4)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias)
    ax.set_yticks(range(1, 11))
    ax.set_title("Rueda de la Vida (último registro)", size=16, y=1.1)

    ruta_imagen = 'static/grafico.png'
    os.makedirs('static', exist_ok=True)
    plt.savefig(ruta_imagen)
    plt.close()

    return send_file(ruta_imagen, mimetype='image/png')


@app.route('/registros')
def ver_registros():
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')
    if df.empty:
        return 'No hay datos aún.'

    promedios = df[CATEGORIAS].mean().round(2).to_dict()
    registros = df.to_dict(orient='records')

    return render_template_string('''
    <html>
    <head>
    <title>Registros guardados</title>
    <style>
        /* Estilos generales */
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
            color: #333;
        }
        header {
            background-color: #4CAF50;
            color: white;
            padding: 10px 0;
            text-align: center;
        }

        header h1 {
            color: white;
            
            /*margin-top: 10px;*/
        }

        nav {
            margin-top: 10px;
        }

        nav a {
            color: white;
            margin: 0 15px;
            text-decoration: none;
            display: inline-block;
        }

        header nav a {
            color: white;
            text-decoration: none;
            margin: 0 15px;
            /*font-size: 16px;*/
        }

        header nav a:hover {
            text-decoration: underline;
        }
        
        h2 {
            
            color: #050b05;
            margin-bottom: 15px;
        }

        a {
            text-decoration: none;
            color: #4CAF50;
            transition: color 0.3s ease;
        }

        a:hover {
            color: #3e8e41;
        }
        
        section {
            display: flex;
            align-items: center; /* Alinea los elementos verticalmente */
            justify-content: center;
            margin-top: 20px;
        }
        .ppal h2{
            text-align: center;
            max-width: 800px; 
            margin: 20px auto;
        }
        .ppal p{
            text-align: center;
            max-width: 600px; 
            margin: 20px auto;
            line-height: 1.2;
        }

        .img-container {
            text-align: center;
            float:left;
            margin-right: 40px;
            margin-top: 40px;
        }

        .ppal {
            text-align: center;
            float:left;
            margin-left: 40px;
            margin-top: 40px;
        }
        .baja h2{
            color: #050b05;
        }
        /* Contenedor principal */
        .container {
            max-width: 1000px;
            margin: 30px auto;
            padding: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        /* Estilos para las listas */
        ul {
            list-style-type: none;
            padding-left: 0;
        }

        li {
            margin-bottom: 8px;
        }

        b {
            color: #4CAF50;
        }

        /* Estilo de la tabla */
        table {
            width: 60%;
            margin: 30px auto;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-collapse: collapse;
            margin-top: 20px;
        }

        th, td {
            padding: 10px;
            text-align: left;
            border: 1px solid #ddd;
        }

        th {
            background-color: #4CAF50;
            color: white;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        tr:hover {
            background-color: #f1f1f1;
        }

        /* Estilo de los botones */
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 16px;
            margin: 10px 5px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #45a049;
        }

        /* Estilo de los enlaces para las acciones de cada registro */
        td a {
            text-decoration: none;
            color: #4CAF50;
            padding: 5px 10px;
            border: 1px solid #4CAF50;
            border-radius: 5px;
            transition: background-color 0.3s ease;
        }

        td a:hover {
            background-color: #4CAF50;
            color: white;
        }

        /* Estilos para el enlace de regresar */
        .back-link {
            display: inline-block;
            margin-top: 20px;
            font-size: 16px;
            color: #4CAF50;
            text-decoration: none;
        }

        .back-link:hover {
            color: #3e8e41;
        }
        .nota1 a{
            text-align: center;
        }
        .nota h2 {
            color: #050b05;
        }
        .nota {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: row;
            margin-top: 20px;
        }
        button.nota {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button.nota:hover {
            background-color: #45a049;
        }
        .nota button{
              /* Ajusta el ancho del texto */
            padding: 10px;
            text-align: justify;
            }
        h2 {
            text-align: center;
            color: #333;
            margin-top: 30px;
        }
        footer {
            background-color: #333;
            color: white;
            text-align: center;
            padding: 10px;
            
            width: 100%;
            bottom: 0;
        }
    </style>
    </head>
    <body>
        <header>
        <h1>Respuestas de la Encuesta</h1>
        <nav>
            <a href="/">Inicio</a>
            <a href="nosotros">Nosotros</a>
            <a href="contacto">Contacto</a>
            <a href="persona">Evaluacion</a>
        </nav>
    </header>
    <section>
            <div class="ppal">
                <h2>Introducción</h2>
                <p>Bienvenido a nuestra página de evaluación de la rueda de la vida de AgroCreditoFacil. Aquí podrás completar una evaluación que te ayudará a entender mejor tu equilibrio entre diferentes áreas de tu vida. <br><br>Es una herramienta visual de coaching personal que facilita la obtención de una visión gráfica de los aspectos que componen nuestra vida y el grado de satisfacción y equilibrio respecto a ellos. <br><br>La Rueda de Vida te ayudará a valorar tu grado de felicidad en los distintos apartados de la vida. La Rueda de la Vida es también llamada por algunos autores como círculo de la vida.</p><br>
            </div>
            <div class="img-container">
                <img src="./static/IMG/rueda_vida.jpg" alt="La cabeza y el torso de un esqueleto de dinosaurio;
                tiene una cabeza grande con dientes largos y afilados" width="600" height="341"/>
            </div>
            
    </section>
        <!--h2>Preguntas por categoría</h2>
        <ul>
        {% for categoria in categorias %}
            <li><b>{{ categoria.capitalize() }}</b>: {{ preguntas[categoria] }}</li>
        {% endfor %}
        </ul>

        <h2>Promedio por categoría</h2>
        <ul>
        {% for categoria, valor in promedios.items() %}
            <li><b>{{ categoria.capitalize() }}</b>: {{ valor }}</li>
        {% endfor %}
        </ul-->
    <section>
        <div class="ppal">
            <h2>Preguntas por categoría</h2>
            <ul>
            {% for categoria in categorias %}
                <li><b>{{ categoria.capitalize() }}</b>: {{ preguntas[categoria] }}</li>
            {% endfor %}
            </ul>
        </div>
        <div class="ppal">
            <h2>Promedio por categoría</h2>
            <ul>
            {% for categoria, valor in promedios.items() %}
                <li><b>{{ categoria.capitalize() }}</b>: {{ valor }}</li>
            {% endfor %}
            </ul>
        </div>    
    </section><br><br>
    <div class="baja">
        <h2>Registros disponibles</h2>
    </div>
<table border="1">

    <tr>
        {% for key in registros[0].keys() %}
            <th>{{ key.capitalize() }}</th>
        {% endfor %}
        <th>Ver gráfico</th>
        <th>Editar</th>
        <th>Eliminar</th>
    </tr>
    {% for fila in registros %}
    {% set idx = loop.index0 %}
    <tr>
        {% for valor in fila.values() %}
            <td>{{ valor }}</td>
        {% endfor %}
        <td><a href="/grafico/{{ idx }}">Ver</a></td>
        <td><a href="/editar/{{ idx }}">Editar</a></td>
        <td><a href="/eliminar/{{ idx }}" onclick="return confirm('¿Estás seguro de eliminar este registro?')">Eliminar</a></td>
    </tr>
    {% endfor %}
</table>
<div class="nota">
<h2>Descargar resultados</h2>
<a href="/generar_pdf">
    <button class="nota">Generar PDF</button>
</a>
<a href="/generar_excel">
    <button class="nota">Generar Excel</button>
</a>
<a href="/generar_txt">
    <button class="nota">Generar TXT</button>
</a><br>
<a href="/descargar_csv">
        <button class="nota">Descargar CSV</button>
    </a>
</div>
        <br><a href="/" id="nota1">← Volver al formulario</a>
<footer>
    <p>&copy; 2025 - Rueda de la Vida</p>
</footer>
    </body>
    </html>
    ''', registros=registros, promedios=promedios, categorias=CATEGORIAS, preguntas=PREGUNTAS)


@app.route('/grafico/<int:indice>')
def mostrar_grafico_individual(indice):
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')
    if df.empty or indice >= len(df):
        return 'Registro no encontrado.'

    datos = df.iloc[indice]

    # Obtener nombre y apellido del registro
    nombre = datos.get('nombre', 'Desconocido')
    apellido = datos.get('apellido', '')

    # Solo categorías, eliminando campos personales
    categorias = [col for col in datos.index if col not in ['nombre', 'apellido', 'edad']]
    valores = datos[categorias].values.astype(float).tolist()
    valores += valores[:1]

    angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
    angulos += angulos[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angulos, valores, color='green', linewidth=2)
    ax.fill(angulos, valores, color='lime', alpha=0.4)
    ax.set_xticks(angulos[:-1])
    ax.set_xticklabels(categorias)
    ax.set_yticks(range(1, 11))
    
    # ✅ TÍTULO personalizado con el nombre
    ax.set_title(f"Rueda de la Vida - {nombre} {apellido}", size=14, y=1.1)

    ruta_imagen = f'static/grafico_{indice}.png'
    os.makedirs('static', exist_ok=True)
    plt.savefig(ruta_imagen)
    plt.close()

    return send_file(ruta_imagen, mimetype='image/png')

@app.route('/editar/<int:indice>', methods=['GET', 'POST'])
def editar(indice):
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')

    if indice >= len(df):
        return 'Registro no encontrado.'

    if request.method == 'POST':
        for campo in df.columns:
            df.at[indice, campo] = request.form[campo]
        df.to_csv('datos_rueda.csv', index=False)
        return redirect('/registros')

    datos = df.iloc[indice].to_dict()
    return render_template_string('''
        
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Editar Registro</title>
            <style>
                /* General */
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f9;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                }

                /* Contenedor principal */
                .container {
                    margin-top: 100px;
                    background-color: white;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    width: 400px;
                    max-width: 100%;
                }

                h2 {
                    text-align: center;
                    margin-bottom: 20px;
                    color: #333;
                }

                /* Formulario */
                form {
                    display: flex;
                    flex-direction: column;
                }

                label {
                    font-weight: bold;
                    margin: 10px 0 5px;
                    color: #555;
                }

                input[type="text"],
                input[type="number"] {
                    padding: 10px;
                    margin-bottom: 15px;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    font-size: 14px;
                    outline: none;
                }

                input[type="text"]:focus,
                input[type="number"]:focus {
                    border-color: #007bff;
                    box-shadow: 0 0 5px rgba(0, 123, 255, 0.3);
                }

                /* Botones */
                button {
                    padding: 10px 15px;
                    font-size: 16px;
                    color: white;
                    background-color: #007bff;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                    margin-top: 10px;
                }

                button:hover {
                    background-color: #4CAF50;
                }

                button[type="button"] {
                    background-color: #6c757d;
                }

                button[type="button"]:hover {
                    background-color: #5a6268;
                }

                /* Enlace */
                a {
                    text-decoration: none;
                }
            </style>
        </head>
        <body>
            
            <br><br><br><br><br><br>
            <div class="container">
                <h2>Editar Registro</h2>
                <form method="POST">
                    {% for campo, valor in datos.items() %}
                        <label>{{ campo.capitalize() }}:</label>
                        <input type="{{ 'number' if campo in categorias else 'text' }}" name="{{ campo }}" value="{{ valor }}" required><br><br>
                    {% endfor %}
                    <button type="submit">Guardar cambios</button>
                    <a href="/registros"><button type="button">Cancelar</button></a>
                </form>
            </div>
        </body>
    </html>
    ''', datos=datos, categorias=CATEGORIAS)


@app.route('/eliminar/<int:indice>')
def eliminar(indice):
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')

    if indice >= len(df):
        return 'Registro no encontrado.'

    df = df.drop(index=indice).reset_index(drop=True)
    df.to_csv('datos_rueda.csv', index=False)

    return redirect('/registros')


if __name__ == '__main__':
    app.run(debug=True)


#codigo prueba

@app.route('/descargar_csv')
def descargar_csv():
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún para descargar.'

    try:
        return send_file(
            'datos_rueda.csv',
            as_attachment=True,
            mimetype='text/csv',
            download_name='registros_rueda.csv'
        )
    except Exception as e:
        return f"Ocurrió un error al descargar el CSV: {e}"
    
@app.route('/generar_pdf')
def generar_pdf():
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')
    if df.empty:
        return 'No hay datos aún.'

    # Crear un archivo PDF en memoria
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    c.setFont("Helvetica", 12)
    c.drawString(30, 750, "Resultados de la Rueda de la Vida")

    y_position = 730
    for index, row in df.iterrows():
        c.drawString(30, y_position, f"{row['nombre']} {row['apellido']} (Edad: {row['edad']})")
        y_position -= 20

        for categoria in CATEGORIAS:
            c.drawString(30, y_position, f"{categoria.capitalize()}: {row[categoria]}")
            y_position -= 15

        y_position -= 10  # Espacio entre registros

        if y_position < 50:  # Si llegamos al final de la página, generamos una nueva página
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 750

    c.showPage()
    c.save()

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="resultados_rueda.pdf", mimetype="application/pdf")

@app.route('/generar_excel')
def generar_excel():
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'

    df = pd.read_csv('datos_rueda.csv')
    if df.empty:
        return 'No hay datos aún.'

    # Guardar los datos en un archivo Excel
    excel_file = 'resultados_rueda.xlsx'
    df.to_excel(excel_file, index=False, engine='openpyxl')

    return send_file(excel_file, as_attachment=True, download_name="resultados_rueda.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Crear un archivo PDF en memoria

@app.route('/generar_txt')
def generar_txt():
    if not os.path.exists('datos_rueda.csv'):
        return 'No hay datos aún.'
    
    df = pd.read_csv('datos_rueda.csv')
    if df.empty:
        return 'No hay datos aún.'
    
    # Crear el contenido del archivo .txt
    contenido = []
    for _, row in df.iterrows():
        registro = f"Nombre: {row['nombre']} {row['apellido']} - Edad: {row['edad']}\n"
        for categoria in CATEGORIAS:
            registro += f"{categoria.capitalize()}: {row[categoria]}\n"
        contenido.append(registro + "\n")
    
    # Guardar el archivo .txt
    ruta_archivo = 'static/registros.txt'
    with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
        archivo.writelines(contenido)

    return send_file(ruta_archivo, as_attachment=True, mimetype='text/plain', attachment_filename='registros.txt')
