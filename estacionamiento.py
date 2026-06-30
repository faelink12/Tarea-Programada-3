import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from funciones import guardarBaseDatos
from funciones import crearVoucherPdf
from funciones import crearFacturaPdf
from funciones import calcularCantidadEspeciales
from funciones import convertirIdATexto
from funciones import convertirTextoAId
from funciones import calcularMontoEstadia
from funciones import obtenerMarcasYTiposApi

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

#estructura del estacionamiento
def denominarEspacios(tamanioEstacionamiento, tieneElectrico):
    cantidadEspeciales = calcularCantidadEspeciales(tamanioEstacionamiento)
    cantidadElectricos = 1 if tieneElectrico else 0
    cantidadNormales = tamanioEstacionamiento - cantidadEspeciales - cantidadElectricos
    if cantidadNormales < 0:
        cantidadNormales = 0
    espacios = []
    for i in range(cantidadNormales):
        espacios.append({"tipo": "normal", "carro": None})
    for i in range(cantidadEspeciales):
        espacios.append({"tipo": "discapacidad", "carro": None})
    if tieneElectrico:
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

#esto es de obtener vehículos y vouchers
def existeEspacioElectrico(espacios):
    for espacio in espacios:
        if espacio["tipo"] == "electrico":
            return True
    return False

def obtenerUbicacionesGeneralesLibres(espacios):
    ubicacionesGeneralesLibres = []
    numeroEspacio = 0
    for espacio in espacios:
        numeroEspacio += 1
        if espacio["tipo"] == "normal" and espacio["carro"] is None:
            ubicacionesGeneralesLibres.append(numeroEspacio)
    return ubicacionesGeneralesLibres

def contarEspaciosGeneralesOcupados(espacios):
    contadorOcupados = 0
    for espacio in espacios:
        if espacio["tipo"] == "normal" and espacio["carro"] is not None:
            contadorOcupados += 1
    return contadorOcupados

def ocuparEspaciosMasivos(diccionarioVehiculos, espacios):
    for placa, datos in diccionarioVehiculos.items():
        ubicacion = int(datos[3])
        indice = ubicacion - 1
        if indice >= 0 and indice < len(espacios):
            espacios[indice]["carro"] = placa

def agregarObjetosEstacionamiento(listaObjetos, diccionarioVehiculos):
    contador = len(listaObjetos) + 1
    for placa, datos in diccionarioVehiculos.items():
        objeto = Estacionamiento(contador, placa, datos[0], datos[1], datos[2], datos[3], datos[4], datos[5], datos[6], datos[7])
        listaObjetos.append(objeto)
        contador += 1

