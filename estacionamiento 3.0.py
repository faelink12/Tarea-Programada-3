#funciones tp 3
import tkinter as tk
import json
import random
import string
from datetime import datetime

marcas = (
    'Acura', 'Aston Martin', 'Audi', 'BMW', 'Buick', 'Cadillac', 'Chevrolet', 
'Chrysler', 'Daihatsu', 'Dodge', 'Ford', 'GMC', 'Honda', 'Hyundai', 'Infiniti', 
'Isuzu', 'Jaguar', 'Jeep', 'Kia', 'Lamborghini', 'Lexus', 'Lincoln', 'Mazda', 
'Mercedes-Benz', 'Mercury', 'Mitsubishi', 'Nissan', 'Oldsmobile', 'Plymouth', 
'Pontiac', 'Porsche', 'Saab', 'Scion', 'Subaru','Suzuki', 'Toyota', 
'Volkswagen', 'Volvo'
)

colores = [
    'Aquamarina', 'Azul', 'Carmesí', 'Fucsia', 'Dorado', 'Verde', 'Indigo', 
'Caqui', 'Marrón', 'Malva', 'Naranja', 'Rosado', 'Pardo Rojizo', 'Morado', 'Rojo', 
'Verde Azulado', 'Turquesa', 'Violeta', 'Amarillo'
]

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

def regresar(app):
    app.destroy()

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

def observarEspacio(espacio, ventanaAbierta, numero, espacios):
    if ventanaAbierta[0] is not None:
        ventanaAbierta[0].destroy()
    app = tk.Toplevel()
    ventanaAbierta[0] = app
    app.title("Información del vehículo")
    app.geometry("450x250")
    if espacio["carro"] is not None:
        app.config(bg="#F15959")
        app.resizable(False,False)
        placa = espacio["carro"]
        tk.Label(app, text="#Campo").grid(row=0, column=0,sticky="w", padx=5, pady=5)
        tk.Label(app, text=numero).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Placa").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=espacio["carro"]).grid(row=1, column=1,sticky="ew", padx=5,pady=5)
        tk.Label(app, text="Marca").grid(row=2, column=0, sticky="w", padx=5,pady=5)
        tk.Label(app, text=diccionario[placa][0]).grid(row=2, column=1, sticky="w", padx=5,pady=5)
        tk.Label(app, text="Color").grid(row=3, column=0, sticky="w", padx=5,pady=5)
        tk.Label(app, text=diccionario[placa][1]).grid(row=3, column=1, sticky="w", padx=5,pady=5)
        tk.Label(app, text="Hora de entrada").grid(row=4, column=0, sticky="w", padx=5,pady=5)
        tk.Label(app, text=diccionario[placa][4]).grid(row=4, column=1, sticky="w", padx=5,pady=5)
        frameBotones = tk.Frame(app, bg="#F15959")
        frameBotones.grid(row=0, column=2, rowspan=5, padx=20, pady=20, sticky="ns")
        tk.Button(frameBotones, text="Pagar", bg="#0d7703",fg="white", font=("SansSerif", 10, "bold"),padx=15, pady=10).pack(pady=5)
        tk.Button(frameBotones, text="Regresar", command=lambda: regresar(app), bg="#770303", fg="white", font=("SansSerif", 10), padx=15, pady=10).pack(pady=5)
    elif espacio["tipo"] == "discapacidad":
        app.config(bg="#597FF1")
    elif espacio["tipo"] == "electrico":
        app.config(bg="#F1D559")
    else:
        app.config(bg="#6FB95D")
        app.resizable(False,False)
        horaEntrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        camposDisponibles = []
        for i, esp in enumerate(espacios):
            if esp["carro"] is None:
                camposDisponibles.append(i + 1)
        tk.Label(app, text="#Campo").grid(row=0, column=0,sticky="w", padx=5, pady=5)
        entryCampo = tk.StringVar()
        tk.OptionMenu(app, entryCampo, *camposDisponibles).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Placa").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entryPlaca = tk.Entry(app)
        entryPlaca.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Marca").grid(row=2, column=0, sticky="w", padx=5,pady=5)
        entryMarca = tk.StringVar()
        tk.OptionMenu(app, entryMarca, *marcas).grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Color").grid(row=3, column=0, sticky="w", padx=5,pady=5)
        entryColor = tk.StringVar()
        tk.OptionMenu(app, entryColor, *colores).grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Hora de entrada").grid(row=4, column=0, sticky="w", padx=5,pady=5)
        entryHora = tk.Entry(app)
        entryHora.insert(0, horaEntrada)
        entryHora.config(state="readonly")
        entryHora.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        frameBotones = tk.Frame(app, bg="#6FB95D")
        frameBotones.grid(row=0, column=2, rowspan=5, padx=20, pady=20, sticky="ns")
        tk.Button(frameBotones, text="Estacionar", bg="#0d7703",fg="white", font=("SansSerif", 10, "bold"),padx=15, pady=10).pack(pady=5)
        tk.Button(frameBotones, text="Regresar", command=lambda: regresar(app), bg="#770303", fg="white", font=("SansSerif", 10), padx=15, pady=10).pack(pady=5)
        
def estacionamientoVentana():
    app = tk.Tk()
    app.title("Estacionamiento")
    app.geometry("750x350")
    app.resizable(False, False)
    app.config(bg="#2D2F33")
    espacios = denominarEspacios()
    botones = [None] * 20
    ventanaAbierta = [None]
    tk.Label(app, text="Estacionamiento", bg="#2D2F33", fg="White", font=("SansSerif", 16, "bold")).grid(row=0, column=0, columnspan=10, pady=15)
    tk.Button(app, text="Baño", bg="#8B1475", fg="white", width=6, height=2, relief="flat", bd=1).grid(row=1, column=0, padx=5, pady=5)
    tk.Label(app, text="Entrada", bg="#2D2F33", fg="white", font=("SansSerif",8)).grid(row=2, column=0, padx=5)
    tk.Button(app, text="Casetilla", bg="#8B1475", fg="white", width=6, height=2, relief="flat", bd=1).grid(row=3, column=0, padx=5, pady=5)
    for i in range(9):
        boton = tk.Button(app, text=f"#{i+1}", bg=colorEspacio(espacios[i]), command=lambda n=i: observarEspacio(espacios[n], ventanaAbierta, n + 1, espacios), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=1, column=i+1, padx=5, pady=5)
        botones[i] = boton
    tk.Label(app, text="- - " * 20, bg="#2D2F33", fg="#EED42B", font=("arial", 18, "bold")).grid(row=2, column=1, columnspan=9, pady=5)
    for i in range(9,17):
        boton = tk.Button(app, text=f"#{i+1}",bg=colorEspacio(espacios[i]), command=lambda n=i: observarEspacio(espacios[n], ventanaAbierta, n + 1, espacios), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=3, column=i-8, padx=5, pady=5)
        botones[i] = boton
    especiales = [17,18,19]
    for num, valor in enumerate(especiales):
        boton = tk.Button(app, text=f"#{valor+1}",bg=colorEspacio(espacios[valor]), command=lambda n=valor: observarEspacio(espacios[n], ventanaAbierta, n + 1, espacios), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=num+1, column=11, padx=5, pady=5)
        botones[valor] = boton
    app.mainloop()
estacionamientoVentana()
