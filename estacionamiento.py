import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from funciones import guardarBaseDatos
from funciones import crearVoucherPdf
from funciones import crearPlaca
from funciones import crearFacturaPdf
import json
import random
from datetime import datetime

marcas = {
    0: 'Acura', 1: 'Aston Martin', 2: 'Audi', 3:'BMW', 4:'Buick', 5:'Cadillac', 6:'Chevrolet', 
7:'Chrysler', 8:'Daihatsu', 9:'Dodge', 10:'Ford', 11:'GMC', 12:'Honda', 13:'Hyundai', 14:'Infiniti', 
15:'Isuzu', 16:'Jaguar', 17:'Jeep', 18:'Kia', 19:'Lamborghini', 20:'Lexus', 21:'Lincoln', 22:'Mazda', 
23:'Mercedes-Benz', 24:'Mercury', 25:'Mitsubishi', 26:'Nissan', 27:'Oldsmobile', 28:'Plymouth', 
29:'Pontiac', 30:'Porsche', 31:'Saab', 32:'Scion', 33:'Subaru',34:'Suzuki', 35:'Toyota', 
36:'Volkswagen', 37:'Volvo'
}

colores = {
    0:'Aquamarina', 1:'Azul', 2:'Carmesí', 3:'Fucsia', 4:'Dorado', 5:'Verde', 6:'Indigo', 
7:'Caqui', 8:'Marrón', 9:'Malva', 10:'Naranja', 11:'Rosado', 12:'Pardo Rojizo', 13:'Morado', 14:'Rojo', 
15:'Verde Azulado', 16:'Turquesa', 17:'Violeta', 18:'Amarillo'
}

tiposVehiculo = {
    0: 'Automovil', 1:'SUV', 2:'Pickup', 3:'Motocicleta', 4:'Microbus', 5:'Camioneta',
    6:'Sedan', 7:'Hatchback', 8:'Coupe', 9:'Convertible', 10:'Minivan'
}

tiposPago = {1: "Efectivo", 2: "SINPE", 3: "Tarjeta"}

class Estacionamiento:
    def __init__(self, id, placa, marca, color, tipo, ubicacion, fechaHoraEntrada, fechaHoraSalida, monto, tipoPago):
        self.id = id
        self.info = (placa, marca, color, tipo)
        self.estadia = [ubicacion, fechaHoraEntrada, fechaHoraSalida]
        self.pago = (monto, tipoPago)

def crearDiccionarioJSON():
    marcasInversas = {v: l for l, v in marcas.items()}
    coloresInversos = {v: l for l, v in colores.items()}
    tiposInversos = {v: l for l, v in tiposVehiculo.items()}
    with open("MOCK_DATA.json", "r", encoding="utf-8-sig") as jason:
        datos = json.load(jason)
    ubicaciones = list(range(1, 18))
    random.shuffle(ubicaciones)
    diccionario = {}
    for i, carro in enumerate(datos):
        placa = crearPlaca()
        diccionario[placa] = [
           marcasInversas.get(carro["Marca"]),
            coloresInversos.get(carro["Color"]),
            tiposInversos.get(carro["Tipo de Carro"]),
            ubicaciones[i],
            carro["fechaHoraEntrada"],
            carro["fechaHoraSalida"],
            carro["Monto"],
            carro["Tipo de pago"],
        ]
    return diccionario

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

def regresar(app):
    app.destroy()

