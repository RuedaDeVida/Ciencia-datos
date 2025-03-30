from flask import Flask, request, render_template, redirect, url_for
import pymysql
#import mysql.connector
import csv
import json
import os

app = Flask(__name__)

# Configuración de la conexión a MySQL
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",  # Cambia según tu configuración
        password="",  # Cambia según tu configuración
        database="encuesta"
    )

# Página de inicio
@app.route("/")
def index():
    return render_template("index.html")

# Página de nosotros
@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

# Página de contacto con formulario


""" @app.route("/contacto", methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        mensaje = request.form['mensaje']

        # Conectar a la BD y guardar el mensaje
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO mensaje (nombre, email, mensaje) VALUES (%s, %s, %s)", (nombre, email, mensaje))
        #sql1 = """"""INSERT INTO mensaje (nombre, email, mensaje) VALUES (%s, %s, %s)""""""
        #valors =  (nombre, email, mensaje)              
        #cursor.execute(sql1, valors)
        #cursor.execute()
        
        db.commit()
        cursor.close()
        db.close()

        return redirect(url_for('mensajes'))  # Redirigir a la página de mensajes

    return render_template("contacto.html") """

#inicio prueba
@app.route("/contacto")
def contacto():
    return render_template("contacto.html")

@app.route("/contacto", methods=['POST'])
def contact():
    #request.method == 'POST':
    nombre = request.form['nombre']
    email = request.form['email']
    mensaje = request.form['mensaje']

        # Conectar a la BD y guardar el mensaje
    db = get_db_connection()
    cursor = db.cursor()
    #cursor.execute("INSERT INTO mensaje (nombre, email, mensaje) VALUES (%s, %s, %s)", (nombre, email, mensaje))
    sql1 = """INSERT INTO mensaje (nombre, email, mensaje) VALUES (%s, %s, %s)"""
    valors =  (nombre, email, mensaje)              
    cursor.execute(sql1, valors)
        #cursor.execute()
        
    db.commit()
    cursor.close()
    db.close()

    return redirect(url_for('mensajes'))  # Redirigir a la página de mensajes

    #return render_template("contacto.html")

#fin prueba

# Página para ver mensajes almacenados
@app.route('/mensajes')
def mensajes():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM mensaje")
    #cursor.execute("SELECT nombre, email, mensaje FROM mensaje ORDER BY id DESC")
    #cursor.execute("SELECT nombre, email, mensaje FROM mensaje ORDER BY nombre DESC")
    mensajes = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template('mensajes.html', mensajes=mensajes)

# Página del formulario de la persona
@app.route("/persona")
def persona():
    return render_template("persona.html")

# Procesar el formulario de encuesta
@app.route("/procesar", methods=["POST"])
def procesar():
    nombre = request.form["nombre"]
    edad = request.form["edad"]
    salud = request.form["salud"]
    desarrollo = request.form["desarrollo"]
    amistad = request.form["amistad"]
    hogar = request.form["hogar"]
    amor = request.form["amor"]
    ocio = request.form["ocio"]
    trabajo = request.form["trabajo"]
    dinero = request.form["dinero"]

#nuevo
# Guardar en archivo JSON
    data = {
        "nombre": nombre,
        "edad": edad,
        "salud": salud,
        "desarrollo": desarrollo,
        "amistad": amistad,
        "hogar": hogar,
        "amor": amor,
        "ocio": ocio,
        "trabajo": trabajo,
        "dinero": dinero
    }

    # Guardar en un archivo JSON
    if os.path.exists('resultados.json'):
        with open('resultados.json', 'r') as file:
            resultados = json.load(file)
    else:
        resultados = []

    resultados.append(data)
    with open('resultados.json', 'w') as file:
        json.dump(resultados, file, indent=4)

    # Guardar en un archivo CSV
    with open('resultados.csv', 'a', newline='') as csvfile:
        fieldnames = ['nombre', 'edad', 'salud', 'desarrollo', 'amistad', 'hogar', 'amor', 'ocio', 'trabajo', 'dinero']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(data)

#nuevo


    # Conectar a la BD
    db = get_db_connection()
    cursor = db.cursor()

    sql = """
    INSERT INTO respuestas (nombre, edad, salud, desarrollo, amistad, hogar, amor, ocio, trabajo, dinero) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (nombre, edad, salud, desarrollo, amistad, hogar, amor, ocio, trabajo, dinero)

    cursor.execute(sql, valores)
    db.commit()

    # Cerrar conexión
    cursor.close()
    db.close()

    return redirect(url_for("resultados"))

# Ver resultados de la encuesta
@app.route("/encuesta")
def resultados():
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM respuestas")
    datos = cursor.fetchall()
    cursor.close()
    db.close()

    return render_template("encuesta.html", datos=datos)

if __name__ == "__main__":
    app.run(debug=True)

