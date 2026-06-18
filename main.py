from botones import construirVentanaPrincipal
from estacionamiento import denominarEspacios
from funciones import cargarBaseDatos
from funciones import reconstruirDiccionarioDesdeObjetos
from funciones import reconstruirEspaciosDesdeObjetos

def main():
    archivoBaseDatos = "baseDatosParqueo.pkl"
    carpetaVouchers = "vouchers"
    urlApiMockaroo = "https://my.api.mockaroo.com/vehiculos.json?key=5f760930"
    listaObjetos = cargarBaseDatos(archivoBaseDatos)
    diccionario = reconstruirDiccionarioDesdeObjetos(listaObjetos)
    espaciosEstacionamiento = denominarEspacios()
    espaciosEstacionamiento = reconstruirEspaciosDesdeObjetos(listaObjetos, espaciosEstacionamiento)
    construirVentanaPrincipal(diccionario, listaObjetos, espaciosEstacionamiento, archivoBaseDatos, carpetaVouchers, urlApiMockaroo)

if __name__ == "__main__":
    main()