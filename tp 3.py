import tkinter as tk
import json
import random
import string
from datetime import datetime
import os
import pickle
import urllib.request
from datetime import timedelta
from tkinter import messagebox
from fpdf import FPDF
import qrcode

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

class Estacionamiento:
    def __init__(self, id, placa, marca, color, tipo, ubicacion, fechaHoraEntrada, fechaHoraSalida, monto, tipoPago):
        self.id = id
        self.info = (placa, marca, color, tipo)
        self.estadia = [ubicacion, fechaHoraEntrada, fechaHoraSalida]
        self.pago = (monto, tipoPago)

def crearPlaca():
    """
    Funcionalidad:
        Genera una placa aleatoria en formato LLL-NNN.
    Entrada:
        - None
    Salida:
        - placa (str): Placa generada aleatoriamente.
    """
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=3))
    return letras + "-" + numeros

def crearDiccionarioJSON():
    """
    Funcionalidad:
        Lee el archivo MOCK_DATA.json y construye un diccionario con los datos
        de los vehículos usando placas generadas aleatoriamente como clave.
    Entrada:
        - None
    Salida:
        - diccionario (dict): Diccionario con placas como clave y datos del vehículo como valor.
    """
    try:
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
    except FileNotFoundError:
        print("Error: no se encontró el archivo MOCK_DATA.json")
        return {}

def regresar(app):
    """
    Funcionalidad:
        Cierra la ventana recibida como parámetro.
    Entrada:
        - app (tk.Tk o tk.Toplevel): Ventana a cerrar.
    Salida:
        - None
    """
    app.destroy()

def crearListaDiccionario(diccionario):
    """
    Funcionalidad:
        Convierte el diccionario de vehículos en una lista de objetos Estacionamiento.
    Entrada:
        - diccionario (dict): Diccionario con placas como clave y datos del vehículo como valor.
    Salida:
        - lista (list): Lista de objetos Estacionamiento.
    """
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
        contador += 1
    return lista

def denominarEspacios():
    """
    Funcionalidad:
        Crea la lista de espacios del estacionamiento con su tipo y estado inicial.
    Entrada:
        - None
    Salida:
        - espacios (list): Lista de diccionarios con tipo y estado de cada espacio.
    """
    espacios = []
    for i in range(17):
        espacios.append({"tipo": "normal", "carro": None})
    espacios.append({"tipo": "discapacidad", "carro": None})
    espacios.append({"tipo": "discapacidad", "carro": None})
    espacios.append({"tipo": "electrico", "carro": None})
    return espacios

diccionario = {}
listaObjetos = []
espaciosEstacionamiento = denominarEspacios()
archivoBaseDatos = "baseDatosParqueo.pkl"
carpetaVouchers = "vouchers"
urlApiMockaroo = "https://my.api.mockaroo.com/vehiculos.json?key=5f760930"

def colorEspacio(espacio):
    """
    Funcionalidad:
        Determina el color de fondo de un espacio según su tipo y estado.
    Entrada:
        - espacio (dict): Diccionario con tipo y estado del espacio.
    Salida:
        - color (str): Color hexadecimal correspondiente al estado del espacio.
    """
    if espacio["carro"] is not None:
        return "#F15959"
    elif espacio["tipo"] == "discapacidad":
        return "#597FF1"
    elif espacio["tipo"] == "electrico":
        return "#F1D559"
    else:
        return "#6FB95D"

