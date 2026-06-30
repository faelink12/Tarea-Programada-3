def alClickCierreDiario(listaObjetos, diccionario, espaciosEstacionamiento, archivoBaseDatos, carpetaReportes, carpetaVouchers, montoHora, tiempoDeGracia):
    hayPendientes = False
    for objeto in listaObjetos:
        if objeto.estadia[2] == "":
            hayPendientes = True
            break
    if not hayPendientes:
        messagebox.showwarning("Cierre diario", "No hay vehículos pendientes por facturar.")
        return
    confirmar = messagebox.askyesno("Cierre diario", "Se facturarán todos los vehículos pendientes y se liberarán sus espacios.\n\n¿Desea continuar?")
    if not confirmar:
        return
    filasCierre = facturarPendientesCierreDiario(listaObjetos, diccionario, espaciosEstacionamiento, montoHora[0], tiempoDeGracia[0], carpetaVouchers, marcas, colores, tiposVehiculo, tiposPago)
    guardarBaseDatos(listaObjetos, archivoBaseDatos)
    archivoCierreDiario = carpetaReportes + "/ultimoCierreDiario.pkl"
    guardarUltimoCierreDiario(filasCierre, archivoCierreDiario)
    rutaPdf = crearReporteCierreDiarioPdf(filasCierre, carpetaReportes, tiposPago)
    messagebox.showinfo("Cierre diario", "Cierre diario finalizado.\n\nVehículos facturados: " + str(len(filasCierre)) + "\nReporte: " + rutaPdf)


def facturarPendientesCierreDiario(listaObjetos, diccionario, espacios, montoHora, tiempoDeGracia, carpetaVouchers, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago):
    fechaHoraSalida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tiposPagoDisponibles = list(catalogoTiposPago.keys())
    indiceTipoPago = 0
    filasCierre = []
    for objeto in listaObjetos:
        if objeto.estadia[2] == "":
            placa = objeto.info[0]
            tipoPago = tiposPagoDisponibles[indiceTipoPago % len(tiposPagoDisponibles)]
            indiceTipoPago += 1
            monto = calcularMontoEstadia(objeto.estadia[1], fechaHoraSalida, montoHora, tiempoDeGracia)
            objeto.estadia[2] = fechaHoraSalida
            objeto.pago = (monto, tipoPago)
            crearFacturaPdf(objeto, carpetaVouchers, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago)
            if placa in diccionario:
                del diccionario[placa]
            try:
                indice = int(objeto.estadia[0]) - 1
                if indice >= 0 and indice < len(espacios):
                    espacios[indice]["carro"] = None
            except ValueError:
                pass
            filasCierre.append([objeto.estadia[0], placa, objeto.estadia[1], objeto.estadia[2], tipoPago, monto])
    return filasCierre


def guardarUltimoCierreDiario(filasCierre, archivoCierreDiario):
    crearCarpetaSiNoExiste(os.path.dirname(archivoCierreDiario))
    with open(archivoCierreDiario, "wb") as archivo:
        pickle.dump(filasCierre, archivo)


def crearReporteCierreDiarioPdf(filasCierre, carpetaReportes, catalogoTiposPago):
    crearCarpetaSiNoExiste(carpetaReportes)
    fechaTexto = datetime.now().strftime("%d-%m-%Y_%H-%M")
    nombreArchivo = limpiarNombreArchivo("cierreDiario_" + fechaTexto + ".pdf")
    rutaPdf = os.path.join(carpetaReportes, nombreArchivo)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_text_color(20, 20, 90)
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 12, "Cierre Diario de Estacionamiento", ln=True, align="C")
    pdf.set_text_color(80, 80, 80)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, "Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ln=True, align="C")
    pdf.ln(6)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 10)
    anchos = [22, 28, 35, 35, 30, 30]
    encabezados = ["Ubicacion", "Placa", "Hora entrada", "Hora salida", "Tipo de pago", "Monto"]
    for indice in range(len(encabezados)):
        pdf.cell(anchos[indice], 8, encabezados[indice], border=1, align="C")
    pdf.ln()
    pdf.set_font("Arial", "", 9)
    montosPorTipo = {1: 0, 2: 0, 3: 0}
    montoTotal = 0
    for fila in filasCierre:
        ubicacion, placa, horaEntrada, horaSalida, tipoPago, monto = fila
        tipoPagoTexto = convertirIdATexto(catalogoTiposPago, tipoPago, "Desconocido")
        pdf.cell(anchos[0], 8, str(ubicacion), border=1, align="C")
        pdf.cell(anchos[1], 8, str(placa), border=1, align="C")
        pdf.cell(anchos[2], 8, str(horaEntrada), border=1, align="C")
        pdf.cell(anchos[3], 8, str(horaSalida), border=1, align="C")
        pdf.cell(anchos[4], 8, str(tipoPagoTexto), border=1, align="C")
        pdf.cell(anchos[5], 8, "C" + str(monto), border=1, align="C")
        pdf.ln()
        if tipoPago in montosPorTipo:
            montosPorTipo[tipoPago] += monto
        montoTotal += monto
    pdf.ln(8)
    pdf.set_text_color(20, 90, 20)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Subtotales por tipo de pago", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "", 11)
    for idTipoPago, montoTipo in montosPorTipo.items():
        tipoPagoTexto = convertirIdATexto(catalogoTiposPago, idTipoPago, "Desconocido")
        pdf.cell(0, 7, tipoPagoTexto + ": C" + str(montoTipo), ln=True)
    pdf.ln(4)
    pdf.set_text_color(150, 0, 0)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Monto total acumulado del dia: C" + str(montoTotal), ln=True)
    pdf.output(rutaPdf)
    return rutaPdf


