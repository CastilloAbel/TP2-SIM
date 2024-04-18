import random
import numpy as np
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import tkinter.filedialog

def generar_numeros_aleatorios(n):
    numeros_aleatorios = []
    for _ in range(n):
        numero= np.around(random.random(),decimals=4)
        numeros_aleatorios.append(numero)
    
    print("rnd", numeros_aleatorios)
    return numeros_aleatorios

def generar_distribucion(): # Esta función se encarga de generar la distribución de acuerdo a los parámetros ingresados por el usuario.

    distribucion = combo_distribucion.get() #Busca el dato seleccionado en el combo (Uniforme, exponenecial, normal)
    tamaño_muestra = int(entry_tamaño_muestra.get()) #Busca el dato tamaño de muestra solicitado y devuelve un entero
    intervalos = int(entry_intervalos.get()) #Busca el dato cantidad de intervalos solicitado yb devuelve un entero

    if distribucion == "Uniforme": 
        rnd= generar_numeros_aleatorios(tamaño_muestra)
        a = float(entry_a.get()) # Obtiene el valor ingresado por el usuario en un widget de entrada y lo combierte a float
        b = float(entry_b.get())

        datos = []

        for i in rnd:
            x = np.around(a + i* (b - a),4)
            datos.append(x)
        print("uniforme", datos)

        #datos = np.around(np.random.uniform(a, b, tamaño_muestra),decimals=4) #redondea a 4 decimales

    elif distribucion == "Exponencial":
        rnd= generar_numeros_aleatorios(tamaño_muestra)
        datos = []

        λ = float(entry_λ.get())

        for i in rnd:
            x = (-1/λ)*math.log((1-i))
            datos.append(x)
        print("EXPONENCIAL", datos)
        
    
    elif distribucion == "Normal":
        rnd1= generar_numeros_aleatorios(tamaño_muestra)
        rnd2= generar_numeros_aleatorios(tamaño_muestra)

        datos = []

        μ = float(entry_μ.get())
        σ = float(entry_σ.get())

        for i, j in zip(rnd1, rnd2):
            N1 = math.sqrt(-2 * math.log(i))* math.cos(2 * math.pi * j) * σ +  μ
            N2 = math.sqrt(-2 * math.log(i))* math.sin(2 * math.pi * j) * σ + μ
            datos.append([N1,N2])
        print("NORMAL", datos)
        
    
        #datos = np.around(np.random.normal(μ, σ, tamaño_muestra), decimals=4)
    
    histograma_frecuencias(datos, intervalos)

def histograma_frecuencias(datos, intervalos): # Define una función llamada histograma_frecuencias que calcula el histograma de frecuencias de los datos generados y muestra tanto el histograma como la tabla de frecuencias en una nueva ventana.
    mostrar_datos(datos)
    frecuencia, intervalo = np.histogram(datos, bins=intervalos)
    
    # Crear una nueva ventana para mostrar el histograma y la tabla de frecuencias
    ventana_resultados = tk.Toplevel(ventana)
    ventana_resultados.title("Resultados")

    # Mostrar el histograma
    fig, ax = plt.subplots()
    ax.hist(datos, bins=intervalos, edgecolor='black')
    ax.set_xlabel('Intervalos')
    ax.set_ylabel('Frecuencia')
    ax.set_title('Histograma de Frecuencias')

    # Mostrar los intervalos limitantes en el eje x
    ax.set_xticks(intervalo)

    # Mostrar la tabla de frecuencias
    tabla_frecuencias = "Tabla de frecuencias:\nIntervalo\tFrecuencia\n"
    for i in range(len(frecuencia)):
        tabla_frecuencias += f"{intervalo[i]:.2f} - {intervalo[i+1]:.2f}\t{frecuencia[i]}\n"

    txt_tabla_frecuencias = tk.Text(ventana_resultados, height=20, width=40)
    txt_tabla_frecuencias.insert(tk.END, tabla_frecuencias)
    txt_tabla_frecuencias.grid(row=1, column=0)

    #Agregar un botón para guardar la tabla de frecuencias
    #btn_guardar_tabla = tk.Button(ventana_resultados, text="Guardar Tabla", command=lambda: guardar_tabla_frecuencias(tabla_frecuencias))
    #btn_guardar_tabla.grid(row=2, column=0)

    plt.show()

def mostrar_datos(datos): # Define una función llamada mostrar_datos que muestra los datos generados en una nueva ventana.
    ventana_datos = tk.Toplevel(ventana)
    ventana_datos.title("Variables aleatroia segun distribucion")

    txt_datos = tk.Text(ventana_datos, height=40, width=50)
    txt_datos.pack()

    # Insertar los datos en el widget Text
    for dato in datos:
        txt_datos.insert(tk.END, f"{dato}\n")

    # Deshabilitar la edición del widget Text
    txt_datos.config(state=tk.DISABLED)

    # Botón para guardar los datos en un archivo
    btn_guardar = tk.Button(ventana_datos, text="Guardar", command=lambda: guardar_datos(datos))
    btn_guardar.pack()

