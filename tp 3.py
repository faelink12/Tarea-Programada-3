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

diccionario = crearDiccionarioJSON()
listaObjetos = crearListaDiccionario(diccionario)

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

def observarEspacio(espacio, ventanaAbierta, numero, espacios):
    """
    Funcionalidad:
        Abre una ventana con la información del espacio seleccionado,
        mostrando datos del vehículo si está ocupado o formulario si está libre.
    Entrada:
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
    elif espacio["tipo"] == "electrico":
        app.config(bg="#F1D559")
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

def estacionamientoVentana():
    """
    Funcionalidad:
        Abre la ventana gráfica del estacionamiento con todos sus espacios.
    Entrada:
        - None
    Salida:
        - None
    """
    app = tk.Toplevel()
    app.title("Estacionamiento")
    app.geometry("750x350")
    app.resizable(False, False)
    app.config(bg="#2D2F33")
    espacios = denominarEspacios()
    botones = [None] * 20
    ventanaAbierta = [None]
    tk.Label(app, text="Estacionamiento", bg="#2D2F33", fg="White", font=("SansSerif", 16, "bold")).grid(row=0, column=0, columnspan=10, pady=15)
    tk.Button(app, text="Baño", bg="#8B1475", fg="white", width=6, height=2, relief="flat", bd=1).grid(row=1, column=0, padx=5, pady=5)
    tk.Label(app, text="Entrada", bg="#2D2F33", fg="white", font=("SansSerif", 8)).grid(row=2, column=0, padx=5)
    tk.Button(app, text="Casetilla", bg="#8B1475", fg="white", width=6, height=2, relief="flat", bd=1).grid(row=3, column=0, padx=5, pady=5)
    for i in range(9):
        boton = tk.Button(app, text=f"#{i+1}", bg=colorEspacio(espacios[i]), command=lambda n=i: observarEspacio(espacios[n], ventanaAbierta, n + 1, espacios), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=1, column=i+1, padx=5, pady=5)
        botones[i] = boton
    tk.Label(app, text="- - " * 20, bg="#2D2F33", fg="#EED42B", font=("arial", 18, "bold")).grid(row=2, column=1, columnspan=9, pady=5)
    for i in range(9, 17):
        boton = tk.Button(app, text=f"#{i+1}", bg=colorEspacio(espacios[i]), command=lambda n=i: observarEspacio(espacios[n], ventanaAbierta, n + 1, espacios), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=3, column=i-8, padx=5, pady=5)
        botones[i] = boton
    especiales = [17, 18, 19]
    for num, valor in enumerate(especiales):
        boton = tk.Button(app, text=f"#{valor+1}", bg=colorEspacio(espacios[valor]), command=lambda n=valor: observarEspacio(espacios[n], ventanaAbierta, n + 1, espacios), width=6, height=4, relief="flat", bd=1)
        boton.grid(row=num+1, column=11, padx=5, pady=5)
        botones[valor] = boton

def alClickObtenerVehiculos():
    """
    Funcionalidad:
        Placeholder para ejecutar la obtención masiva de vehículos desde la API.
    Entrada:
        - None
    Salida:
        - None
    """
    print("Obtener vehículos")

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
    tk.Button(app, text="Obtener vehículos", bg="#8B1475", fg="white", font=("SansSerif", 10, "bold"), width=28, pady=8, relief="flat", command=alClickObtenerVehiculos).pack(pady=4)
    tk.Label(app, text="2. Ver estacionamiento", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack(pady=(10, 0))
    tk.Button(app, text="a. Observar espacio / Estacionar", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=estacionamientoVentana).pack(pady=2)
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

if __name__ == "__main__":
    construirVentanaPrincipal()