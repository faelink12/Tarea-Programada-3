import tkinter as tk
from tkinter import messagebox
from estacionamiento import estacionamientoVentana
from estacionamiento import existeEspacioElectrico
from estacionamiento import obtenerUbicacionesGeneralesLibres
from estacionamiento import ocuparEspaciosMasivos
from estacionamiento import agregarObjetosEstacionamiento
from funciones import calcularTopeMasivo
from funciones import obtenerDatosVehiculos
from funciones import crearDiccionarioVehiculos
from funciones import agregarDiccionarioGlobal
from funciones import guardarBaseDatos
from funciones import crearVouchersMasivos
from funciones import imprimirDiccionarioVehiculos
from funciones import cierreTipoPago

def construirVentanaPrincipal(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo, montoHora, tiempoDeGracia):
    app = tk.Tk()
    app.title("Sistema de Parqueo")
    app.geometry("400x600")
    app.resizable(False, False)
    app.config(bg="#2D2F33")
    tk.Label(app, text="Sistema de Parqueo", bg="#2D2F33", fg="White", font=("SansSerif", 16, "bold")).pack(pady=15)
    tk.Label(app, text="1. Vehículos", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack()
    tk.Button(app, text="Obtener vehículos", bg="#8B1475", fg="white", font=("SansSerif", 10, "bold"), width=28, pady=8, relief="flat", command=lambda: alClickObtenerVehiculos(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo)).pack(pady=4)
    tk.Button(app, text="Ver estacionamiento", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: estacionamientoVentana(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers)).pack(pady=2)
    tk.Label(app, text="2. Reportes", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack(pady=(10, 0))
    tk.Button(app, text="Cierre diario", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: alClickCierreDiario(listaObjetos)).pack(pady=2)
    tk.Button(app, text="Cierre por tipo de pago", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: botonCierreTipoPago(listaObjetos)).pack(pady=2)
    tk.Button(app, text="Exportar cierre diario a CSV", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: alClickExportarCSV(listaObjetos)).pack(pady=2)
    tk.Label(app, text="3. Configuración", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack(pady=(10, 0))
    tk.Button(app, text="Tamaño del estacionamiento", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: botonTamannoEstacionamiento(espaciosEstacionamiento)).pack(pady=2)
    tk.Button(app, text="Tiempo de gracia en minutos", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: botonTiempoDeGracia(tiempoDeGracia)).pack(pady=2)
    tk.Button(app, text="Modificar monto por hora", bg="#4a4a4a", fg="white", font=("SansSerif", 10), width=28, pady=6, relief="flat", command=lambda: botonModificarMontoHora(montoHora)).pack(pady=2)
    tk.Label(app, text="4. Acerca de", bg="#2D2F33", fg="white", font=("SansSerif", 9, "italic")).pack(pady=(10, 0))
    tk.Button(app, text="Acerca de", bg="#8B1475", fg="white", font=("SansSerif", 10, "bold"), width=28, pady=8, relief="flat", command=botonAcercaDe).pack(pady=4)
    app.mainloop()

def alClickObtenerVehiculos(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo):
    try:
        tamanioEstacionamiento = len(espaciosEstacionamiento)
        tieneElectrico = existeEspacioElectrico(espaciosEstacionamiento)
        topeMasivo = calcularTopeMasivo(tamanioEstacionamiento, tieneElectrico)
        ubicacionesLibres = obtenerUbicacionesGeneralesLibres(espaciosEstacionamiento)
        cantidadVehiculos = topeMasivo
        if cantidadVehiculos > len(ubicacionesLibres):
            cantidadVehiculos = len(ubicacionesLibres)
        if cantidadVehiculos <= 0:
            messagebox.showwarning("Obtener vehículos", "No hay espacios generales disponibles para carga masiva.")
            return
        confirmar = messagebox.askyesno("Obtener vehículos", "Se cargarán " + str(cantidadVehiculos) + " vehículos generales.\n\nDesea continuar?")
        if not confirmar:
            return
        datosVehiculos = obtenerDatosVehiculos(cantidadVehiculos, urlApiMockaroo)
        diccionarioVehiculos = crearDiccionarioVehiculos(diccionario, datosVehiculos, ubicacionesLibres, cantidadVehiculos)
        if len(diccionarioVehiculos) == 0:
            messagebox.showwarning("Obtener vehículos", "No se pudieron generar vehículos.")
            return
        imprimirDiccionarioVehiculos(diccionarioVehiculos)
        agregarDiccionarioGlobal(diccionario, diccionarioVehiculos)
        agregarObjetosEstacionamiento(listaObjetos, diccionarioVehiculos)
        ocuparEspaciosMasivos(diccionarioVehiculos, espaciosEstacionamiento)
        guardarBaseDatos(listaObjetos, archivoBaseDatos)
        cantidadVouchers = crearVouchersMasivos(diccionarioVehiculos, listaObjetos, carpetaVouchers)
        messagebox.showinfo("Obtener vehículos", "Carga masiva finalizada.\n\nVehículos cargados: " + str(len(diccionarioVehiculos)) + "\nVouchers generados: " + str(cantidadVouchers))
    except ValueError:
        messagebox.showerror("Error", "No se pudo obtener la información de vehículos.")
    except Exception:
        messagebox.showerror("Error", "No se pudo completar la carga masiva.")

def alClickCierreDiario(listaObjetos):
    print("Cierre diario")
    messagebox.showinfo("Cierre diario", "Función de cierre diario pendiente.")

def alClickExportarCSV(listaObjetos):
    print("Exportar cierre diario a CSV")
    messagebox.showinfo("Exportar CSV", "Función de exportar cierre diario a CSV pendiente.")

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

def botonCierreTipoPago(listaObjetos):
    if len(listaObjetos) == 0:
        messagebox.showwarning("Cierre por tipo de pago", "No hay vehículos registrados.")
        return ""
    rutaXML = cierreTipoPago(listaObjetos, "archivos")
    messagebox.showinfo("Cierre por tipo de pago", "Archivo XML generado correctamente.\nRuta: " + rutaXML)

def botonModificarMontoHora(montoHora):
    app = tk.Toplevel()
    app.title("Modificar monto por hora")
    app.geometry("300x200")
    app.resizable(False, False)
    tk.Label(app, text="Monto por hora (₡):").pack(pady=10)
    entryMonto = tk.Entry(app)
    entryMonto.insert(0, str(montoHora[0]))
    entryMonto.pack(pady=5)
    tk.Button(app, text="Confirmar", bg="#0d7703", fg="white", command=lambda: confirmar(entryMonto, montoHora, app)).pack(pady=10)

def confirmar(entryMonto, montoHora, app):
    valor = entryMonto.get().strip()
    if not valor.isdigit():
        messagebox.showwarning("Error", "Ingrese un número válido.")
        return ""
    confirmarCambio = messagebox.askyesno("Confirmar", f"¿Cambiar monto a ₡{valor}?")
    if confirmarCambio:
        montoHora[0] = int(valor)
        messagebox.showinfo("Éxito", "Monto actualizado correctamente.")
        app.destroy()

def botonTiempoDeGracia(tiempoDeGracia):
    app = tk.Toplevel()
    app.title("Modificar tiempo de gracia")
    app.geometry("300x200")
    app.resizable(False, False)
    tk.Label(app, text="Tiempo de gracia (minutos): ").pack(pady=10)
    entryTiempo = tk.Entry(app)
    entryTiempo.insert(0, str(tiempoDeGracia[0]))
    entryTiempo.pack(pady=5)
    tk.Button(app, text="Confirmar", bg="#0d7703", fg="white", command=lambda: confirmarTiempoGracia(entryTiempo, tiempoDeGracia, app)).pack(pady=10)

def confirmarTiempoGracia(entryTiempo, tiempoDeGracia, app):
    valor = entryTiempo.get().strip()
    if not valor.isdigit():
        messagebox.showwarning("Error", "Ingrese un número válido.")
        return ""
    confirmarCambio = messagebox.askyesno("Confirmar", f"¿Cambiar tiempo de gracia a {valor} minutos?")
    if confirmarCambio:
        tiempoDeGracia[0] = int(valor)
        messagebox.showinfo("Éxito", "Tiempo de gracia actualizado correctamente.")
        app.destroy()

def botonTamannoEstacionamiento(espaciosEstacionamiento):
    app = tk.Toplevel()
    app.title("Tamaño del estacionamiento")
    app.geometry("300x150")
    app.resizable(False, False)
    tk.Label(app, text="Tamaño del estacionamiento:").pack(pady=10)
    entryTamanno = tk.Entry(app)
    entryTamanno.insert(0, str(len(espaciosEstacionamiento)))
    entryTamanno.config(state="readonly")
    entryTamanno.pack(pady=5)
