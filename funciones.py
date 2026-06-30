import json
import random
import string
from datetime import datetime
from datetime import timedelta
import os
import pickle
import urllib.request
from fpdf import FPDF
import qrcode

def crearPlaca():
    letras = ''.join(random.choices(string.ascii_uppercase, k=3))
    numeros = ''.join(random.choices(string.digits, k=3))
    return letras + "-" + numeros

def crearPlacaUnica(diccionario, diccionarioTemporal):
    placa = crearPlaca()
    placaRepetida = True
    while placaRepetida:
        placaRepetida = False
        if placa in diccionario:
            placaRepetida = True
        if placa in diccionarioTemporal:
            placaRepetida = True
        if placaRepetida:
            placa = crearPlaca()
    return placa

def redondearHaciaArriba(numero):
    entero = int(numero)
    if numero > entero:
        return entero + 1
    return entero

def calcularCantidadEspeciales(tamanioEstacionamiento):
    cantidadEspeciales = redondearHaciaArriba(tamanioEstacionamiento * 0.05)
    if cantidadEspeciales < 2:
        cantidadEspeciales = 2
    if cantidadEspeciales > tamanioEstacionamiento:
        cantidadEspeciales = tamanioEstacionamiento
    return cantidadEspeciales

def calcularTopeMasivo(tamanioEstacionamiento, tieneElectrico):
    cantidadEspeciales = calcularCantidadEspeciales(tamanioEstacionamiento)
    cantidadElectricos = 0
    if tieneElectrico:
        cantidadElectricos = 1
    cantidadGeneral = tamanioEstacionamiento - cantidadEspeciales - cantidadElectricos
    if cantidadGeneral <= 0:
        return 0
    cantidadLibreClientes = redondearHaciaArriba(cantidadGeneral * 0.05)
    topeMasivo = cantidadGeneral - cantidadLibreClientes
    if topeMasivo < 0:
        topeMasivo = 0
    return topeMasivo

def guardarConfiguracion(configuracion, archivoConfiguracion):
    with open(archivoConfiguracion, "wb") as archivo:
        pickle.dump(configuracion, archivo)

def cargarConfiguracion(archivoConfiguracion):
    if not os.path.exists(archivoConfiguracion):
        return None
    try:
        with open(archivoConfiguracion, "rb") as archivo:
            configuracion = pickle.load(archivo)
        if isinstance(configuracion, dict):
            return configuracion
        return None
    except Exception:
        return None

def guardarBaseDatos(listaObjetos, archivoBaseDatos):
    with open(archivoBaseDatos, "wb") as archivo:
        pickle.dump(listaObjetos, archivo)

def cargarBaseDatos(archivoBaseDatos):
    if not os.path.exists(archivoBaseDatos):
        return []
    try:
        with open(archivoBaseDatos, "rb") as archivo:
            listaObjetos = pickle.load(archivo)
        if isinstance(listaObjetos, list):
            return listaObjetos
        return []
    except Exception:
        return []

def crearFechaHoraEntradaAleatoria():
    horaActual = datetime.now()
    horaApertura = horaActual.replace(hour=7, minute=0, second=0, microsecond=0)
    if horaActual < horaApertura:
        return horaActual.strftime("%Y-%m-%d %H:%M:%S")
    segundosMaximos = int((horaActual - horaApertura).total_seconds())
    if segundosMaximos <= 0:
        return horaActual.strftime("%Y-%m-%d %H:%M:%S")
    segundosAleatorios = random.randint(0, segundosMaximos)
    fechaHoraEntrada = horaApertura + timedelta(seconds=segundosAleatorios)
    return fechaHoraEntrada.strftime("%Y-%m-%d %H:%M:%S")

def calcularMontoEstadia(fechaHoraEntrada, fechaHoraSalida, montoHora, tiempoDeGracia):
    entrada = datetime.strptime(fechaHoraEntrada, "%Y-%m-%d %H:%M:%S")
    salida = datetime.strptime(fechaHoraSalida, "%Y-%m-%d %H:%M:%S")
    minutosEstadia = (salida - entrada).total_seconds() / 60
    if minutosEstadia <= tiempoDeGracia:
        return 0
    horasEstadia = minutosEstadia / 60
    horasCobradas = redondearHaciaArriba(horasEstadia)
    return horasCobradas * montoHora

def obtenerDatoCarro(carro, llave, valorDefecto):
    if llave in carro:
        if carro[llave] is not None:
            if str(carro[llave]).strip() != "":
                return str(carro[llave])
    return valorDefecto

