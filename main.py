import tkinter as tk
from tkinter import simpledialog, messagebox
from botones import construirVentanaPrincipal
from estacionamiento import denominarEspacios
from funciones import cargarBaseDatos
from funciones import reconstruirDiccionarioDesdeObjetos
from funciones import reconstruirEspaciosDesdeObjetos
from funciones import cargarConfiguracion
from funciones import guardarConfiguracion
def pedirEntero(mensajeTitulo, mensajeTexto, valorDefecto, valorMinimo, valorMaximo, ventanaRaiz):
    valorValido = False
    numero = valorDefecto
    while not valorValido:
        valorTexto = simpledialog.askstring(mensajeTitulo, mensajeTexto, parent=ventanaRaiz)
        if valorTexto is None:
            return valorDefecto
        valorTexto = valorTexto.strip()
        if not valorTexto.isdigit():
            messagebox.showwarning(mensajeTitulo, "Debe ingresar un número entero válido.")
        else:
            numero = int(valorTexto)
            if numero < valorMinimo:
                messagebox.showwarning(mensajeTitulo, "El número debe ser mayor o igual a " + str(valorMinimo) + ".")
            elif valorMaximo is not None and numero > valorMaximo:
                messagebox.showwarning(mensajeTitulo, "El número debe ser menor o igual a " + str(valorMaximo) + ".")
            else:
                valorValido = True
    return numero

def pedirConfiguracionInicial(ventanaRaiz):
    tamannoEstacionamiento = pedirEntero("Configuración inicial", "¿Cuántos parqueos tiene su estacionamiento?", 20, 3, None, ventanaRaiz)
    tieneElectrico = pedirEntero("Configuración inicial", "¿El estacionamiento tiene espacio para vehículos eléctricos? (1 = Sí, 0 = No)", 0, 0, 1, ventanaRaiz)
    tiempoDeGracia = pedirEntero("Configuración inicial", "Tiempo de gracia (minutos):", 10, 0, None, ventanaRaiz)
    montoHora = pedirEntero("Configuración inicial", "Monto por hora (₡):", 1000, 1, None, ventanaRaiz)
    configuracion = {
        "tamanioEstacionamiento": tamannoEstacionamiento,
        "tieneElectrico": bool(tieneElectrico),
        "tiempoDeGracia": tiempoDeGracia,
        "montoHora": montoHora
    }
    return configuracion

def main():
    archivoBaseDatos = "baseDatosParqueo.pkl"
    archivoConfiguracion = "configuracionParqueo.pkl"
    carpetaVouchers = "vouchers"
    carpetaReportes = "reportes"
    urlApiMockaroo = "https://my.api.mockaroo.com/vehiculos.json?key=5f760930"
    ventanaRaiz = tk.Tk()
    ventanaRaiz.withdraw()
    configuracion = cargarConfiguracion(archivoConfiguracion)
    if configuracion is None:
        configuracion = pedirConfiguracionInicial(ventanaRaiz)
        guardarConfiguracion(configuracion, archivoConfiguracion)
    ventanaRaiz.destroy()
    montoHora = [configuracion["montoHora"]]
    tiempoDeGracia = [configuracion["tiempoDeGracia"]]
    listaObjetos = cargarBaseDatos(archivoBaseDatos)
    diccionario = reconstruirDiccionarioDesdeObjetos(listaObjetos)
    espaciosEstacionamiento = denominarEspacios(configuracion["tamanioEstacionamiento"], configuracion["tieneElectrico"])
    espaciosEstacionamiento = reconstruirEspaciosDesdeObjetos(listaObjetos, espaciosEstacionamiento)
    construirVentanaPrincipal(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo, montoHora, tiempoDeGracia, archivoConfiguracion, carpetaReportes)

if __name__ == "__main__":
    main()
