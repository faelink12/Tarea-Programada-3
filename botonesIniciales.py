import tkinter as tk

colorFondo = "#1E1E2E"
colorPanel = "#2A2A3E"
colorTexto = "#FFFFFF"
colorSubtexto = "#A0A0C0"
colorBotonPrincipal = "#4A90D9"
colorBotonPrincipalHover = "#357ABD"
colorBotonSub = "#3A3A5E"
colorBotonSubHover = "#4A4A7E"

fuenteTitulo = ("Segoe UI", 20, "bold")
fuenteSubtitulo = ("Segoe UI", 10)
fuenteBotonPrincipal = ("Segoe UI", 11, "bold")
fuenteBotonSub = ("Segoe UI", 10)
fuenteSeccion = ("Segoe UI", 9, "italic")

anchoBotonPrincipal = 32
anchoBotonSub = 30
paddingVerticalPrincipal = 10
paddingVerticalSub = 6


def crearBoton(contenedor, textoBoton, colorFondoBoton, colorHover,
               comandoBoton, anchoBoton, fuenteBoton, paddingVertical):
    """
    Funcionalidad:
        Crea un botón estilizado con efecto hover para la ventana principal.
    Entrada:
        - contenedor (tk.Widget): Widget padre donde se coloca el botón.
        - textoBoton (str): Texto visible en el botón.
        - colorFondoBoton (str): Color de fondo normal del botón.
        - colorHover (str): Color de fondo al pasar el mouse.
        - comandoBoton (callable): Función ejecutada al hacer clic.
        - anchoBoton (int): Ancho del botón en caracteres.
        - fuenteBoton (tuple): Configuración de fuente.
        - paddingVertical (int): Espacio vertical interno del botón.
    Salida:
        - boton (tk.Button): El botón creado y configurado.
    """
    boton = tk.Button(
        contenedor,
        text=textoBoton,
        font=fuenteBoton,
        bg=colorFondoBoton,
        fg=colorTexto,
        activebackground=colorHover,
        activeforeground=colorTexto,
        relief="flat",
        bd=0,
        width=anchoBoton,
        pady=paddingVertical,
        cursor="hand2",
        command=comandoBoton
    )

    def alEntrarMouse(evento):
        boton.config(bg=colorHover)

    def alSalirMouse(evento):
        boton.config(bg=colorFondoBoton)

    boton.bind("<Enter>", alEntrarMouse)
    boton.bind("<Leave>", alSalirMouse)
    return boton


def crearEtiquetaSeccion(contenedor, textoSeccion):
    """
    Funcionalidad:
        Crea una etiqueta de sección para agrupar botones visualmente.
    Entrada:
        - contenedor (tk.Widget): Widget padre donde se coloca la etiqueta.
        - textoSeccion (str): Texto descriptivo de la sección.
    Salida:
        - None
    """
    tk.Label(
        contenedor,
        text=textoSeccion,
        font=fuenteSeccion,
        bg=colorFondo,
        fg=colorSubtexto
    ).pack(pady=(10, 2))


def alClickObtenerVehiculos():
    """
    Funcionalidad:
        Placeholder para ejecutar la obtención masiva de vehículos desde la API.
    Entrada:
        - None
    Salida:
        - None
    """
    print(">> Obtener vehículos")


def alClickObservarEspacio():
    """
    Funcionalidad:
        Placeholder para abrir la vista de observación de un espacio.
    Entrada:
        - None
    Salida:
        - None
    """
    print(">> Observar espacio")


def alClickEstacionarVehiculo():
    """
    Funcionalidad:
        Placeholder para abrir el formulario de estacionamiento de un vehículo.
    Entrada:
        - None
    Salida:
        - None
    """
    print(">> Estacionar un vehículo")


def alClickCierreDiario():
    """
    Funcionalidad:
        Placeholder para ejecutar el cierre diario y generar su reporte.
    Entrada:
        - None
    Salida:
        - None
    """
    print(">> Cierre diario")


def alClickCierrePorTipoPago():
    """
    Funcionalidad:
        Placeholder para generar el cierre agrupado por tipo de pago en XML.
    Entrada:
        - None
    Salida:
        - None
    """
    print(">> Cierre por tipo de pago")