def estacionamientoVentana(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo, montoHora, tiempoDeGracia, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago):
    app = tk.Toplevel()
    app.title("Estacionamiento")
    app.config(bg="#2D2F33")
    espacios = espaciosEstacionamiento
    columnas = 10
    botones = [None] * len(espacios)
    ventanaAbierta = [None]
    tk.Label(app, text="Estacionamiento", bg="#2D2F33", fg="White", font=("SansSerif", 16, "bold")).grid(row=0, column=0, columnspan=columnas, pady=15)
    tk.Button(app, text="Baño", bg="#8B1475", fg="white", width=8, height=2, relief="flat", bd=1).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(app, text="Casetilla", bg="#8B1475", fg="white", width=8, height=2, relief="flat", bd=1).grid(row=1, column=1, padx=5, pady=5)
    for indice in range(len(espacios)):
        fila = 2 + (indice // columnas)
        columna = indice % columnas
        boton = tk.Button(app, text="#" + str(indice + 1), bg=colorEspacio(espacios[indice]), command=lambda n=indice: observarEspacio(diccionario, listaObjetos, espacios[n], ventanaAbierta, n + 1, espacios, botones, archivoBaseDatos, carpetaVouchers, urlApiMockaroo, montoHora, tiempoDeGracia, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=fila, column=columna, padx=5, pady=5)
        botones[indice] = boton

def actualizarUbicacionesDisponibles(tipoEspacioSeleccionado, tipoInternoPorTexto, espacios, menuUbicacion, entryUbicacion):
    tipoInternoSeleccionado = tipoInternoPorTexto[tipoEspacioSeleccionado]
    ubicacionesDisponibles = obtenerUbicacionesLibresPorTipo(espacios, tipoInternoSeleccionado)
    textoUbicacionesDisponibles = []
    for ubicacionDisponible in ubicacionesDisponibles:
        textoUbicacionesDisponibles.append(str(ubicacionDisponible))
    menuDesplegableUbicacion = menuUbicacion["menu"]
    menuDesplegableUbicacion.delete(0, "end")
    for textoUbicacion in textoUbicacionesDisponibles:
        menuDesplegableUbicacion.add_command(label=textoUbicacion, command=lambda valorUbicacion=textoUbicacion: entryUbicacion.set(valorUbicacion))
    if len(textoUbicacionesDisponibles) > 0:
        entryUbicacion.set(textoUbicacionesDisponibles[0])
    else:
        entryUbicacion.set("")

def observarEspacio(diccionario, listaObjetos, espacio, ventanaAbierta, numero, espacios, botones, archivoBaseDatos, carpetaVouchers, urlApiMockaroo, montoHora, tiempoDeGracia, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago):
    if ventanaAbierta[0] is not None:
        ventanaAbierta[0].destroy()
    app = tk.Toplevel()
    ventanaAbierta[0] = app
    app.title("Información del espacio")
    app.geometry("560x380")
    if espacio["carro"] is not None:
        app.config(bg="#F15959")
        app.resizable(False, False)
        placa = espacio["carro"]
        tk.Label(app, text="#Campo").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=numero).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Placa").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=placa).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Marca").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=convertirIdATexto(catalogoMarcas, diccionario[placa][0], "Desconocida")).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        tk.Label(app, text="Color").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=convertirIdATexto(catalogoColores, diccionario[placa][1], "Desconocido")).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        tk.Label(app, text="Tipo").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=convertirIdATexto(catalogoTipos, diccionario[placa][2], "Desconocido")).grid(row=4, column=1, sticky="w", padx=5, pady=5)
        tk.Label(app, text="Hora de entrada").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=diccionario[placa][4]).grid(row=5, column=1, sticky="w", padx=5, pady=5)
        frameBotones = tk.Frame(app, bg="#F15959")
        frameBotones.grid(row=0, column=2, rowspan=6, padx=20, pady=20, sticky="ns")
        tk.Button(frameBotones, text="Pagar", command=lambda: pagar(diccionario, listaObjetos, espacios, botones, espacio, placa, archivoBaseDatos, carpetaVouchers, app, montoHora, tiempoDeGracia, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago), bg="#0d7703", fg="white", font=("SansSerif", 10, "bold"), padx=15, pady=10).pack(pady=5)
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
        marcasDinamicas, tiposDinamicos = obtenerMarcasYTiposApi(urlApiMockaroo, catalogoMarcas, catalogoTipos)
        entryMarca = tk.StringVar()
        entryMarca.set(marcasDinamicas[0])
        tk.OptionMenu(app, entryMarca, *marcasDinamicas).grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Color").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        entryColor = tk.StringVar()
        entryColor.set(convertirIdATexto(catalogoColores, 0, "Desconocido"))
        tk.OptionMenu(app, entryColor, *catalogoColores.values()).grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Tipo").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        entryTipo = tk.StringVar()
        entryTipo.set(tiposDinamicos[0])
        tk.OptionMenu(app, entryTipo, *tiposDinamicos).grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Hora de entrada").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        entryHora = tk.Entry(app)
        entryHora.insert(0, horaEntrada)
        entryHora.config(state="readonly")
        entryHora.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Tipo de espacio requerido").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        textoTipoEspacio = {"normal": "General", "discapacidad": "Especial", "electrico": "Eléctrico"}
        tipoInternoPorTexto = {"General": "normal", "Especial": "discapacidad", "Eléctrico": "electrico"}
        tipoEspacioInicial = textoTipoEspacio.get(espacio["tipo"], "General")
        ubicacionesDisponiblesInicial = obtenerUbicacionesLibresPorTipo(espacios, tipoInternoPorTexto[tipoEspacioInicial])
        textoUbicacionesInicial = []
        for ubicacionDisponible in ubicacionesDisponiblesInicial:
            textoUbicacionesInicial.append(str(ubicacionDisponible))
        entryUbicacion = tk.StringVar()
        if len(textoUbicacionesInicial) > 0:
            entryUbicacion.set(textoUbicacionesInicial[0])
        else:
            entryUbicacion.set("")
        tk.Label(app, text="Ubicación disponible").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        menuUbicacion = tk.OptionMenu(app, entryUbicacion, *textoUbicacionesInicial)
        menuUbicacion.grid(row=7, column=1, sticky="ew", padx=5, pady=5)
        entryTipoEspacio = tk.StringVar()
        entryTipoEspacio.set(tipoEspacioInicial)
        tk.OptionMenu(app, entryTipoEspacio, *textoTipoEspacio.values(), command=lambda tipoEspacioSeleccionado: actualizarUbicacionesDisponibles(tipoEspacioSeleccionado, tipoInternoPorTexto, espacios, menuUbicacion, entryUbicacion)).grid(row=6, column=1, sticky="ew", padx=5, pady=5)
        frameBotones = tk.Frame(app, bg=colorEspacio(espacio))
        frameBotones.grid(row=0, column=2, rowspan=8, padx=20, pady=20, sticky="ns")
        tk.Button(frameBotones, text="Estacionar", command=lambda: estacionarVehiculo(diccionario, listaObjetos, espacios, botones, entryUbicacion.get(), entryPlaca.get(), entryMarca.get(), entryColor.get(), entryTipo.get(), entryTipoEspacio.get(), horaEntrada, archivoBaseDatos, carpetaVouchers, app, montoHora), bg="#0d7703", fg="white", font=("SansSerif", 10, "bold"), padx=15, pady=10).pack(pady=5)
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

