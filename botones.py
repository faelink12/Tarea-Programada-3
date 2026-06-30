import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime
from funciones import *
from reportes import *
from estacionamiento import *

#esta es la ventana inicial de botones
def construirVentanaPrincipal(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo, montoHora, tiempoDeGracia, archivoConfiguracion, carpetaReportes):
    app = tk.Tk()
    app.title("Sistema de Parqueo")
    app.geometry("400x600")
    app.resizable(False, False)
    app.config(bg="#2D2F33")
    tk.Label(app, text="Sistema de Parqueo", bg="#2D2F33", fg="White", font=("SansSerif", 16, "bold")).pack(pady=15)
    tk.Label(app, text="1. Vehículos", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack()
    tk.Button(app, text="Obtener vehículos", bg="#8B1475", fg="white", font=("SansSerif", 10, "bold"), width=28, pady=8, relief="flat", command=lambda: alClickObtenerVehiculos(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo)).pack(pady=4)
    tk.Button(app, text="Ver estacionamiento", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: estacionamientoVentana(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo, montoHora, tiempoDeGracia, marcas, colores, tiposVehiculo, tiposPago)).pack(pady=2)
    tk.Label(app, text="2. Reportes", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack(pady=(10, 0))
    tk.Button(app, text="Cierre diario", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: alClickCierreDiario(listaObjetos, diccionario, espaciosEstacionamiento, archivoBaseDatos, carpetaReportes, carpetaVouchers, montoHora, tiempoDeGracia)).pack(pady=2)
    tk.Button(app, text="Cierre por tipo de pago", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: botonCierreTipoPago(listaObjetos)).pack(pady=2)
    tk.Button(app, text="Exportar cierre diario a CSV", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: alClickExportarCSV(carpetaReportes)).pack(pady=2)
    tk.Label(app, text="3. Configuración", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack(pady=(10, 0))
    tk.Button(app, text="Tamaño del estacionamiento", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: botonTamannoEstacionamiento(espaciosEstacionamiento, archivoConfiguracion)).pack(pady=2)
    tk.Button(app, text="Tiempo de gracia en minutos", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: botonTiempoDeGracia(tiempoDeGracia, archivoConfiguracion)).pack(pady=2)
    tk.Button(app, text="Modificar monto por hora", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: botonModificarMontoHora(montoHora, archivoConfiguracion)).pack(pady=2)
    tk.Label(app, text="4. Acerca de", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack(pady=(10, 0))
    tk.Button(app, text="Acerca de", bg="#8B1475", fg="white", font=("SansSerif", 10, "bold"), width=28, pady=8, relief="flat", command=botonAcercaDe).pack(pady=4)
    app.mainloop()

#esto es para obtener vehículos y vouchers
def alClickObtenerVehiculos(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo):
    try:
        tamannoEstacionamiento = len(espaciosEstacionamiento)
        tieneElectrico = existeEspacioElectrico(espaciosEstacionamiento)
        topeMasivo = calcularTopeMasivo(tamannoEstacionamiento, tieneElectrico)
        ocupadosGenerales = contarEspaciosGeneralesOcupados(espaciosEstacionamiento)
        topeMasivoDisponible = topeMasivo - ocupadosGenerales
        if topeMasivoDisponible < 0:
            topeMasivoDisponible = 0
        ubicacionesLibres = obtenerUbicacionesGeneralesLibres(espaciosEstacionamiento)
        cantidadVehiculos = topeMasivoDisponible
        if cantidadVehiculos > len(ubicacionesLibres):
            cantidadVehiculos = len(ubicacionesLibres)
        if cantidadVehiculos <= 0:
            messagebox.showwarning("Obtener vehículos", "No hay espacios generales disponibles para carga masiva.")
            return
        confirmar = messagebox.askyesno("Obtener vehículos", "Se cargarán " + str(cantidadVehiculos) + " vehículos generales.\n\nDesea continuar?")
        if not confirmar:
            return
        datosVehiculos = obtenerDatosVehiculos(cantidadVehiculos, urlApiMockaroo)
        diccionarioVehiculos = crearDiccionarioVehiculos(diccionario, datosVehiculos, ubicacionesLibres, cantidadVehiculos, marcas, colores, tiposVehiculo)
        if len(diccionarioVehiculos) == 0:
            messagebox.showwarning("Obtener vehículos", "No se pudieron generar vehículos.")
            return
        imprimirDiccionarioVehiculos(diccionarioVehiculos)
        agregarDiccionarioGlobal(diccionario, diccionarioVehiculos)
        agregarObjetosEstacionamiento(listaObjetos, diccionarioVehiculos)
        ocuparEspaciosMasivos(diccionarioVehiculos, espaciosEstacionamiento)
        guardarBaseDatos(listaObjetos, archivoBaseDatos)
        cantidadVouchers = crearVouchersMasivos(diccionarioVehiculos, listaObjetos, carpetaVouchers, marcas, colores, tiposVehiculo)
        messagebox.showinfo("Obtener vehículos", "Carga masiva finalizada.\n\nVehículos cargados: " + str(len(diccionarioVehiculos)) + "\nVouchers generados: " + str(cantidadVouchers))
    except ValueError:
        messagebox.showerror("Error", "No se pudo obtener la información de vehículos.")
    except Exception:
        messagebox.showerror("Error", "No se pudo completar la carga masiva.")

def pedirTiposPagoPendientes(listaObjetos):
    tipoPagoPorPlaca = {}
    for objeto in listaObjetos:
        if objeto.estadia[2] == "":
            placa = objeto.info[0]
            tipoPagoValido = False
            while not tipoPagoValido:
                valor = simpledialog.askstring("Tipo de pago", "Tipo de pago para la placa " + str(placa) + "\n1 = Efectivo\n2 = SINPE\n3 = Tarjeta")
                if valor is None:
                    return None
                valor = valor.strip()
                if valor == "1" or valor == "2" or valor == "3":
                    tipoPagoPorPlaca[placa] = int(valor)
                    tipoPagoValido = True
                else:
                    messagebox.showwarning("Tipo de pago", "Ingrese 1, 2 o 3.")
    return tipoPagoPorPlaca

def alClickCierreDiario(listaObjetos, diccionario, espaciosEstacionamiento, archivoBaseDatos, carpetaReportes, carpetaVouchers, montoHora, tiempoDeGracia):
    hayPendientes = False
    for objeto in listaObjetos:
        if objeto.estadia[2] == "":
            hayPendientes = True
            break
    fechaCierre = datetime.now()
    if hayPendientes:
        confirmar = messagebox.askyesno("Cierre diario", "Se facturarán todos los vehículos pendientes y se liberarán sus espacios.\n\n¿Desea continuar?")
    else:
        confirmar = messagebox.askyesno("Cierre diario", "No hay vehículos pendientes por facturar.\n\n¿Desea generar el reporte del cierre diario con los vehículos ya facturados hoy?")
    if not confirmar:
        return
    if hayPendientes:
        tipoPagoPorPlaca = pedirTiposPagoPendientes(listaObjetos)
        if tipoPagoPorPlaca is None:
            return
        facturarPendientesCierreDiario(listaObjetos, diccionario, espaciosEstacionamiento, montoHora[0], tiempoDeGracia[0], carpetaVouchers, marcas, colores, tiposVehiculo, tiposPago, tipoPagoPorPlaca)
        guardarBaseDatos(listaObjetos, archivoBaseDatos)
    filasCierre = obtenerFilasCierreDiario(listaObjetos, fechaCierre)
    if len(filasCierre) == 0:
        messagebox.showwarning("Cierre diario", "No hay vehículos facturados para el cierre diario de hoy.")
        return
    archivoCierreDiario = carpetaReportes + "/ultimoCierreDiario.pkl"
    guardarUltimoCierreDiario(filasCierre, archivoCierreDiario)
    rutaPdf = crearReporteCierreDiarioPdf(filasCierre, carpetaReportes, tiposPago)
    messagebox.showinfo("Cierre diario", "Cierre diario finalizado.\n\nRegistros del reporte: " + str(len(filasCierre)) + "\nReporte: " + rutaPdf)

def alClickExportarCSV(carpetaReportes):
    archivoCierreDiario = carpetaReportes + "/ultimoCierreDiario.pkl"
    filasCierre = cargarUltimoCierreDiario(archivoCierreDiario)
    if len(filasCierre) == 0:
        messagebox.showwarning("Exportar CSV", "No hay un cierre diario generado para exportar.")
        return
    rutaCsv = exportarCierreDiarioCsv(filasCierre, carpetaReportes, tiposPago)
    messagebox.showinfo("Exportar CSV", "Archivo CSV generado correctamente.\nRuta: " + rutaCsv)

def botonCierreTipoPago(listaObjetos):
    if len(listaObjetos) == 0:
        messagebox.showwarning("Cierre por tipo de pago", "No hay vehículos registrados.")
        return ""
    rutaXML = cierreTipoPago(listaObjetos, "archivos", marcas, colores, tiposVehiculo, tiposPago)
    messagebox.showinfo("Cierre por tipo de pago", "Archivo XML generado correctamente.\nRuta: " + rutaXML)

def botonTamannoEstacionamiento(espaciosEstacionamiento, archivoConfiguracion):
    app = tk.Toplevel()
    app.title("Tamaño del estacionamiento")
    app.geometry("330x230")
    app.resizable(False, False)

    tk.Label(app, text="Tamaño actual del estacionamiento:").pack(pady=10)

    entryTamanno = tk.Entry(app)
    entryTamanno.insert(0, str(len(espaciosEstacionamiento)))
    entryTamanno.pack(pady=5)

    tk.Button(app, text="Confirmar", bg="#0d7703", fg="white", command=lambda: confirmarTamannoEstacionamiento(entryTamanno, espaciosEstacionamiento, archivoConfiguracion, app)).pack(pady=10)

    tk.Button(app, text="Regresar", bg="#770303", fg="white", command=app.destroy).pack(pady=5)

def confirmarTamannoEstacionamiento(entryTamanno, espaciosEstacionamiento, archivoConfiguracion, app):
    valor = entryTamanno.get().strip()
    if not valor.isdigit():
        messagebox.showwarning("Tamaño del estacionamiento", "Ingrese un número válido.")
        return
    nuevoTamanno = int(valor)
    if nuevoTamanno < 3:
        messagebox.showwarning("Tamaño del estacionamiento", "El tamaño mínimo permitido es 3.")
        return
    if hayVehiculosActivos(espaciosEstacionamiento):
        messagebox.showwarning("Tamaño del estacionamiento", "No se puede modificar el tamaño mientras existan vehículos activos.\n\nPrimero debe pagar los espacios ocupados o realizar el cierre diario.")
        return
    configuracion = cargarConfiguracion(archivoConfiguracion)
    if configuracion is None:
        configuracion = {}
    tieneElectrico = False
    if "tieneElectrico" in configuracion:
        tieneElectrico = configuracion["tieneElectrico"]
    confirmarCambio = messagebox.askyesno("Confirmar cambio", "¿Desea cambiar el tamaño del estacionamiento a " + str(nuevoTamanno) + " espacios?\n\nEsto reconstruirá los espacios porque no hay vehículos activos.")
    if not confirmarCambio:
        return
    nuevosEspacios = denominarEspacios(nuevoTamanno, tieneElectrico)
    espaciosEstacionamiento.clear()
    for espacio in nuevosEspacios:
        espaciosEstacionamiento.append(espacio)
    configuracion["tamanioEstacionamiento"] = nuevoTamanno
    configuracion["tieneElectrico"] = tieneElectrico
    guardarConfiguracion(configuracion, archivoConfiguracion)
    messagebox.showinfo("Tamaño del estacionamiento", "Tamaño actualizado correctamente.\n\nCierre y vuelva a abrir la ventana de estacionamiento para ver la nueva distribución.")
    app.destroy()

def hayVehiculosActivos(espaciosEstacionamiento):
    for espacio in espaciosEstacionamiento:
        if espacio["carro"] is not None:
            return True
    return False

def botonTiempoDeGracia(tiempoDeGracia, archivoConfiguracion):
    app = tk.Toplevel()
    app.title("Modificar tiempo de gracia")
    app.geometry("300x200")
    app.resizable(False, False)
    tk.Label(app, text="Tiempo de gracia (minutos): ").pack(pady=10)
    entryTiempo = tk.Entry(app)
    entryTiempo.insert(0, str(tiempoDeGracia[0]))
    entryTiempo.pack(pady=5)
    tk.Button(app, text="Confirmar", bg="#0d7703", fg="white", command=lambda: confirmarTiempoGracia(entryTiempo, tiempoDeGracia, app, archivoConfiguracion)).pack(pady=10)

def confirmarTiempoGracia(entryTiempo, tiempoDeGracia, app, archivoConfiguracion):
    valor = entryTiempo.get().strip()
    if not valor.isdigit():
        messagebox.showwarning("Error", "Ingrese un número válido.")
        return ""
    confirmarCambio = messagebox.askyesno("Confirmar", f"¿Cambiar tiempo de gracia a {valor} minutos?")
    if confirmarCambio:
        tiempoDeGracia[0] = int(valor)
        configuracion = cargarConfiguracion(archivoConfiguracion)
        if configuracion is None:
            configuracion = {}
        configuracion["tiempoDeGracia"] = tiempoDeGracia[0]
        guardarConfiguracion(configuracion, archivoConfiguracion)
        messagebox.showinfo("Éxito", "Tiempo de gracia actualizado correctamente.")
        app.destroy()

def botonModificarMontoHora(montoHora, archivoConfiguracion):
    app = tk.Toplevel()
    app.title("Modificar monto por hora")
    app.geometry("300x200")
    app.resizable(False, False)
    tk.Label(app, text="Monto por hora (₡):").pack(pady=10)
    entryMonto = tk.Entry(app)
    entryMonto.insert(0, str(montoHora[0]))
    entryMonto.pack(pady=5)
    tk.Button(app, text="Confirmar", bg="#0d7703", fg="white", command=lambda: confirmar(entryMonto, montoHora, app, archivoConfiguracion)).pack(pady=10)

def confirmar(entryMonto, montoHora, app, archivoConfiguracion):
    valor = entryMonto.get().strip()
    if not valor.isdigit():
        messagebox.showwarning("Error", "Ingrese un número válido.")
        return ""
    if int(valor) <= 0:
        messagebox.showwarning("Error", "El monto por hora debe ser mayor que cero.")
        return ""
    confirmarCambio = messagebox.askyesno("Confirmar", f"¿Cambiar monto a ₡{valor}?")
    if confirmarCambio:
        montoHora[0] = int(valor)
        configuracion = cargarConfiguracion(archivoConfiguracion)
        if configuracion is None:
            configuracion = {}
        configuracion["montoHora"] = montoHora[0]
        guardarConfiguracion(configuracion, archivoConfiguracion)
        messagebox.showinfo("Éxito", "Monto actualizado correctamente.")
        app.destroy()

def botonAcercaDe():
    app = tk.Toplevel()
    app.title("Acerca de")
    app.geometry("400x380")
    app.resizable(False, False)
    tk.Label(app, text="Acerca del Sistema", font=("SansSerif", 16, "bold")).pack(pady=15)
    info = (
        "Instituto Tecnológico de Costa Rica\nIngeniería en Computación\n"
    "Curso: Taller de Programación\nI Semestre 2026\nDesarrolladores:\nSebastián Rodriguez Vega y Fabián Eduarte Linkimer\n"
    "Github: \ngithub.com/sebastianrvg | github.com/faelink12"
    )
    tk.Label(app, text=info, font=("SansSerif", 10), justify="center").pack(pady=10)
    tk.Button(app, text="Regresar", bg="#770303", fg="white", font=("SansSerif", 10, "bold"), width=15, relief="flat", command=app.destroy).pack(pady=15)