def crearFacturaPdf(objeto, carpetaVouchers, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago):
    crearCarpetaSiNoExiste(carpetaVouchers)
    placa = objeto.info[0]
    marca = convertirIdATexto(catalogoMarcas, objeto.info[1], "Desconocida")
    color = convertirIdATexto(catalogoColores, objeto.info[2], "Desconocido")
    tipo = convertirIdATexto(catalogoTipos, objeto.info[3], "Desconocido")
    ubicacion = objeto.estadia[0]
    fechaHoraEntrada = objeto.estadia[1]
    fechaHoraSalida = objeto.estadia[2]
    monto = objeto.pago[0]
    tipoPagoTexto = convertirIdATexto(catalogoTiposPago, objeto.pago[1], "Desconocido")
    try:
        fecha = datetime.strptime(fechaHoraSalida, "%Y-%m-%d %H:%M:%S")
        fechaTexto = fecha.strftime("%d-%m-%Y_%H-%M")
    except:
        fechaTexto = limpiarNombreArchivo(fechaHoraSalida)
    nombreArchivo = "factura_#" + str(placa) + "_" + fechaTexto + ".pdf"
    nombreArchivo = limpiarNombreArchivo(nombreArchivo)
    rutaPdf = os.path.join(carpetaVouchers, nombreArchivo)
    textoQr = str(placa) + "-" + str(marca) + "-" + str(color) + "-" + str(tipo)
    textoQr += "-" + str(ubicacion) + "-" + str(fechaHoraEntrada) + "-" + str(fechaHoraSalida)
    textoQr += "-" + str(tipoPagoTexto) + "-" + str(monto)
    imagenQr = qrcode.make(textoQr)
    nombreQr = "qr_factura_" + limpiarNombreArchivo(str(placa)) + ".png"
    rutaQr = os.path.join(carpetaVouchers, nombreQr)
    imagenQr.save(rutaQr)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Factura de Estacionamiento", ln=True, align="C")
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "Placa: " + str(placa), ln=True)
    pdf.cell(0, 8, "Marca: " + str(marca), ln=True)
    pdf.cell(0, 8, "Color: " + str(color), ln=True)
    pdf.cell(0, 8, "Tipo: " + str(tipo), ln=True)
    pdf.cell(0, 8, "Ubicacion: " + str(ubicacion), ln=True)
    pdf.cell(0, 8, "Fecha y hora de entrada: " + str(fechaHoraEntrada), ln=True)
    pdf.cell(0, 8, "Fecha y hora de salida: " + str(fechaHoraSalida), ln=True)
    pdf.cell(0, 8, "Tipo de pago: " + str(tipoPagoTexto), ln=True)
    pdf.cell(0, 8, "Monto: " + str(monto), ln=True)
    pdf.ln(10)
    pdf.cell(0, 8, "Codigo QR:", ln=True)
    pdf.image(rutaQr, x=80, y=pdf.get_y(), w=50, h=50)
    pdf.output(rutaPdf)
    try:
        os.remove(rutaQr)
    except OSError:
        pass
    return rutaPdf
