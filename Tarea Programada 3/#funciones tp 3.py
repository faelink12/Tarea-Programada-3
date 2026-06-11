#funciones tp 3
import tkinter as tk
import json
import random
import string

class Estacionamiento:
    def __init__(self, id, placa, marca, color, tipo, ubicacion, fechaHoraEntrada, fechaHoraSalida, monto, tipoPago):
        self.id = id
        self.info = (placa, marca, color, tipo)
        self.estadia = [ubicacion, fechaHoraEntrada, fechaHoraSalida]
        self.pago = (monto, tipoPago)
        
def crearPlaca():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=3))
    return letras + "-" + numeros

def crearDiccionarioJSON():
    with open("MOCK_DATA.json", "r", encoding="utf-8-sig") as jason:
        datos = json.load(jason)
    diccionario = {}
    for carro in datos:
        placa = crearPlaca()
        diccionario[placa] = [
            carro["Marca"],
            carro["Color"],
            carro["Tipo"],
            carro["Ubicación"],
            carro["fechaHoraEntrada"],
            carro["fechaHoraSalida"],
            carro["Monto"],
            carro["tipoPago"],
        ]
    return diccionario

def crearListaDiccionario(diccionario):
    lista = []
    contador = 1
    for placa, datos in diccionario.items():
        objeto = Estacionamiento(
            id=contador,
            placa=placa,
            marca=datos[0],
            color=datos[1],
            tipo=datos[2],
            ubicacion=datos[3],
            fechaHoraEntrada=datos[4],
            fechaHoraSalida=datos[5],
            monto=datos[6],
            tipoPago=datos[7],
        )
        lista.append(objeto)
        contador+=1
    return lista

diccionario = crearDiccionarioJSON()
listaObjetos = crearListaDiccionario(diccionario)

def denominarEspacios():
    espacios = []
    for i in range(17):
        espacios.append({"tipo": "normal", "carro": None})
    espacios.append({"tipo": "discapacidad", "carro": None})
    espacios.append({"tipo": "discapacidad", "carro": None})
    espacios.append({"tipo": "electrico", "carro": None})
    return espacios

def colorEspacio(espacio):
    if espacio["carro"] is not None:
        return "#F15959"
    elif espacio["tipo"] == "discapacidad":
        return "#597FF1"
    elif espacio["tipo"] == "electrico":
        return "#F1D559"
    else:
        return "#6FB95D"

def observarEspacio(espacio, ventanaAbierta):
    if ventanaAbierta[0] is not None:
        ventanaAbierta[0].destroy()
    app = tk.Toplevel()
    ventanaAbierta[0] = app
    app.title("Información del vehículo")
    app.geometry("400x250")
    if espacio["carro"] is not None:
        app.config(bg="#F15959")
    elif espacio["tipo"] == "discapacidad":
        app.config(bg="#597FF1")
    elif espacio["tipo"] == "electrico":
        app.config(bg="#F1D559")
    else:
        app.config(bg="#6FB95D")

def estacionamientoVentana():
    app = tk.Tk()
    app.title("Estacionamiento")
    app.geometry("600x600")
    app.resizable(False, False)
    app.config(bg="#2D2F33")
    espacios = denominarEspacios()
    botones = []
    ventanaAbierta = [None]
    tk.Label(app, text="Estacionamiento", bg="#2D2F33", fg="White", font=("SansSerif", 16, "bold")).grid(row=0, column=0, columnspan=5, pady=15, padx=15)
    for i in range(20):
        fila = (i // 5) + 1
        columna = i % 5
        boton = tk.Button(app, text="", bg=colorEspacio(espacios[i]), command=lambda n=i: observarEspacio(espacios[n], ventanaAbierta), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=fila, column=columna, padx=10, pady=10)
        botones.append(boton)
    app.mainloop()
estacionamientoVentana()