def observarEspacio(diccionario, espacio, ventanaAbierta, numero, espacios):
    """
    Funcionalidad:
        Abre una ventana con la información del espacio seleccionado,
        mostrando datos del vehículo si está ocupado o formulario si está libre.
    Entrada:
        - diccionario (dict): Diccionario de vehículos cargados.
        - espacio (dict): Diccionario con tipo y estado del espacio.
        - ventanaAbierta (list): Lista de un elemento que referencia la ventana abierta.
        - numero (int): Número del espacio seleccionado.
        - espacios (list): Lista completa de espacios del estacionamiento.
    Salida:
        - None
    """
    if ventanaAbierta[0] is not None:
        ventanaAbierta[0].destroy()
    app = tk.Toplevel()
    ventanaAbierta[0] = app
    app.title("Información del vehículo")
    app.geometry("450x250")
    if espacio["carro"] is not None:
        app.config(bg="#F15959")
        app.resizable(False, False)
        placa = espacio["carro"]
        tk.Label(app, text="#Campo").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=numero).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Placa").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=espacio["carro"]).grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Marca").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=diccionario[placa][0]).grid(row=2, column=1, sticky="w", padx=5, pady=5)
        tk.Label(app, text="Color").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=diccionario[placa][1]).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        tk.Label(app, text="Hora de entrada").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        tk.Label(app, text=diccionario[placa][4]).grid(row=4, column=1, sticky="w", padx=5, pady=5)
        frameBotones = tk.Frame(app, bg="#F15959")
        frameBotones.grid(row=0, column=2, rowspan=5, padx=20, pady=20, sticky="ns")
        tk.Button(frameBotones, text="Pagar", bg="#0d7703", fg="white", font=("SansSerif", 10, "bold"), padx=15, pady=10).pack(pady=5)
        tk.Button(frameBotones, text="Regresar", command=lambda: regresar(app), bg="#770303", fg="white", font=("SansSerif", 10), padx=15, pady=10).pack(pady=5)
    elif espacio["tipo"] == "discapacidad":
        app.config(bg="#597FF1")
        tk.Label(app, text="Espacio especial disponible", bg="#597FF1", fg="white", font=("SansSerif", 12, "bold")).pack(pady=40)
        tk.Button(app, text="Regresar", command=lambda: regresar(app), bg="#770303", fg="white", font=("SansSerif", 10), padx=15, pady=10).pack()
    elif espacio["tipo"] == "electrico":
        app.config(bg="#F1D559")
        tk.Label(app, text="Espacio eléctrico disponible", bg="#F1D559", fg="black", font=("SansSerif", 12, "bold")).pack(pady=40)
        tk.Button(app, text="Regresar", command=lambda: regresar(app), bg="#770303", fg="white", font=("SansSerif", 10), padx=15, pady=10).pack()
    else:
        app.config(bg="#6FB95D")
        app.resizable(False, False)
        horaEntrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        camposDisponibles = []
        for i, esp in enumerate(espacios):
            if esp["carro"] is None:
                camposDisponibles.append(i + 1)
        tk.Label(app, text="#Campo").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        entryCampo = tk.StringVar()
        tk.OptionMenu(app, entryCampo, *camposDisponibles).grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Placa").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        entryPlaca = tk.Entry(app)
        entryPlaca.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Marca").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        entryMarca = tk.StringVar()
        tk.OptionMenu(app, entryMarca, *marcas).grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Color").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        entryColor = tk.StringVar()
        tk.OptionMenu(app, entryColor, *colores).grid(row=3, column=1, sticky="ew", padx=5, pady=5)
        tk.Label(app, text="Hora de entrada").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        entryHora = tk.Entry(app)
        entryHora.insert(0, horaEntrada)
        entryHora.config(state="readonly")
        entryHora.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
        frameBotones = tk.Frame(app, bg="#6FB95D")
        frameBotones.grid(row=0, column=2, rowspan=5, padx=20, pady=20, sticky="ns")
        tk.Button(frameBotones, text="Estacionar", bg="#0d7703", fg="white", font=("SansSerif", 10, "bold"), padx=15, pady=10).pack(pady=5)
        tk.Button(frameBotones, text="Regresar", command=lambda: regresar(app), bg="#770303", fg="white", font=("SansSerif", 10), padx=15, pady=10).pack(pady=5)