def estacionarVehiculo(diccionario, listaObjetos, espacios, botones, ubicacionSeleccionadaTexto, placa, marcaTexto, colorTexto, tipoTexto, tipoEspacioTexto, fechaHoraEntrada, archivoBaseDatos, carpetaVouchers, app, montoHora):
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
    if marcaTexto == "":
        messagebox.showwarning("Estacionar vehículo", "Debe seleccionar la marca del vehículo.")
        return
    if colorTexto == "":
        messagebox.showwarning("Estacionar vehículo", "Debe seleccionar el color del vehículo.")
        return
    if tipoTexto == "":
        messagebox.showwarning("Estacionar vehículo", "Debe seleccionar el tipo del vehículo.")
        return
    if ubicacionSeleccionadaTexto == "":
        messagebox.showwarning("Estacionar vehículo", "No hay espacios disponibles del tipo seleccionado.")
        return
    numeroEspacio = int(ubicacionSeleccionadaTexto)
    indice = numeroEspacio - 1
    if indice < 0 or indice >= len(espacios):
        messagebox.showerror("Estacionar vehículo", "El espacio seleccionado no es válido.")
        return
    if espacios[indice]["carro"] is not None:
        messagebox.showwarning("Estacionar vehículo", "El espacio seleccionado ya está ocupado.")
        return
    tipoEspacioReal = {"normal": "General", "discapacidad": "Especial", "electrico": "Eléctrico"}.get(espacios[indice]["tipo"], "General")
    if tipoEspacioTexto != tipoEspacioReal:
        messagebox.showwarning("Estacionar vehículo", "El tipo de espacio requerido (" + tipoEspacioTexto + ") no coincide con el espacio seleccionado (" + tipoEspacioReal + ").")
        return
    confirmar = messagebox.askyesno("Estacionar vehículo", f"El costo es de ₡{montoHora[0]} por hora.\n\n¿Confirma la reserva del espacio #{numeroEspacio}?")
    if not confirmar:
        return
    marca = convertirTextoAId(marcas, marcaTexto, 0)
    color = convertirTextoAId(colores, colorTexto, 0)
    tipo = convertirTextoAId(tiposVehiculo, tipoTexto, 0)
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
    crearVoucherPdf(objeto, carpetaVouchers, marcas, colores, tiposVehiculo)
    messagebox.showinfo("Estacionar vehículo", "Vehículo estacionado correctamente.\n\nPlaca: " + placa + "\nCampo: " + ubicacion)
    app.destroy()

