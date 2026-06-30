def alClickExportarCSV(carpetaReportes):
    archivoCierreDiario = carpetaReportes + "/ultimoCierreDiario.pkl"
    filasCierre = cargarUltimoCierreDiario(archivoCierreDiario)
    if len(filasCierre) == 0:
        messagebox.showwarning("Exportar CSV", "No hay un cierre diario generado para exportar.")
        return
    rutaCsv = exportarCierreDiarioCsv(filasCierre, carpetaReportes, tiposPago)
    messagebox.showinfo("Exportar CSV", "Archivo CSV generado correctamente.\nRuta: " + rutaCsv)


def cargarUltimoCierreDiario(archivoCierreDiario):
    if not os.path.exists(archivoCierreDiario):
        return []
    try:
        with open(archivoCierreDiario, "rb") as archivo:
            filasCierre = pickle.load(archivo)
        if isinstance(filasCierre, list):
            return filasCierre
        return []
    except Exception:
        return []


def exportarCierreDiarioCsv(filasCierre, carpetaReportes, catalogoTiposPago):
    crearCarpetaSiNoExiste(carpetaReportes)
    rutaCsv = os.path.join(carpetaReportes, "cierreDiario.csv")
    with open(rutaCsv, "w", newline="", encoding="utf-8") as archivoCsv:
        escritor = csv.writer(archivoCsv)
        for fila in filasCierre:
            ubicacion, placa, horaEntrada, horaSalida, tipoPago, monto = fila
            tipoPagoTexto = convertirIdATexto(catalogoTiposPago, tipoPago, "Desconocido")
            escritor.writerow([ubicacion, placa, horaEntrada, horaSalida, tipoPagoTexto, monto])
    return rutaCsv


def crearCarpetaSiNoExiste(nombreCarpeta):
    if not os.path.exists(nombreCarpeta):
        os.makedirs(nombreCarpeta)


def convertirIdATexto(catalogo, idValor, textoDefecto):
    if idValor in catalogo:
        return catalogo[idValor]
    return textoDefecto