def estacionamientoVentana(diccionario, espaciosEstacionamiento):
    """
    Funcionalidad:
        Abre la ventana gráfica del estacionamiento con todos sus espacios.
    Entrada:
        - diccionario (dict): Diccionario de vehículos cargados.
        - espaciosEstacionamiento (list): Lista de espacios del estacionamiento.
    Salida:
        - None
    """
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
        boton = tk.Button(app, text=f"#{i+1}", bg=colorEspacio(espacios[i]), command=lambda n=i: observarEspacio(diccionario, espacios[n], ventanaAbierta, n + 1, espacios), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=1, column=i+1, padx=5, pady=5)
        botones[i] = boton
    tk.Label(app, text="- - " * 20, bg="#2D2F33", fg="#EED42B", font=("arial", 18, "bold")).grid(row=2, column=1, columnspan=9, pady=5)
    for i in range(9, 17):
        boton = tk.Button(app, text=f"#{i+1}", bg=colorEspacio(espacios[i]), command=lambda n=i: observarEspacio(diccionario, espacios[n], ventanaAbierta, n + 1, espacios), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=3, column=i-8, padx=5, pady=5)
        botones[i] = boton
    especiales = [17, 18, 19]
    for num, valor in enumerate(especiales):
        boton = tk.Button(app, text=f"#{valor+1}", bg=colorEspacio(espacios[valor]), command=lambda n=valor: observarEspacio(diccionario, espacios[n], ventanaAbierta, n + 1, espacios), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=num+1, column=11, padx=5, pady=5)
        botones[valor] = boton
        

def alClickCierreDiario():
    """
    Funcionalidad:
        Placeholder para ejecutar el cierre diario y generar su reporte.
    Entrada:
        - None
    Salida:
        - None
    """
    print("Cierre diario")

def alClickCierrePorTipoPago():
    """
    Funcionalidad:
        Placeholder para generar el cierre agrupado por tipo de pago en XML.
    Entrada:
        - None
    Salida:
        - None
    """
    print("Cierre por tipo de pago")

def alClickExportarCSV():
    """
    Funcionalidad:
        Placeholder para exportar el cierre diario a un archivo CSV.
    Entrada:
        - None
    Salida:
        - None
    """
    print("Exportar cierre diario a CSV")

def alClickTamanioEstacionamiento():
    """
    Funcionalidad:
        Placeholder para configurar el tamaño del estacionamiento.
    Entrada:
        - None
    Salida:
        - None
    """
    print("Tamaño del estacionamiento")

def alClickTiempoDeGracia():
    """
    Funcionalidad:
        Placeholder para configurar el tiempo de gracia en minutos.
    Entrada:
        - None
    Salida:
        - None
    """
    print("Tiempo de gracia en minutos")

def alClickModificarMontoPorHora():
    """
    Funcionalidad:
        Placeholder para modificar el monto cobrado por hora.
    Entrada:
        - None
    Salida:
        - None
    """
    print("Modificar monto por hora")

def alClickAcercaDe():
    """
    Funcionalidad:
        Placeholder para abrir la ventana de información del equipo desarrollador.
    Entrada:
        - None
    Salida:
        - None
    """
    print("Acerca de")