def guardar_datos(datos): #Define una función llamada guardar_datos que permite al usuario guardar las variables generadas en un archivo.
    archivo_datos = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if archivo_datos is None:
        return
    for dato in datos:
        archivo_datos.write(f"{dato}\n")
    archivo_datos.close()

def cerrar_aplicacion(): #Define una función llamada cerrar_aplicacion que cierra la aplicación.
    ventana.quit()
    ventana.destroy()

def seleccionar_dist(event):
    seleccion = combo_distribucion.get()

    if seleccion == "Uniforme":
        entry_a.config(state="normal")
        entry_b.config(state="normal")
        entry_λ.config(state="disabled")
        entry_μ.config(state="disabled")
        entry_σ.config(state="disabled")
    elif seleccion == "Exponencial":
        entry_a.config(state="disabled")
        entry_b.config(state="disabled")
        entry_λ.config(state="normal")
        entry_μ.config(state="disabled")
        entry_σ.config(state="disabled")
    elif seleccion == "Normal":
        entry_a.config(state="disabled")
        entry_b.config(state="disabled")
        entry_λ.config(state="disabled")
        entry_μ.config(state="normal")
        entry_σ.config(state="normal")

#///////////////////////////////////////////////////////////////////////////////////////////////////////////
#MUESTRA DE DATOS Y INTERACION CON EL USUARIO
    
# Crear ventana principal
ventana = tk.Tk()
ventana.title("Generador de Distribuciones")

# Crear widgets
lbl_tamaño_muestra = tk.Label(ventana, text="Tamaño de muestra:")
entry_tamaño_muestra = tk.Entry(ventana)
lbl_intervalos = tk.Label(ventana, text="Número de intervalos:")
entry_intervalos = tk.Entry(ventana)

lbl_distribucion = tk.Label(ventana, text="Distribución:")
combo_distribucion = ttk.Combobox(ventana, values=["Uniforme", "Exponencial", "Normal"])
combo_distribucion.bind("<<ComboboxSelected>>", seleccionar_dist)
lbl_a = tk.Label(ventana, text="Valor de a:")
entry_a = tk.Entry(ventana)
lbl_b = tk.Label(ventana, text="Valor de b:")
entry_b = tk.Entry(ventana)

lbl_λ = tk.Label(ventana, text="Valor de λ:")
entry_λ = tk.Entry(ventana)

lbl_μ = tk.Label(ventana, text="Valor de μ:")
entry_μ = tk.Entry(ventana)
lbl_σ = tk.Label(ventana, text="Valor de σ:")
entry_σ = tk.Entry(ventana)

btn_generar = tk.Button(ventana, text="Generar Distribución", command=generar_distribucion) #Aca manda a llamae a la funcion generar distribucion 

# Ubicar widgets en la ventana
lbl_tamaño_muestra.grid(row=0, column=0, padx=5, pady=5)
entry_tamaño_muestra.grid(row=0, column=1, padx=5, pady=5)
lbl_intervalos.grid(row=1, column=0, padx=5, pady=5)
entry_intervalos.grid(row=1, column=1, padx=5, pady=5)
lbl_distribucion.grid(row=2, column=0, padx=5, pady=5)
combo_distribucion.grid(row=2, column=1, padx=5, pady=5)

lbl_a.grid(row=3, column=0, padx=5, pady=5)
entry_a.grid(row=3, column=1, padx=5, pady=5)
lbl_b.grid(row=4, column=0, padx=5, pady=5)
entry_b.grid(row=4, column=1, padx=5, pady=5)

lbl_λ.grid(row=5, column=0, padx=5, pady=5)
entry_λ.grid(row=5, column=1, padx=5, pady=5)

lbl_μ.grid(row=6, column=0, padx=5, pady=5)
entry_μ.grid(row=6, column=1, padx=5, pady=5)
lbl_σ.grid(row=7, column=0, padx=5, pady=5)
entry_σ.grid(row=7, column=1, padx=5, pady=5)

#botones
btn_generar.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
btn_cerrar = tk.Button(ventana, text="Cerrar", command=cerrar_aplicacion)
btn_cerrar.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Iniciar la ventana
ventana.mainloop() #Inicia el bucle principal de eventos de la interfaz gráfica. Esto mantiene la ventana abierta y escuchando eventos hasta que el usuario la cierre.