def estacionamientoVentana(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, montoHora):
    app = tk.Toplevel()
    app.title("Estacionamiento")
    app.geometry("750x350")
    app.resizable(False, False)
    app.config(bg="#2D2F33")
    espacios = espaciosEstacionamiento
    botones = [None] * 20
    ventanaAbierta = [None]
    tk.Label(app, text="Estacionamiento", bg="#2D2F33", fg="White", font=("SansSerif", 16, "bold")).grid(row=0, column=0, columnspan=10, pady=15)
    tk.Button(app, text="Baño", bg="#8B1475", fg="white", width=6, height=2, relief="flat", bd=1).grid(row=1, column=0, padx=5, pady=5)
    tk.Label(app, text="Entrada", bg="#2D2F33", fg="white", font=("SansSerif", 8)).grid(row=2, column=0, padx=5)
    tk.Button(app, text="Casetilla", bg="#8B1475", fg="white", width=6, height=2, relief="flat", bd=1).grid(row=3, column=0, padx=5, pady=5)
    for i in range(9):
        boton = tk.Button(app, text="#" + str(i + 1), bg=colorEspacio(espacios[i]), command=lambda n=i: observarEspacio(diccionario, listaObjetos, espacios[n], ventanaAbierta, n + 1, espacios, botones, archivoBaseDatos, carpetaVouchers,montoHora), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=1, column=i + 1, padx=5, pady=5)
        botones[i] = boton
    tk.Label(app, text="- - " * 20, bg="#2D2F33", fg="#EED42B", font=("arial", 18, "bold")).grid(row=2, column=1, columnspan=9, pady=5)
    for i in range(9, 17):
        boton = tk.Button(app, text="#" + str(i + 1), bg=colorEspacio(espacios[i]), command=lambda n=i: observarEspacio(diccionario, listaObjetos, espacios[n], ventanaAbierta, n + 1, espacios, botones, archivoBaseDatos, carpetaVouchers, montoHora), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=3, column=i - 8, padx=5, pady=5)
        botones[i] = boton
    especiales = [17, 18, 19]
    for num, valor in enumerate(especiales):
        boton = tk.Button(app, text="#" + str(valor + 1), bg=colorEspacio(espacios[valor]), command=lambda n=valor: messagebox.showinfo("No disponible", f"El espacio #{n + 1} no está disponible ya que es un espacio especial."), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=num + 1, column=11, padx=5, pady=5)
        botones[valor] = boton
    app.mainloop()

def pagar(diccionario, listaObjetos, espacios, botones, espacio, placa, archivoBaseDatos, carpetaVouchers, mainApp, montoHora):
    fechaEntrada = datetime.strptime(diccionario[placa][4], "%Y-%m-%d %H:%M:%S")
    fechaSalida = datetime.now()
    horas = (fechaSalida - fechaEntrada).total_seconds() / 3600
    monto = round(horas*montoHora[0])
    fechaSalidaStr = fechaSalida.strftime("%Y-%m-%d %H:%M:%S")
    app = tk.Toplevel()
    app.title("Tipo de pago")
    app.geometry("300x200")
    tk.Label(app, text="Elija su tipo de pago", font=("SansSerif", 14, "bold")).pack(pady=10)
    entryTipoPago = tk.StringVar()
    entryTipoPago.set(tiposPago[1])
    tk.OptionMenu(app, entryTipoPago, *tiposPago.values()).pack(pady=5)
    tk.Label(app, text=f"Monto a pagar: ₡{monto}", font=("SansSerif", 12)).pack(pady=5)
    tk.Button(app, text="Confirmar pago", bg="#0d7703", fg="white", command=lambda: confirmarPago(diccionario, listaObjetos, espacios, botones, espacio, placa, entryTipoPago.get(), monto, fechaSalidaStr, archivoBaseDatos, carpetaVouchers, app, mainApp)).pack(pady=10)

def confirmarPago(diccionario, listaObjetos, espacios, botones, espacio, placa, tipoPagoTexto, monto, fechaSalidaStr, archivoBaseDatos, carpetaVouchers, app, mainApp):
    tiposPagoInverso = {v: k for k,v in tiposPago.items()}
    tiposPagoInt = tiposPagoInverso[tipoPagoTexto]
    diccionario[placa][5] = fechaSalidaStr
    diccionario[placa][6] = monto
    diccionario[placa][7] = tiposPagoInt
    for objeto in listaObjetos:
        if objeto.info[0] == placa:
            objeto.estadia[2] = fechaSalidaStr
            objeto.pago = (monto, tiposPagoInt)
            crearFacturaPdf(objeto, carpetaVouchers)
            break
    espacio["carro"] = None
    indice = int(diccionario[placa][3]) - 1
    botones[indice].config(bg=colorEspacio(espacio))
    guardarBaseDatos(listaObjetos, archivoBaseDatos)
    messagebox.showinfo("Pago", f"Pago realizado correctamente. \nMonto: ₡{monto}\nTipo: {tipoPagoTexto}")
    app.destroy()
    mainApp.destroy()

