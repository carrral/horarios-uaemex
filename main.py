from sys import argv, version_info
import os
from driver import *
from algoritmo_principal import principal_semilla, principal, recursivo
from horarios import *
from lector import *
import copy

DEFAULT_CONF = "configuracion.json"

argc = len(argv)


def main(argc, argv):
    """
    Se ejecuta el programa con el comando
        $ python3 main.py  mi_config.json > resultados.txt

    o alternativamente

        $ python3 main.py > resultados.txt

    para usar el archivo de configuración por default.
    """

    if(version_info[0]==2):
        #Corriendo python 2
        print_error("Se está corriendo desde python 2.X.X, favor de actualizar a python >= 3.4")
    if argc > 1:
        conf = argv[1]

        # Verificar que existe el archivo
        if( not os.path.exists(conf)):
            print_error("No se encontró un archivo de configuración '{}' ".format(conf))
            exit(-1)

    elif argc == 1:
        conf = DEFAULT_CONF

    else:
        print_error("Exceso de argumentos")
        exit(-1)
    try:
        driver = Driver()
        driver.main(conf)

    except Exception as ex:
        print_error(ex.msg)
        exit(-1)

    C = driver.get_candidatos()
    w = driver.get_num_cursar()

    Z = list()

    if driver.get_semilla() is None:

        #Algoritmo sin semilla
        Z =  principal(C,w)

    else:

        #Algoritmo con semilla
        S = driver.get_semilla()
        Z = principal_semilla(C,S,w)

    if not Z:
        #  Si Z está vacía
        print_aviso(" No se encontraron resultados. Amplie los parámetros de la búsqueda")

    else:

        print("""
          ___________________________________________
           Se encontraron [{}] combinaciones posibles
          ___________________________________________
            """.format(len(Z)))
        for Li in Z:
            i = Z.index(Li)
            print("-> Opción {}".format(i+1))
            Li.display()


def print_error(msg):

    print("""
        ============
            ERROR
        ============

        ->{}

        """.format(msg))



def print_aviso(msg):
    print("""
        ||       ||
        || Aviso ||

        ->{}
        """.format(msg))

main(argc,argv)