def alClickExportarCSV():
    """
    Funcionalidad:
        Placeholder para exportar el cierre diario a un archivo CSV.
    Entrada:
        - None
    Salida:
        - None
    """
    print(">> Exportar cierre diario a CSV")


def alClickTamanioEstacionamiento():
    """
    Funcionalidad:
        Placeholder para configurar el tamaño del estacionamiento.
    Entrada:
        - None
    Salida:
        - None
    """
    print(">> Tamaño del estacionamiento")


def alClickTiempoDeGracia():
    """
    Funcionalidad:
        Placeholder para configurar el tiempo de gracia en minutos.
    Entrada:
        - None
    Salida:
        - None
    """
    print(">> Tiempo de gracia en minutos")


def alClickModificarMontoPorHora():
    """
    Funcionalidad:
        Placeholder para modificar el monto cobrado por hora.
    Entrada:
        - None
    Salida:
        - None
    """
    print(">> Modificar monto por hora")


def alClickAcercaDe():
    """
    Funcionalidad:
        Placeholder para abrir la ventana de información del equipo desarrollador.
    Entrada:
        - None
    Salida:
        - None
    """
    print(">> Acerca de")


def construirEncabezado(contenedor):
    """
    Funcionalidad:
        Construye el encabezado visual de la ventana principal.
    Entrada:
        - contenedor (tk.Widget): Widget padre donde se coloca el encabezado.
    Salida:
        - None
    """
    marcoEncabezado = tk.Frame(contenedor, bg=colorPanel, pady=18)
    marcoEncabezado.pack(fill="x")
    tk.Label(
        marcoEncabezado,
        text="Sistema de Parqueo",
        font=fuenteTitulo,
        bg=colorPanel,
        fg=colorTexto
    ).pack()
    tk.Label(
        marcoEncabezado,
        text="Gestión de estacionamiento",
        font=fuenteSubtitulo,
        bg=colorPanel,
        fg=colorSubtexto
    ).pack(pady=(4, 0))


def construirBotonObtenerVehiculos(contenedor):
    """
    Funcionalidad:
        Construye y coloca el botón principal de obtener vehículos.
    Entrada:
        - contenedor (tk.Widget): Widget padre donde se coloca el botón.
    Salida:
        - None
    """
    crearEtiquetaSeccion(contenedor, "1. Vehículos")
    botonObtenerVehiculos = crearBoton(
        contenedor,
        "Obtener vehículos",
        colorBotonPrincipal,
        colorBotonPrincipalHover,
        alClickObtenerVehiculos,
        anchoBotonPrincipal,
        fuenteBotonPrincipal,
        paddingVerticalPrincipal
    )
    botonObtenerVehiculos.pack(pady=(2, 0))


def construirBotonesVerEstacionamiento(contenedor):
    """
    Funcionalidad:
        Construye y coloca los botones de la sección Ver Estacionamiento
        con sus dos sub-opciones: Observar espacio y Estacionar un vehículo.
    Entrada:
        - contenedor (tk.Widget): Widget padre donde se colocan los botones.
    Salida:
        - None
    """
    crearEtiquetaSeccion(contenedor, "2. Ver estacionamiento")
    botonObservarEspacio = crearBoton(
        contenedor,
        "a. Observar espacio",
        colorBotonSub,
        colorBotonSubHover,
        alClickObservarEspacio,
        anchoBotonSub,
        fuenteBotonSub,
        paddingVerticalSub
    )
    botonObservarEspacio.pack(pady=(2, 2))
    botonEstacionarVehiculo = crearBoton(
        contenedor,
        "b. Estacionar un vehículo",
        colorBotonSub,
        colorBotonSubHover,
        alClickEstacionarVehiculo,
        anchoBotonSub,
        fuenteBotonSub,
        paddingVerticalSub
    )
    botonEstacionarVehiculo.pack(pady=(0, 0))