def observarEspacio(diccionario, listaObjetos, espacio, ventanaAbierta, numero, espacios, botones, archivoBaseDatos, carpetaVouchers, montoHora):
    if ventanaAbierta[0] is not None:
        ventanaAbierta[0].destroy()
    app = tk.Toplevel()
    ventanaAbierta[0] = app
    app.title("Información del espacio")
    app.geometry("470x270")
    if espacio["carro"] is not None:
        app.config(bg="#F15959")
        app.resizable(False, False)
        placa = espacio["carro"]
        tk.Label(app, text="#Campo").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=numero).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Placa").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=placa).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Marca").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=marcas[diccionario[placa][0]]).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        tk.Label(app, text="Color").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=colores[diccionario[placa][1]]).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        tk.Label(app, text="Tipo").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=tiposVehiculo[diccionario[placa][2]]).grid(row=4, column=1, sticky="w", padx=5, pady=5)
        tk.Label(app, text="Hora de entrada").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=diccionario[placa][4]).grid(row=5, column=1, sticky="w", padx=5, pady=5)
        frameBotones = tk.Frame(app, bg="#F15959")
        frameBotones.grid(row=0, column=2, rowspan=6, padx=20, pady=20, sticky="ns")
        tk.Button(frameBotones, text="Pagar", command=lambda: pagar(diccionario, listaObjetos, espacios, botones, espacio, placa, archivoBaseDatos, carpetaVouchers, app, montoHora), bg="#0d7703", fg="white", font=("SansSerif", 10, "bold"), padx=15, pady=10).pack(pady=5)
        tk.Button(frameBotones, text="Regresar", command=lambda: regresar(app), bg="#770303", fg="white", font=("SansSerif", 10), padx=15, pady=10).pack(pady=5)
    else:
        app.config(bg=colorEspacio(espacio))
        app.resizable(False, False)
        horaEntrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tk.Label(app, text="#Campo").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=numero).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Placa").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entryPlaca = tk.Entry(app)
        entryPlaca.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Marca").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entryMarca = tk.StringVar()
        entryMarca.set(marcas[0])
        tk.OptionMenu(app, entryMarca, *marcas.values()).grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Color").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        entryColor = tk.StringVar()
        entryColor.set(colores[0])
        tk.OptionMenu(app, entryColor, *colores.values()).grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Tipo").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        entryTipo = tk.StringVar()
        entryTipo.set(tiposVehiculo[0])
        tk.OptionMenu(app, entryTipo, *tiposVehiculo.values()).grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Hora de entrada").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        entryHora = tk.Entry(app)
        entryHora.insert(0, horaEntrada)
        entryHora.config(state="readonly")
        entryHora.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        frameBotones = tk.Frame(app, bg=colorEspacio(espacio))
        frameBotones.grid(row=0, column=2, rowspan=6, padx=20, pady=20, sticky="ns")
        tk.Button(frameBotones, text="Estacionar", command=lambda: estacionarVehiculo(diccionario, listaObjetos, espacios, botones, numero, entryPlaca.get(), entryMarca.get(), entryColor.get(), entryTipo.get(), horaEntrada, archivoBaseDatos, carpetaVouchers, app), bg="#0d7703", fg="white", font=("SansSerif", 10, "bold"), padx=15, pady=10).pack(pady=5)
        tk.Button(frameBotones, text="Regresar", command=lambda: regresar(app), bg="#770303", fg="white", font=("SansSerif", 10), padx=15, pady=10).pack(pady=5)