def obtenerUbicacionesLibresPorTipo(espacios, tipoEspacioBuscado):
    ubicacionesLibresDelTipo = []
    numeroEspacio = 0
    for espacio in espacios:
        numeroEspacio += 1
        if espacio["tipo"] == tipoEspacioBuscado and espacio["carro"] is None:
            ubicacionesLibresDelTipo.append(numeroEspacio)
    return ubicacionesLibresDelTipo

def pagar(diccionario, listaObjetos, espacios, botones, espacio, placa, archivoBaseDatos, carpetaVouchers, mainApp, montoHora, tiempoDeGracia, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago):
    fechaSalidaStr = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    monto = calcularMontoEstadia(diccionario[placa][4], fechaSalidaStr, montoHora[0], tiempoDeGracia[0])
    app = tk.Toplevel()
    app.title("Tipo de pago")
    app.geometry("300x200")
    tk.Label(app, text="Elija su tipo de pago", font=("SansSerif", 14, "bold")).pack(pady=10)
    entryTipoPago = tk.StringVar()
    entryTipoPago.set(catalogoTiposPago[1])
    tk.OptionMenu(app, entryTipoPago, *catalogoTiposPago.values()).pack(pady=5)
    tk.Label(app, text=f"Monto a pagar: ₡{monto}", font=("SansSerif", 12)).pack(pady=5)
    tk.Button(app, text="Confirmar pago", bg="#0d7703", fg="white", command=lambda: confirmarPago(diccionario, listaObjetos, espacios, botones, espacio, placa, entryTipoPago.get(), monto, fechaSalidaStr, archivoBaseDatos, carpetaVouchers, app, mainApp, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago)).pack(pady=10)

def confirmarPago(diccionario, listaObjetos, espacios, botones, espacio, placa, tipoPagoTexto, monto, fechaSalidaStr, archivoBaseDatos, carpetaVouchers, app, mainApp, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago):
    tiposPagoInverso = {}
    for idTipoPago, textoTipoPago in catalogoTiposPago.items():
        tiposPagoInverso[textoTipoPago] = idTipoPago
    tiposPagoInt = tiposPagoInverso[tipoPagoTexto]
    diccionario[placa][5] = fechaSalidaStr
    diccionario[placa][6] = monto
    diccionario[placa][7] = tiposPagoInt
    indice = espacios.index(espacio)
    for objeto in listaObjetos:
        if objeto.info[0] == placa:
            objeto.estadia[2] = fechaSalidaStr
            objeto.pago = (monto, tiposPagoInt)
            crearFacturaPdf(objeto, carpetaVouchers, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago)
            break
    del diccionario[placa]
    espacio["carro"] = None
    botones[indice].config(bg=colorEspacio(espacio))
    guardarBaseDatos(listaObjetos, archivoBaseDatos)
    messagebox.showinfo("Pago", f"Pago realizado correctamente. \nMonto: ₡{monto}\nTipo: {tipoPagoTexto}")
    app.destroy()
    mainApp.destroy()

def regresar(app):
    app.destroy()
