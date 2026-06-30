import os
import pickle
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
from fpdf import FPDF
from funciones import crearCarpetaSiNoExiste
from funciones import limpiarNombreArchivo
from funciones import convertirIdATexto
from funciones import calcularMontoEstadia
from funciones import crearFacturaPdf

def cierreTipoPago(listaObjetos, carpetaArchivos, catalogoMarcas, catalogoColores, catalogoTipos, catalogoTiposPago):
    raiz = ET.Element("estacionamiento")
    efectivo = ET.SubElement(raiz, "efectivo")
    sinpe = ET.SubElement(raiz, "sinpe")
    tarjeta = ET.SubElement(raiz, "tarjeta")
    for objeto in listaObjetos:
        tipoPago = objeto.pago[1]
        if tipoPago == 1:
            seccion = efectivo
        elif tipoPago == 2:
            seccion = sinpe
        elif tipoPago == 3:
            seccion = tarjeta
        else:
            continue
        vehiculo = ET.SubElement(seccion, "vehiculo")
        ET.SubElement(vehiculo, "id").text = str(objeto.id)
        ET.SubElement(vehiculo, "placa").text = str(objeto.info[0])
        ET.SubElement(vehiculo, "marca").text = convertirIdATexto(catalogoMarcas, objeto.info[1], "Desconocida")
        ET.SubElement(vehiculo, "color").text = convertirIdATexto(catalogoColores, objeto.info[2], "Desconocido")
        ET.SubElement(vehiculo, "tipo").text = convertirIdATexto(catalogoTipos, objeto.info[3], "Desconocido")
        ET.SubElement(vehiculo, "ubicacion").text = str(objeto.estadia[0])
        ET.SubElement(vehiculo, "fechaEntrada").text = str(objeto.estadia[1])
        ET.SubElement(vehiculo, "fechaSalida").text = str(objeto.estadia[2])
        ET.SubElement(vehiculo, "monto").text = str(objeto.pago[0])
        ET.SubElement(vehiculo, "tipoPago").text = convertirIdATexto(catalogoTiposPago, objeto.pago[1], "Desconocido")
    crearCarpetaSiNoExiste(carpetaArchivos)
    arbol = ET.ElementTree(raiz)
    rutaXML = os.path.join(carpetaArchivos, "cierreTipoPago.xml")
    arbol.write(rutaXML, encoding="utf-8-sig", xml_declaration=True)
    return rutaXML

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
            fila = [objeto.estadia[0], placa, objeto.estadia[1], objeto.estadia[2], tipoPago, monto]
            filasCierre.append(fila)
    return filasCierre

def guardarUltimoCierreDiario(filasCierre, archivoCierreDiario):
    carpetaCierre = os.path.dirname(archivoCierreDiario)
    crearCarpetaSiNoExiste(carpetaCierre)
    with open(archivoCierreDiario, "wb") as archivo:
        pickle.dump(filasCierre, archivo)

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
        ubicacion = fila[0]
        placa = fila[1]
        horaEntrada = fila[2]
        horaSalida = fila[3]
        tipoPago = fila[4]
        monto = fila[5]
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

def exportarCierreDiarioCsv(filasCierre, carpetaReportes, catalogoTiposPago):
    crearCarpetaSiNoExiste(carpetaReportes)
    rutaCsv = os.path.join(carpetaReportes, "cierreDiario.csv")
    with open(rutaCsv, "w", newline="", encoding="utf-8") as archivoCsv:
        escritor = csv.writer(archivoCsv)
        for fila in filasCierre:
            ubicacion = fila[0]
            placa = fila[1]
            horaEntrada = fila[2]
            horaSalida = fila[3]
            tipoPago = fila[4]
            monto = fila[5]
            tipoPagoTexto = convertirIdATexto(catalogoTiposPago, tipoPago, "Desconocido")
            escritor.writerow([ubicacion, placa, horaEntrada, horaSalida, tipoPagoTexto, monto])
    return rutaCsv