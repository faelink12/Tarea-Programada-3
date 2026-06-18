import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from funciones import guardarBaseDatos
from funciones import crearVoucherPdf

marcas = (
    'Acura', 'Aston Martin', 'Audi', 'BMW', 'Buick', 'Cadillac', 'Chevrolet',
    'Chrysler', 'Daihatsu', 'Dodge', 'Ford', 'GMC', 'Honda', 'Hyundai', 'Infiniti',
    'Isuzu', 'Jaguar', 'Jeep', 'Kia', 'Lamborghini', 'Lexus', 'Lincoln', 'Mazda',
    'Mercedes-Benz', 'Mercury', 'Mitsubishi', 'Nissan', 'Oldsmobile', 'Plymouth',
    'Pontiac', 'Porsche', 'Saab', 'Scion', 'Subaru', 'Suzuki', 'Toyota',
    'Volkswagen', 'Volvo'
)

colores = [
    'Aquamarina', 'Azul', 'Carmesí', 'Fucsia', 'Dorado', 'Verde', 'Indigo',
    'Caqui', 'Marrón', 'Malva', 'Naranja', 'Rosado', 'Pardo Rojizo', 'Morado', 'Rojo',
    'Verde Azulado', 'Turquesa', 'Violeta', 'Amarillo'
]

tiposVehiculo = [
    'Automovil', 'SUV', 'Pickup', 'Motocicleta', 'Microbus', 'Camioneta',
    'Sedan', 'Hatchback', 'Coupe', 'Convertible', 'Minivan'
]

class Estacionamiento:
    def __init__(self, id, placa, marca, color, tipo, ubicacion, fechaHoraEntrada, fechaHoraSalida, monto, tipoPago):
        self.id = id
        self.info = (placa, marca, color, tipo)
        self.estadia = [ubicacion, fechaHoraEntrada, fechaHoraSalida]
        self.pago = (monto, tipoPago)

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

def estacionamientoVentana(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers):
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
        boton = tk.Button(app, text="#" + str(i + 1), bg=colorEspacio(espacios[i]), command=lambda n=i: observarEspacio(diccionario, listaObjetos, espacios[n], ventanaAbierta, n + 1, espacios, botones, archivoBaseDatos, carpetaVouchers), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=1, column=i + 1, padx=5, pady=5)
        botones[i] = boton
    tk.Label(app, text="- - " * 20, bg="#2D2F33", fg="#EED42B", font=("arial", 18, "bold")).grid(row=2, column=1, columnspan=9, pady=5)
    for i in range(9, 17):
        boton = tk.Button(app, text="#" + str(i + 1), bg=colorEspacio(espacios[i]), command=lambda n=i: observarEspacio(diccionario, listaObjetos, espacios[n], ventanaAbierta, n + 1, espacios, botones, archivoBaseDatos, carpetaVouchers), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=3, column=i - 8, padx=5, pady=5)
        botones[i] = boton
    especiales = [17, 18, 19]
    for num, valor in enumerate(especiales):
        boton = tk.Button(app, text="#" + str(valor + 1), bg=colorEspacio(espacios[valor]), command=lambda n=valor: observarEspacio(diccionario, listaObjetos, espacios[n], ventanaAbierta, n + 1, espacios, botones, archivoBaseDatos, carpetaVouchers), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=num + 1, column=11, padx=5, pady=5)
        botones[valor] = boton

def convertirTipoEstacionamiento(tipoRequerido):
    if tipoRequerido == "General":
        return "normal"
    if tipoRequerido == "Especial":
        return "discapacidad"
    if tipoRequerido == "Eléctrico":
        return "electrico"
    return "normal"

def obtenerUbicacionesDisponiblesPorTipo(espacios, tipoRequerido):
    tipoEspacio = convertirTipoEstacionamiento(tipoRequerido)
    ubicaciones = []
    contador = 0
    for espacio in espacios:
        contador += 1
        if espacio["tipo"] == tipoEspacio and espacio["carro"] is None:
            ubicaciones.append(contador)
    return ubicaciones

def actualizarUbicacionesDisponibles(espacios, tipoRequerido, variableUbicacion, menuUbicacion):
    ubicaciones = obtenerUbicacionesDisponiblesPorTipo(espacios, tipoRequerido)
    menu = menuUbicacion["menu"]
    menu.delete(0, "end")
    if len(ubicaciones) == 0:
        variableUbicacion.set("")
        return
    variableUbicacion.set(str(ubicaciones[0]))
    for ubicacion in ubicaciones:
        menu.add_command(label=str(ubicacion), command=lambda valor=ubicacion: variableUbicacion.set(str(valor)))

