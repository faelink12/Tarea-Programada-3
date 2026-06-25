def crearFacturaPdf(objeto, carpetaVouchers):
    crearCarpetaSiNoExiste(carpetaVouchers)
    placa = objeto.info[0]
    marca = objeto.info[1]
    color = objeto.info[2]
    tipo = objeto.info[3]
    ubicacion = objeto.estadia[0]
    fechaHoraEntrada = objeto.estadia[1]
    fechaHoraSalida = objeto.estadia[2]
    monto = objeto.pago[0]
    tipoPago = objeto.pago[1]
    try:
        fecha = datetime.strptime(fechaHoraEntrada, "%Y-%m-%d %H:%M:%S")
        fechaTexto = fecha.strftime("%d-%m-%Y_%H-%M")
    except:
        fechaTexto = limpiarNombreArchivo(fechaHoraEntrada)
    nombreArchivo = "factura_" + str(placa) + "_" + fechaTexto + ".pdf"
    nombreArchivo = limpiarNombreArchivo(nombreArchivo)
    rutaPdf = os.path.join(carpetaVouchers, nombreArchivo)
    textoQr = "Placa: " + str(placa)
    textoQr += "\nMarca: " + str(marca)
    textoQr += "\nTipo: " + str(tipo)
    textoQr += "\nFecha y hora de entrada: " + str(fechaHoraEntrada)
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
    pdf.cell(0, 8, "Tipo de pago: " + str(tipoPago), ln=True)
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