def construirVentanaPrincipal():
    """
    Funcionalidad:
        Inicializa y construye la ventana principal del sistema de parqueo
        con todos sus botones organizados según la especificación del enunciado.
    Entrada:
        - None
    Salida:
        - None
    """
    app = tk.Tk()
    app.title("Sistema de Parqueo")
    app.geometry("400x600")
    app.resizable(False, False)
    app.config(bg="#2D2F33")
    tk.Label(app, text="Sistema de Parqueo", bg="#2D2F33", fg="White", font=("SansSerif", 16, "bold")).pack(pady=15)
    tk.Label(app, text="1. Vehículos", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack()
    tk.Button(app, text="Obtener vehículos", bg="#8B1475", fg="white", font=("SansSerif", 10, "bold"), width=28, pady=8, relief="flat", command=lambda: alClickObtenerVehiculos(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo)).pack(pady=4)
    tk.Button(app, text="Ver estacionamiento", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: estacionamientoVentana(diccionario, espaciosEstacionamiento)).pack(pady=2)
    tk.Label(app, text="3. Reportes", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack(pady=(10, 0))
    tk.Button(app, text="a. Cierre diario", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=alClickCierreDiario).pack(pady=2)
    tk.Button(app, text="b. Cierre por tipo de pago", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=alClickCierrePorTipoPago).pack(pady=2)
    tk.Button(app, text="c. Exportar cierre diario a CSV", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=alClickExportarCSV).pack(pady=2)
    tk.Label(app, text="4. Configuración", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack(pady=(10, 0))
    tk.Button(app, text="a. Tamaño del estacionamiento", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=alClickTamanioEstacionamiento).pack(pady=2)
    tk.Button(app, text="b. Tiempo de gracia en minutos", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=alClickTiempoDeGracia).pack(pady=2)
    tk.Button(app, text="c. Modificar monto por hora", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=alClickModificarMontoPorHora).pack(pady=2)
    tk.Label(app, text="5. Acerca de", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack(pady=(10, 0))
    tk.Button(app, text="Acerca de", bg="#8B1475", fg="white", font=("SansSerif", 10, "bold"), width=28, pady=8, relief="flat", command=alClickAcercaDe).pack(pady=4)
    app.mainloop()



def redondearHaciaArriba(numero):
    """
    Funcionalidad:
        Redondea un número decimal hacia arriba.
    Entrada:
        - numero (float): Número que se desea redondear.
    Salida:
        - resultado (int): Número entero redondeado hacia arriba.
    """
    entero = int(numero)
    if numero > entero:
        return entero + 1
    return entero


def calcularCantidadEspeciales(tamanioEstacionamiento):
    """
    Funcionalidad:
        Calcula la cantidad de espacios especiales que debe tener el parqueo.
    Entrada:
        - tamanioEstacionamiento (int): Cantidad total de espacios.
    Salida:
        - cantidadEspeciales (int): Cantidad de espacios especiales.
    """
    cantidadEspeciales = redondearHaciaArriba(tamanioEstacionamiento * 0.05)
    if cantidadEspeciales < 2:
        cantidadEspeciales = 2
    if cantidadEspeciales > tamanioEstacionamiento:
        cantidadEspeciales = tamanioEstacionamiento
    return cantidadEspeciales


def existeEspacioElectrico(espacios):
    """
    Funcionalidad:
        Verifica si existe al menos un espacio eléctrico en el estacionamiento.
    Entrada:
        - espacios (list): Lista de espacios del estacionamiento.
    Salida:
        - existe (bool): True si existe espacio eléctrico, False si no existe.
    """
    for espacio in espacios:
        if espacio["tipo"] == "electrico":
            return True
    return False


def calcularTopeMasivo(tamanioEstacionamiento, tieneElectrico):
    """
    Funcionalidad:
        Calcula la cantidad máxima de vehículos que se pueden cargar masivamente.
    Entrada:
        - tamanioEstacionamiento (int): Cantidad total de espacios.
        - tieneElectrico (bool): Indica si el parqueo tiene espacio eléctrico.
    Salida:
        - topeMasivo (int): Cantidad máxima para carga masiva.
    """
    cantidadEspeciales = calcularCantidadEspeciales(tamanioEstacionamiento)
    cantidadElectricos = 0
    if tieneElectrico:
        cantidadElectricos = 1
    cantidadGeneral = tamanioEstacionamiento - cantidadEspeciales - cantidadElectricos
    if cantidadGeneral <= 0:
        return 0
    cantidadLibreClientes = redondearHaciaArriba(cantidadGeneral * 0.05)
    topeMasivo = cantidadGeneral - cantidadLibreClientes
    if topeMasivo < 0:
        topeMasivo = 0
    return topeMasivo


def obtenerUbicacionesGeneralesLibres(espacios):
    """
    Funcionalidad:
        Obtiene las ubicaciones generales libres del estacionamiento.
    Entrada:
        - espacios (list): Lista de espacios del estacionamiento.
    Salida:
        - ubicacionesLibres (list): Lista con números de espacios generales libres.
    """
    ubicacionesLibres = []
    contador = 0
    for espacio in espacios:
        contador += 1
        if espacio["tipo"] == "normal" and espacio["carro"] is None:
            ubicacionesLibres.append(contador)
    return ubicacionesLibres


def crearFechaHoraEntradaAleatoria():
    """
    Funcionalidad:
        Genera una fecha y hora de entrada aleatoria entre las 7:00 a.m.
        y la hora actual del sistema.
    Entrada:
        - None
    Salida:
        - fechaHoraEntrada (str): Fecha y hora generada.
    """
    horaActual = datetime.now()
    horaApertura = horaActual.replace(hour=7, minute=0, second=0, microsecond=0)
    if horaActual < horaApertura:
        return horaActual.strftime("%Y-%m-%d %H:%M:%S")
    segundosMaximos = int((horaActual - horaApertura).total_seconds())
    if segundosMaximos <= 0:
        return horaActual.strftime("%Y-%m-%d %H:%M:%S")
    segundosAleatorios = random.randint(0, segundosMaximos)
    fechaHoraEntrada = horaApertura + timedelta(seconds=segundosAleatorios)
    return fechaHoraEntrada.strftime("%Y-%m-%d %H:%M:%S")

def obtenerDatoCarro(carro, llave, valorDefecto):
    """
    Funcionalidad:
        Obtiene un dato específico de un carro recibido desde JSON.
    Entrada:
        - carro (dict): Diccionario con datos del carro.
        - llave (str): Llave que se desea buscar.
        - valorDefecto (str): Valor usado si la llave no existe.
    Salida:
        - valor (str): Dato encontrado o valor por defecto.
    """
    if llave in carro:
        if carro[llave] is not None:
            if str(carro[llave]).strip() != "":
                return str(carro[llave])
    return valorDefecto


def crearPlacaUnica(diccionario, diccionarioTemporal):
    """
    Funcionalidad:
        Crea una placa que no exista en el diccionario global ni en el temporal.
    Entrada:
        - diccionarioTemporal (dict): Diccionario creado durante la carga actual.
    Salida:
        - placa (str): Placa única.
    """
    placa = crearPlaca()
    placaRepetida = True
    while placaRepetida:
        placaRepetida = False
        if placa in diccionario:
            placaRepetida = True
        if placa in diccionarioTemporal:
            placaRepetida = True
        if placaRepetida:
            placa = crearPlaca()
    return placa


def obtenerDatosVehiculos(cantidadVehiculos, urlApiMockaroo):
    """
    Funcionalidad:
        Obtiene datos de vehículos desde la API interna del sistema.
    Entrada:
        - cantidadVehiculos (int): Cantidad de vehículos solicitados.
        - urlApiMockaroo (str): Dirección interna del servicio de vehículos.
    Salida:
        - datosVehiculos (list): Lista de diccionarios con datos de vehículos.
    """
    separador = "?"
    if "?" in urlApiMockaroo:
        separador = "&"
    urlCompleta = urlApiMockaroo + separador + "count=" + str(cantidadVehiculos)
    respuesta = urllib.request.urlopen(urlCompleta, timeout=15)
    contenido = respuesta.read().decode("utf-8")
    datosVehiculos = json.loads(contenido)
    if isinstance(datosVehiculos, dict):
        datosConvertidos = []
        datosConvertidos.append(datosVehiculos)
        datosVehiculos = datosConvertidos
    if not isinstance(datosVehiculos, list):
        raise ValueError()
    return datosVehiculos


def crearDiccionarioVehiculos(diccionario, datosVehiculos, ubicacionesLibres, cantidadVehiculos):
    """
    Funcionalidad:
        Construye el diccionario de vehículos solicitado por el enunciado.
    Entrada:
        - datosVehiculos (list): Datos recibidos desde JSON.
        - ubicacionesLibres (list): Espacios generales libres.
        - cantidadVehiculos (int): Cantidad máxima a registrar.
    Salida:
        - diccionarioVehiculos (dict): Diccionario con placa como llave.
    """
    diccionarioVehiculos = {}
    contador = 0
    for carro in datosVehiculos:
        if contador < cantidadVehiculos:
            if contador < len(ubicacionesLibres):
                placa = crearPlacaUnica(diccionario, diccionarioVehiculos)
                marca = obtenerDatoCarro(carro, "Marca", "Toyota")
                color = obtenerDatoCarro(carro, "Color", "Azul")
                tipo = obtenerDatoCarro(carro, "Tipo", "Automovil")
                ubicacion = str(ubicacionesLibres[contador])
                fechaHoraEntrada = crearFechaHoraEntradaAleatoria()
                fechaHoraSalida = ""
                monto = 0
                tipoPago = 0
                diccionarioVehiculos[placa] = [
                    marca,
                    color,
                    tipo,
                    ubicacion,
                    fechaHoraEntrada,
                    fechaHoraSalida,
                    monto,
                    tipoPago
                ]

                contador += 1
    return diccionarioVehiculos

def agregarDiccionarioGlobal(diccionario, diccionarioVehiculos):
    """
    Funcionalidad:
        Agrega los vehículos cargados al diccionario global del sistema.
    Entrada:
        - diccionarioVehiculos (dict): Diccionario de vehículos nuevos.
    Salida:
        - None
    """
    for placa, datos in diccionarioVehiculos.items():
        diccionario[placa] = datos


def agregarObjetosEstacionamiento(listaObjetos, diccionarioVehiculos):
    """
    Funcionalidad:
        Convierte los vehículos del diccionario en objetos Estacionamiento
        y los agrega a la lista oficial de objetos.
    Entrada:
        - diccionarioVehiculos (dict): Diccionario de vehículos nuevos.
    Salida:
        - None
    """
    contador = len(listaObjetos) + 1
    for placa, datos in diccionarioVehiculos.items():
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
        listaObjetos.append(objeto)
        contador += 1

def ocuparEspaciosMasivos(diccionarioVehiculos, espacios):
    """
    Funcionalidad:
        Marca como ocupados los espacios generales asignados en la carga masiva.
    Entrada:
        - diccionarioVehiculos (dict): Diccionario de vehículos cargados.
        - espacios (list): Lista de espacios del estacionamiento.
    Salida:
        - None
    """
    for placa, datos in diccionarioVehiculos.items():
        ubicacion = int(datos[3])
        indice = ubicacion - 1
        if indice >= 0 and indice < len(espacios):
            espacios[indice]["carro"] = placa

def guardarBaseDatos(listaObjetos, archivoBaseDatos):
    """
    Funcionalidad:
        Guarda la lista oficial de objetos en memoria secundaria.
    Entrada:
        - None
    Salida:
        - None
    """
    with open(archivoBaseDatos, "wb") as archivo:
        pickle.dump(listaObjetos, archivo)

def crearCarpetaSiNoExiste(nombreCarpeta):
    """
    Funcionalidad:
        Crea una carpeta si todavía no existe.
    Entrada:
        - nombreCarpeta (str): Nombre de la carpeta.
    Salida:
        - None
    """
    if not os.path.exists(nombreCarpeta):
        os.makedirs(nombreCarpeta)

def limpiarNombreArchivo(texto):
    """
    Funcionalidad:
        Limpia caracteres inválidos para nombres de archivo.
    Entrada:
        - texto (str): Texto original.
    Salida:
        - textoLimpio (str): Texto seguro para nombre de archivo.
    """
    textoLimpio = str(texto)
    caracteresInvalidos = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
    for caracter in caracteresInvalidos:
        textoLimpio = textoLimpio.replace(caracter, "-")
    return textoLimpio

def crearTextoQrVoucher(objeto):
    """
    Funcionalidad:
        Crea el texto que va dentro del código QR del voucher.
    Entrada:
        - objeto (Estacionamiento): Objeto del vehículo estacionado.
    Salida:
        - textoQr (str): Información para el código QR.
    """
    placa = objeto.info[0]
    marca = objeto.info[1]
    tipo = objeto.info[3]
    fechaHoraEntrada = objeto.estadia[1]
    textoQr = "Placa: " + str(placa)
    textoQr += "\nMarca: " + str(marca)
    textoQr += "\nTipo: " + str(tipo)
    textoQr += "\nFecha y hora de entrada: " + str(fechaHoraEntrada)
    return textoQr


def crearNombreVoucher(objeto):
    """
    Funcionalidad:
        Crea el nombre del archivo PDF del voucher.
    Entrada:
        - objeto (Estacionamiento): Objeto del vehículo estacionado.
    Salida:
        - nombreArchivo (str): Nombre del voucher.
    """
    placa = objeto.info[0]
    fechaHoraEntrada = objeto.estadia[1]
    try:
        fecha = datetime.strptime(fechaHoraEntrada, "%Y-%m-%d %H:%M:%S")
        fechaTexto = fecha.strftime("%d-%m-%Y_%H-%M")
    except ValueError:
        fechaTexto = limpiarNombreArchivo(fechaHoraEntrada)
    nombreArchivo = "voucher_" + str(placa) + "_" + fechaTexto + ".pdf"
    nombreArchivo = limpiarNombreArchivo(nombreArchivo)
    return nombreArchivo

def crearVoucherPdf(objeto, carpetaVouchers):
    """
    Funcionalidad:
        Crea un voucher PDF con código QR para un vehículo estacionado.
    Entrada:
        - objeto (Estacionamiento): Objeto del vehículo estacionado.
    Salida:
        - rutaPdf (str): Ruta del archivo PDF generado.
    """
    crearCarpetaSiNoExiste(carpetaVouchers)

    placa = objeto.info[0]
    marca = objeto.info[1]
    color = objeto.info[2]
    tipo = objeto.info[3]
    ubicacion = objeto.estadia[0]
    fechaHoraEntrada = objeto.estadia[1]
    nombreArchivo = crearNombreVoucher(objeto)
    rutaPdf = os.path.join(carpetaVouchers, nombreArchivo)
    textoQr = crearTextoQrVoucher(objeto)
    imagenQr = qrcode.make(textoQr)
    nombreQr = "qr_" + limpiarNombreArchivo(str(placa)) + ".png"
    rutaQr = os.path.join(carpetaVouchers, nombreQr)
    imagenQr.save(rutaQr)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Voucher de Estacionamiento", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "Placa: " + str(placa), ln=True)
    pdf.cell(0, 8, "Marca: " + str(marca), ln=True)
    pdf.cell(0, 8, "Color: " + str(color), ln=True)
    pdf.cell(0, 8, "Tipo: " + str(tipo), ln=True)
    pdf.cell(0, 8, "Ubicacion: " + str(ubicacion), ln=True)
    pdf.cell(0, 8, "Fecha y hora de entrada: " + str(fechaHoraEntrada), ln=True)
    pdf.ln(10)
    pdf.cell(0, 8, "Codigo QR:", ln=True)
    pdf.image(rutaQr, x=80, y=100, w=50, h=50)
    pdf.output(rutaPdf)
    try:
        os.remove(rutaQr)
    except OSError:
        pass
    return rutaPdf


def crearVouchersMasivos(diccionarioVehiculos, listaObjetos, carpetaVouchers):
    """
    Funcionalidad:
        Crea los vouchers PDF de todos los vehículos cargados masivamente.
    Entrada:
        - diccionarioVehiculos (dict): Diccionario de vehículos cargados.
    Salida:
        - cantidadVouchers (int): Cantidad de vouchers generados.
    """
    cantidadVouchers = 0
    for objeto in listaObjetos:
        placaObjeto = objeto.info[0]
        if placaObjeto in diccionarioVehiculos:
            crearVoucherPdf(objeto, carpetaVouchers)
            cantidadVouchers += 1
    return cantidadVouchers

def imprimirDiccionarioVehiculos(diccionarioVehiculos):
    """
    Funcionalidad:
        Imprime el diccionario de vehículos.
    Entrada:
        - diccionarioVehiculos (dict): Diccionario de vehículos cargados.
    Salida:
        - None
    """
    print("- DICCIONARIO DE VEHICULOS CARGADOS -")
    print(json.dumps(diccionarioVehiculos, indent=4, ensure_ascii=False))
    print("---------------------")

def alClickObtenerVehiculos(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo):
    """
    Funcionalidad:
        Ejecuta la carga masiva de vehículos, crea objetos, guarda la base de datos
        y genera vouchers PDF con QR.
    Entrada:
        - None
    Salida:
        - None
    """
    try:
        tamanioEstacionamiento = len(espaciosEstacionamiento)
        tieneElectrico = existeEspacioElectrico(espaciosEstacionamiento)
        topeMasivo = calcularTopeMasivo(tamanioEstacionamiento, tieneElectrico)
        ubicacionesLibres = obtenerUbicacionesGeneralesLibres(espaciosEstacionamiento)
        cantidadVehiculos = topeMasivo
        if cantidadVehiculos > len(ubicacionesLibres):
            cantidadVehiculos = len(ubicacionesLibres)

        if cantidadVehiculos <= 0:
            messagebox.showwarning(
                "Obtener vehículos",
                "No hay espacios generales disponibles para carga masiva."
            )
            return
        confirmar = messagebox.askyesno(
            "Obtener vehiculos",
            "Se cargarán " + str(cantidadVehiculos) + " vehículos generales.\n\nDesea continuar?"
        )
        if not confirmar:
            return
        datosVehiculos = obtenerDatosVehiculos(cantidadVehiculos, urlApiMockaroo)
        diccionarioVehiculos = crearDiccionarioVehiculos(
            diccionario,
            datosVehiculos,
            ubicacionesLibres,
            cantidadVehiculos
            )
        if len(diccionarioVehiculos) == 0:
            messagebox.showwarning(
                "Obtener vehiculos",
                "No se pudieron generar vehiculos."
            )
            return
        imprimirDiccionarioVehiculos(diccionarioVehiculos)
        agregarDiccionarioGlobal(diccionario, diccionarioVehiculos)
        agregarObjetosEstacionamiento(listaObjetos, diccionarioVehiculos)
        ocuparEspaciosMasivos(diccionarioVehiculos, espaciosEstacionamiento)
        guardarBaseDatos(listaObjetos, archivoBaseDatos)
        cantidadVouchers = crearVouchersMasivos(diccionarioVehiculos, listaObjetos, carpetaVouchers)
        messagebox.showinfo(
            "Obtener vehiculos",
            "Carga masiva finalizada.\n\nVehiculos cargados: "
            + str(len(diccionarioVehiculos))
            + "\nVouchers generados: "
            + str(cantidadVouchers)
        )
    except ValueError:
        messagebox.showerror("Error", "No se pudo obtener la información de vehículos.")
    except Exception:
        messagebox.showerror("Error", "No se pudo completar la carga masiva.")

if __name__ == "__main__":
    construirVentanaPrincipal()