def observarEspacio(diccionario, listaObjetos, espacio, ventanaAbierta, numero, espacios, botones, archivoBaseDatos, carpetaVouchers):
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
        tk.Label(app, text=diccionario[placa][0]).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        tk.Label(app, text="Color").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=diccionario[placa][1]).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        tk.Label(app, text="Tipo").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=diccionario[placa][2]).grid(row=4, column=1, sticky="w", padx=5, pady=5)
        tk.Label(app, text="Hora de entrada").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=diccionario[placa][4]).grid(row=5, column=1, sticky="w", padx=5, pady=5)
        frameBotones = tk.Frame(app, bg="#F15959")
        frameBotones.grid(row=0, column=2, rowspan=6, padx=20, pady=20, sticky="ns")
        tk.Button(frameBotones, text="Pagar", bg="#0d7703", fg="white", font=("SansSerif", 10, "bold"), padx=15, pady=10).pack(pady=5)
        tk.Button(frameBotones, text="Regresar", command=lambda: regresar(app), bg="#770303", fg="white", font=("SansSerif", 10), padx=15, pady=10).pack(pady=5)
    else:
        app.config(bg=colorEspacio(espacio))
        app.resizable(False, False)
        horaEntrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        montoPorHora = 1000
        tk.Label(app, text="Placa").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entryPlaca = tk.Entry(app)
        entryPlaca.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Marca").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entryMarca = tk.StringVar()
        entryMarca.set(marcas[0])
        tk.OptionMenu(app, entryMarca, *marcas).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Color").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entryColor = tk.StringVar()
        entryColor.set(colores[0])
        tk.OptionMenu(app, entryColor, *colores).grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Tipo vehículo").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        entryTipo = tk.StringVar()
        entryTipo.set(tiposVehiculo[0])
        tk.OptionMenu(app, entryTipo, *tiposVehiculo).grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Tipo estacionamiento").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        entryTipoEstacionamiento = tk.StringVar()
        entryTipoEstacionamiento.set("General")
        menuTipoEstacionamiento = tk.OptionMenu(app, entryTipoEstacionamiento, "General", "Especial", "Eléctrico")
        menuTipoEstacionamiento.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Ubicación disponible").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        entryUbicacion = tk.StringVar()
        ubicacionesIniciales = obtenerUbicacionesDisponiblesPorTipo(espacios, entryTipoEstacionamiento.get())
        if len(ubicacionesIniciales) > 0:
            entryUbicacion.set(str(ubicacionesIniciales[0]))
        else:
            entryUbicacion.set("")
        menuUbicacion = tk.OptionMenu(app, entryUbicacion, *ubicacionesIniciales)
        menuUbicacion.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
        entryTipoEstacionamiento.trace_add("write", lambda *args: actualizarUbicacionesDisponibles(espacios, entryTipoEstacionamiento.get(), entryUbicacion, menuUbicacion))
        tk.Label(app, text="Hora de entrada").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        entryHora = tk.Entry(app)
        entryHora.insert(0, horaEntrada)
        entryHora.config(state="readonly")
        entryHora.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Costo por hora: ₡" + str(montoPorHora), bg=colorEspacio(espacio), font=("SansSerif", 10, "bold")).grid(row=7, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        frameBotones = tk.Frame(app, bg=colorEspacio(espacio))
        frameBotones.grid(row=0, column=2, rowspan=8, padx=20, pady=20, sticky="ns")
        tk.Button(frameBotones, text="Estacionar", command=lambda: estacionarVehiculo(diccionario, listaObjetos, espacios, botones, entryUbicacion.get(), entryPlaca.get(), entryMarca.get(), entryColor.get(), entryTipo.get(), horaEntrada, montoPorHora, archivoBaseDatos, carpetaVouchers, app), bg="#0d7703", fg="white", font=("SansSerif", 10, "bold"), padx=15, pady=10).pack(pady=5)
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

def estacionarVehiculo(diccionario, listaObjetos, espacios, botones, numeroEspacio, placa, marca, color, tipo, fechaHoraEntrada, montoPorHora, archivoBaseDatos, carpetaVouchers, app):
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
    if numeroEspacio == "":
        messagebox.showwarning("Estacionar vehículo", "No hay ubicaciones disponibles para el tipo de estacionamiento seleccionado.")
        return
    try:
        numeroEspacio = int(numeroEspacio)
    except ValueError:
        messagebox.showwarning("Estacionar vehículo", "La ubicación seleccionada no es válida.")
        return
    confirmar = messagebox.askyesno("Confirmar reserva", "¿Desea reservar este espacio?\n\nEsta acción implica un cobro de ₡" + str(montoPorHora) + " por hora.")
    if not confirmar:
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