def obtenerDatosVehiculos(cantidadVehiculos, urlApiMockaroo):
    separador = "?"
    if "?" in urlApiMockaroo:
        separador = "&"
    urlCompleta = urlApiMockaroo + separador + "count=" + str(cantidadVehiculos)
    respuesta = urllib.request.urlopen(urlCompleta, timeout=15)
    contenido = respuesta.read().decode("utf-8")
    datosVehiculos = json.loads(contenido)
    if isinstance(datosVehiculos, dict):
        datosConvertidos = []
        datosConvertidos.append(datosVehiculos)
        datosVehiculos = datosConvertidos
    if not isinstance(datosVehiculos, list):
        raise ValueError()
    return datosVehiculos

def obtenerMarcasYTiposApi(urlApiMockaroo, catalogoMarcas, catalogoTipos):
    try:
        datosVehiculos = obtenerDatosVehiculos(10, urlApiMockaroo)
        marcasApi = []
        tiposApi = []
        for carro in datosVehiculos:
            marcaTexto = obtenerDatoCarro(carro, "Marca", "")
            tipoTexto = obtenerDatoCarro(carro, "Tipo", "")
            if marcaTexto in catalogoMarcas.values() and marcaTexto not in marcasApi:
                marcasApi.append(marcaTexto)
            if tipoTexto in catalogoTipos.values() and tipoTexto not in tiposApi:
                tiposApi.append(tipoTexto)
        marcasApi.sort()
        tiposApi.sort()
        if len(marcasApi) == 0:
            marcasApi = list(catalogoMarcas.values())
        if len(tiposApi) == 0:
            tiposApi = list(catalogoTipos.values())
        return marcasApi, tiposApi
    except Exception:
        return list(catalogoMarcas.values()), list(catalogoTipos.values())

def crearDiccionarioVehiculos(diccionario, datosVehiculos, ubicacionesLibres, cantidadVehiculos, catalogoMarcas, catalogoColores, catalogoTipos):
    diccionarioVehiculos = {}
    contador = 0
    for carro in datosVehiculos:
        if contador < cantidadVehiculos:
            if contador < len(ubicacionesLibres):
                placa = crearPlacaUnica(diccionario, diccionarioVehiculos)
                marcaTexto = obtenerDatoCarro(carro, "Marca", "Toyota")
                colorTexto = obtenerDatoCarro(carro, "Color", "Azul")
                tipoTexto = obtenerDatoCarro(carro, "Tipo", "Automovil")
                marca = convertirTextoAId(catalogoMarcas, marcaTexto, 0)
                color = convertirTextoAId(catalogoColores, colorTexto, 0)
                tipo = convertirTextoAId(catalogoTipos, tipoTexto, 0)
                ubicacion = str(ubicacionesLibres[contador])
                fechaHoraEntrada = crearFechaHoraEntradaAleatoria()
                fechaHoraSalida = ""
                monto = 0
                tipoPago = 0
                diccionarioVehiculos[placa] = [marca, color, tipo, ubicacion, fechaHoraEntrada, fechaHoraSalida, monto, tipoPago]
                contador += 1
    return diccionarioVehiculos

def agregarDiccionarioGlobal(diccionario, diccionarioVehiculos):
    for placa, datos in diccionarioVehiculos.items():
        diccionario[placa] = datos

def reconstruirDiccionarioDesdeObjetos(listaObjetos):
    diccionario = {}
    for objeto in listaObjetos:
        placa = objeto.info[0]
        marca = objeto.info[1]
        color = objeto.info[2]
        tipo = objeto.info[3]
        ubicacion = objeto.estadia[0]
        fechaHoraEntrada = objeto.estadia[1]
        fechaHoraSalida = objeto.estadia[2]
        monto = objeto.pago[0]
        tipoPago = objeto.pago[1]
        if fechaHoraSalida == "":
            diccionario[placa] = [marca, color, tipo, ubicacion, fechaHoraEntrada, fechaHoraSalida, monto, tipoPago]
    return diccionario

def reconstruirEspaciosDesdeObjetos(listaObjetos, espacios):
    for objeto in listaObjetos:
        placa = objeto.info[0]
        ubicacion = objeto.estadia[0]
        fechaHoraSalida = objeto.estadia[2]
        if fechaHoraSalida == "":
            try:
                indice = int(ubicacion) - 1
                if indice >= 0 and indice < len(espacios):
                    espacios[indice]["carro"] = placa
            except ValueError:
                pass
    return espacios

def crearCarpetaSiNoExiste(nombreCarpeta):
    if not os.path.exists(nombreCarpeta):
        os.makedirs(nombreCarpeta)