def construirBotonesReportes(contenedor):
    """
    Funcionalidad:
        Construye y coloca los botones de la sección Reportes
        con sus tres sub-opciones.
    Entrada:
        - contenedor (tk.Widget): Widget padre donde se colocan los botones.
    Salida:
        - None
    """
    crearEtiquetaSeccion(contenedor, "3. Reportes")
    botonCierreDiario = crearBoton(
        contenedor,
        "a. Cierre diario",
        colorBotonSub,
        colorBotonSubHover,
        alClickCierreDiario,
        anchoBotonSub,
        fuenteBotonSub,
        paddingVerticalSub
    )
    botonCierreDiario.pack(pady=(2, 2))
    botonCierrePorTipoPago = crearBoton(
        contenedor,
        "b. Cierre por tipo de pago",
        colorBotonSub,
        colorBotonSubHover,
        alClickCierrePorTipoPago,
        anchoBotonSub,
        fuenteBotonSub,
        paddingVerticalSub
    )
    botonCierrePorTipoPago.pack(pady=(0, 2))
    botonExportarCSV = crearBoton(
        contenedor,
        "c. Exportar cierre diario a CSV",
        colorBotonSub,
        colorBotonSubHover,
        alClickExportarCSV,
        anchoBotonSub,
        fuenteBotonSub,
        paddingVerticalSub
    )
    botonExportarCSV.pack(pady=(0, 0))


def construirBotonesConfiguracion(contenedor):
    """
    Funcionalidad:
        Construye y coloca los botones de la sección Configuración
        con sus tres sub-opciones.
    Entrada:
        - contenedor (tk.Widget): Widget padre donde se colocan los botones.
    Salida:
        - None
    """
    crearEtiquetaSeccion(contenedor, "4. Configuración")
    botonTamanio = crearBoton(
        contenedor,
        "a. Tamaño del estacionamiento",
        colorBotonSub,
        colorBotonSubHover,
        alClickTamanioEstacionamiento,
        anchoBotonSub,
        fuenteBotonSub,
        paddingVerticalSub
    )
    botonTamanio.pack(pady=(2, 2))
    botonTiempoGracia = crearBoton(
        contenedor,
        "b. Tiempo de gracia en minutos",
        colorBotonSub,
        colorBotonSubHover,
        alClickTiempoDeGracia,
        anchoBotonSub,
        fuenteBotonSub,
        paddingVerticalSub
    )
    botonTiempoGracia.pack(pady=(0, 2))
    botonMontoPorHora = crearBoton(
        contenedor,
        "c. Modificar monto por hora",
        colorBotonSub,
        colorBotonSubHover,
        alClickModificarMontoPorHora,
        anchoBotonSub,
        fuenteBotonSub,
        paddingVerticalSub
    )
    botonMontoPorHora.pack(pady=(0, 0))


def construirBotonAcercaDe(contenedor):
    """
    Funcionalidad:
        Construye y coloca el botón de Acerca de al final del menú.
    Entrada:
        - contenedor (tk.Widget): Widget padre donde se coloca el botón.
    Salida:
        - None
    """
    crearEtiquetaSeccion(contenedor, "5. Acerca de")
    botonAcercaDe = crearBoton(
        contenedor,
        "Acerca de",
        colorBotonPrincipal,
        colorBotonPrincipalHover,
        alClickAcercaDe,
        anchoBotonPrincipal,
        fuenteBotonPrincipal,
        paddingVerticalPrincipal
    )
    botonAcercaDe.pack(pady=(2, 16))


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
    ventanaPrincipal = tk.Tk()
    ventanaPrincipal.title("Sistema de Parqueo")
    ventanaPrincipal.configure(bg=colorFondo)
    ventanaPrincipal.resizable(False, False)
    anchoVentana = 420
    altoVentana = 680
    anchoPantalla = ventanaPrincipal.winfo_screenwidth()
    altoPantalla = ventanaPrincipal.winfo_screenheight()
    posicionX = (anchoPantalla // 2) - (anchoVentana // 2)
    posicionY = (altoPantalla // 2) - (altoVentana // 2)
    ventanaPrincipal.geometry(str(anchoVentana) + "x" + str(altoVentana) + "+" + str(posicionX) + "+" + str(posicionY))
    construirEncabezado(ventanaPrincipal)
    marcoCuerpo = tk.Frame(ventanaPrincipal, bg=colorFondo)
    marcoCuerpo.pack(fill="both", expand=True, padx=20)
    construirBotonObtenerVehiculos(marcoCuerpo)
    construirBotonesVerEstacionamiento(marcoCuerpo)
    construirBotonesReportes(marcoCuerpo)
    construirBotonesConfiguracion(marcoCuerpo)
    construirBotonAcercaDe(marcoCuerpo)
    ventanaPrincipal.mainloop()


if __name__ == "__main__":
    construirVentanaPrincipal()