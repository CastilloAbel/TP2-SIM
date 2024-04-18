import random
import numpy as np
import math
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import tkinter.filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

datos_pdf = []

def generar_numeros_aleatorios(n):
    numeros_aleatorios = []
    for _ in range(n):
        numero = np.around(random.random(), decimals=4)
        numeros_aleatorios.append(numero)

    print("rnd", numeros_aleatorios)
    return numeros_aleatorios

def generar_distribucion():
    distribucion = combo_distribucion.get()
    tamaño_muestra = int(entry_tamaño_muestra.get())
    intervalos = int(entry_intervalos.get())
    global datos_pdf
    if distribucion == "Uniforme":
        rnd = generar_numeros_aleatorios(tamaño_muestra)
        a = float(entry_a.get())
        b = float(entry_b.get())

        datos = []

        for i in rnd:
            x = np.around(a + i * (b - a), 4)
            datos.append(x)
        print("uniforme", datos)

    elif distribucion == "Exponencial":
        rnd = generar_numeros_aleatorios(tamaño_muestra)
        datos = []

        λ = float(entry_λ.get())

        for i in rnd:
            x = (-1 / λ) * math.log((1 - i))
            datos.append(x)
        print("EXPONENCIAL", datos)

    elif distribucion == "Normal":
        rnd1 = generar_numeros_aleatorios(tamaño_muestra)
        rnd2 = generar_numeros_aleatorios(tamaño_muestra)

        datos = []

        μ = float(entry_μ.get())
        σ = float(entry_σ.get())

        for i, j in zip(rnd1, rnd2):
            N1 = math.sqrt(-2 * math.log(i)) * math.cos(2 * math.pi * j) * σ + μ
            N2 = math.sqrt(-2 * math.log(i)) * math.sin(2 * math.pi * j) * σ + μ
            datos.append(N1)
            datos.append(N2)
        print("NORMAL", datos)
        datos_pdf = datos
    histograma_frecuencias(datos, intervalos)


def histograma_frecuencias(datos, intervalos):
    mostrar_datos(datos)
    frecuencia, intervalo = np.histogram(datos, bins=intervalos)

    ventana_resultados = tk.Toplevel(ventana)
    ventana_resultados.title("Resultados")

    fig, ax = plt.subplots()
    ax.hist(datos, bins=intervalos, edgecolor='black')
    ax.set_xlabel('Intervalos')
    ax.set_ylabel('Frecuencia')
    ax.set_title('Histograma de Frecuencias')

    ax.set_xticks(intervalo)

    tabla_frecuencias = "Tabla de frecuencias:\nIntervalo\tFrecuencia\n"
    for i in range(len(frecuencia)):
        tabla_frecuencias += f"{intervalo[i]:.2f} - {intervalo[i + 1]:.2f}\t{frecuencia[i]}\n"

    txt_tabla_frecuencias = tk.Text(ventana_resultados, height=20, width=40)
    txt_tabla_frecuencias.insert(tk.END, tabla_frecuencias)
    txt_tabla_frecuencias.grid(row=1, column=0)

    plt.show()

def mostrar_datos(datos):
    ventana_datos = tk.Toplevel(ventana)
    ventana_datos.title("Variables aleatorias según distribución")

    txt_datos = tk.Text(ventana_datos, height=40, width=50)
    txt_datos.pack()

    for dato in datos:
        txt_datos.insert(tk.END, f"{dato}\n")

    txt_datos.config(state=tk.DISABLED)

    btn_guardar = tk.Button(ventana_datos, text="Guardar", command=lambda: guardar_datos(datos))
    btn_guardar.pack()

def guardar_datos(datos):
    archivo_datos = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if archivo_datos is None:
        return
    for dato in datos:
        archivo_datos.write(f"{dato}\n")
    archivo_datos.close()

def guardar_datos_pdf(datos):
    archivo_pdf = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".pdf")
    if archivo_pdf is None:
        return

    c = canvas.Canvas(archivo_pdf.name, pagesize=letter)
    c.drawString(100, 750, "Valores Generados:")
    y = 730
    for dato in datos:
        c.drawString(100, y, str(dato))
        y -= 15

    c.save()
    archivo_pdf.close()
    messagebox.showinfo("Guardado", "Los datos se han guardado en formato PDF correctamente.")

def actualizar_campos(*args):
    distribucion = combo_distribucion.get()

    entry_a.config(state="disabled")
    entry_b.config(state="disabled")
    entry_λ.config(state="disabled")
    entry_μ.config(state="disabled")
    entry_σ.config(state="disabled")

    if distribucion == "Uniforme":
        entry_a.config(state="normal")
        entry_b.config(state="normal")
    elif distribucion == "Exponencial":
        entry_λ.config(state="normal")
    elif distribucion == "Normal":
        entry_μ.config(state="normal")
        entry_σ.config(state="normal")

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

lbl_a = tk.Label(ventana, text="Valor de a:")
entry_a = tk.Entry(ventana, state="disabled")
lbl_b = tk.Label(ventana, text="Valor de b:")
entry_b = tk.Entry(ventana, state="disabled")

lbl_λ = tk.Label(ventana, text="Valor de λ:")
entry_λ = tk.Entry(ventana, state="disabled")

lbl_μ = tk.Label(ventana, text="Valor de μ:")
entry_μ = tk.Entry(ventana, state="disabled")
lbl_σ = tk.Label(ventana, text="Valor de σ:")
entry_σ = tk.Entry(ventana, state="disabled")

btn_generar = tk.Button(ventana, text="Generar Distribución", command=generar_distribucion)

# Asignar función para actualizar campos según selección
combo_distribucion.bind("<<ComboboxSelected>>", actualizar_campos)

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

# Botones
btn_generar.grid(row=8, column=0, columnspan=2, padx=5, pady=5)
btn_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
btn_cerrar.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

# Botón para guardar en PDF
btn_guardar_pdf = tk.Button(ventana, text="Guardar en PDF", command=lambda: guardar_datos_pdf(datos_pdf))
btn_guardar_pdf.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# Iniciar la ventana
ventana.mainloop()