def limpiarNombreArchivo(texto):
    textoLimpio = str(texto)
    caracteresInvalidos = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
    for caracter in caracteresInvalidos:
        textoLimpio = textoLimpio.replace(caracter, "-")
    return textoLimpio

def crearTextoQrVoucher(objeto, catalogoMarcas, catalogoTipos):
    placa = objeto.info[0]
    marca = convertirIdATexto(catalogoMarcas, objeto.info[1], "Desconocida")
    tipo = convertirIdATexto(catalogoTipos, objeto.info[3], "Desconocido")
    fechaHoraEntrada = objeto.estadia[1]
    textoQr = str(placa) + "-" + str(marca) + "-" + str(tipo) + "-" + str(fechaHoraEntrada)
    return textoQr

def crearNombreVoucher(objeto):
    placa = objeto.info[0]
    fechaHoraEntrada = objeto.estadia[1]
    try:
        fecha = datetime.strptime(fechaHoraEntrada, "%Y-%m-%d %H:%M:%S")
        fechaTexto = fecha.strftime("%d-%m-%Y_%H-%M")
    except ValueError:
        fechaTexto = limpiarNombreArchivo(fechaHoraEntrada)
    nombreArchivo = "voucher_#" + str(placa) + "_" + fechaTexto + ".pdf"
    nombreArchivo = limpiarNombreArchivo(nombreArchivo)
    return nombreArchivo

def crearVoucherPdf(objeto, carpetaVouchers, catalogoMarcas, catalogoColores, catalogoTipos):
    crearCarpetaSiNoExiste(carpetaVouchers)
    placa = objeto.info[0]
    marca = convertirIdATexto(catalogoMarcas, objeto.info[1], "Desconocida")
    color = convertirIdATexto(catalogoColores, objeto.info[2], "Desconocido")
    tipo = convertirIdATexto(catalogoTipos, objeto.info[3], "Desconocido")
    ubicacion = objeto.estadia[0]
    fechaHoraEntrada = objeto.estadia[1]
    nombreArchivo = crearNombreVoucher(objeto)
    rutaPdf = os.path.join(carpetaVouchers, nombreArchivo)
    textoQr = crearTextoQrVoucher(objeto, catalogoMarcas, catalogoTipos)
    imagenQr = qrcode.make(textoQr)
    nombreQr = "qr_" + limpiarNombreArchivo(str(placa)) + ".png"
    rutaQr = os.path.join(carpetaVouchers, nombreQr)
    imagenQr.save(rutaQr)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Voucher de Estacionamiento", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, "Placa: " + str(placa), ln=True)
    pdf.cell(0, 8, "Marca: " + str(marca), ln=True)
    pdf.cell(0, 8, "Color: " + str(color), ln=True)
    pdf.cell(0, 8, "Tipo: " + str(tipo), ln=True)
    pdf.cell(0, 8, "Ubicacion: " + str(ubicacion), ln=True)
    pdf.cell(0, 8, "Fecha y hora de entrada: " + str(fechaHoraEntrada), ln=True)
    pdf.ln(10)
    pdf.cell(0, 8, "Codigo QR:", ln=True)
    pdf.image(rutaQr, x=80, y=100, w=50, h=50)
    pdf.output(rutaPdf)
    try:
        os.remove(rutaQr)
    except OSError:
        pass
    return rutaPdf

def crearVouchersMasivos(diccionarioVehiculos, listaObjetos, carpetaVouchers, catalogoMarcas, catalogoColores, catalogoTipos):
    cantidadVouchers = 0
    for objeto in listaObjetos:
        placaObjeto = objeto.info[0]
        if placaObjeto in diccionarioVehiculos:
            crearVoucherPdf(objeto, carpetaVouchers, catalogoMarcas, catalogoColores, catalogoTipos)
            cantidadVouchers += 1
    return cantidadVouchers

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

def convertirTextoAId(catalogo, texto, idDefecto):
    for idValor, valorTexto in catalogo.items():
        if valorTexto == texto:
            return idValor
    if texto == "":
        return idDefecto
    nuevoId = max(catalogo.keys()) + 1
    catalogo[nuevoId] = texto
    return nuevoId

def convertirIdATexto(catalogo, idValor, textoDefecto):
    if idValor in catalogo:
        return catalogo[idValor]
    return textoDefecto

def imprimirDiccionarioVehiculos(diccionarioVehiculos):
    print("- DICCIONARIO DE VEHICULOS CARGADOS -")
    print(json.dumps(diccionarioVehiculos, indent=4, ensure_ascii=False))
    print("---------------------")