def validarPlaca(placa):
    if len(placa) != 7:
        return False
    if placa[3] != "-":
        return False
    letras = placa[0:3]
    numeros = placa[4:7]
    if not letras.isalpha():
        return False
    if not numeros.isdigit():
        return False
    return True

def estacionarVehiculo(diccionario, listaObjetos, espacios, botones, numeroEspacio, placa, marca, color, tipo, fechaHoraEntrada, archivoBaseDatos, carpetaVouchers, app):
    placa = placa.upper().strip()
    if len(placa) == 6:
        if placa[0:3].isalpha() and placa[3:6].isdigit():
            placa = placa[0:3] + "-" + placa[3:6]
    if placa == "":
        messagebox.showwarning("Estacionar vehículo", "Debe ingresar la placa del vehículo.")
        return
    if not validarPlaca(placa):
        messagebox.showwarning("Estacionar vehículo", "La placa debe tener el formato ABC-123.")
        return
    if placa in diccionario:
        messagebox.showwarning("Estacionar vehículo", "Ya existe un vehículo estacionado con esa placa.")
        return
    if marca == "":
        messagebox.showwarning("Estacionar vehículo", "Debe seleccionar la marca del vehículo.")
        return
    if color == "":
        messagebox.showwarning("Estacionar vehículo", "Debe seleccionar el color del vehículo.")
        return
    if tipo == "":
        messagebox.showwarning("Estacionar vehículo", "Debe seleccionar el tipo del vehículo.")
        return
    indice = numeroEspacio - 1
    if indice < 0 or indice >= len(espacios):
        messagebox.showerror("Estacionar vehículo", "El espacio seleccionado no es válido.")
        return
    if espacios[indice]["carro"] is not None:
        messagebox.showwarning("Estacionar vehículo", "El espacio seleccionado ya está ocupado.")
        return
    ubicacion = str(numeroEspacio)
    fechaHoraSalida = ""
    monto = 0
    tipoPago = 0
    diccionario[placa] = [marca, color, tipo, ubicacion, fechaHoraEntrada, fechaHoraSalida, monto, tipoPago]
    idObjeto = len(listaObjetos) + 1
    objeto = Estacionamiento(idObjeto, placa, marca, color, tipo, ubicacion, fechaHoraEntrada, fechaHoraSalida, monto, tipoPago)
    listaObjetos.append(objeto)
    espacios[indice]["carro"] = placa
    botones[indice].config(bg=colorEspacio(espacios[indice]))
    guardarBaseDatos(listaObjetos, archivoBaseDatos)
    crearVoucherPdf(objeto, carpetaVouchers)
    messagebox.showinfo("Estacionar vehículo", "Vehículo estacionado correctamente.\n\nPlaca: " + placa + "\nCampo: " + ubicacion)
    app.destroy()

def ocuparEspaciosMasivos(diccionarioVehiculos, espacios):
    for placa, datos in diccionarioVehiculos.items():
        ubicacion = int(datos[3])
        indice = ubicacion - 1
        if indice >= 0 and indice < len(espacios):
            espacios[indice]["carro"] = placa

def existeEspacioElectrico(espacios):
    for espacio in espacios:
        if espacio["tipo"] == "electrico":
            return True
    return False

def obtenerUbicacionesGeneralesLibres(espacios):
    ubicacionesLibres = []
    contador = 0
    for espacio in espacios:
        contador += 1
        if espacio["tipo"] == "normal" and espacio["carro"] is None:
            ubicacionesLibres.append(contador)
    return ubicacionesLibres

def agregarObjetosEstacionamiento(listaObjetos, diccionarioVehiculos):
    contador = len(listaObjetos) + 1
    for placa, datos in diccionarioVehiculos.items():
        objeto = Estacionamiento(contador, placa, datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7])
        listaObjetos.append(objeto)
        contador += 1