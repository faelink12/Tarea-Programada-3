def botonCierreTipoPago(listaObjetos):
    if len(listaObjetos) == 0:
        messagebox.showwarning("Cierre por tipo de pago", "No hay vehículos registrados.")
        return ""
    rutaXML = cierreTipoPago(listaObjetos, "archivos")
    messagebox.showinfo("Cierre por tipo de pago", "Archivo XML generado correctamente.\nRuta: " + rutaXML)
