def confirmarPago(diccionario, listaObjetos, espacios, botones, espacio, placa, tipoPagoTexto, monto, fechaSalidaStr, archivoBaseDatos, carpetaVouchers, app, mainApp):
    tiposPagoInverso = {v: k for k,v in tiposPago.items()}
    tiposPagoInt = tiposPagoInverso[tipoPagoTexto]
    diccionario[placa][5] = fechaSalidaStr
    diccionario[placa][6] = monto
    diccionario[placa][7] = tiposPagoInt
    for objeto in listaObjetos:
        if objeto.info[0] == placa:
            objeto.estadia[2] = fechaSalidaStr
            objeto.pago = (monto, tiposPagoInt)
            crearFacturaPdf(objeto, carpetaVouchers)
            break
    espacio["carro"] = None
    indice = int(diccionario[placa][3]) - 1
    botones[indice].config(bg=colorEspacio(espacio))
    guardarBaseDatos(listaObjetos, archivoBaseDatos)
    messagebox.showinfo("Pago", f"Pago realizado correctamente. \nMonto: ₡{monto}\nTipo: {tipoPagoTexto}")
    app.destroy()
    mainApp.destroy()
