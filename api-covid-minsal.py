#!/usr/bin/python3
# Encoding: UTF-8

# Integración a APIs REST de Minsal para trazabilidad de muestras PCR para SARS-CoV-2
# 2020 por Jaime de los Hoyos M.
# Departamento de Informática Biomédica, Clínica Alemana de Santiago
#
# Este software se distribuye libremente para su uso por cualquier interesado, bajo la licencia
# Apache 2.0, de acuerdo a los siguientes términos:
#
#   Copyright 2020 Clínica Alemana de Santiago
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import json
import sys
import argparse
from crearMuestras_class import c_crearMuestras
from recepcionarMuestra_class import c_recepcionarMuestra
from entregaResultado_class import c_entregaResultado
from datosMuestraID_class import c_datosMuestraID
from datosMuestraRUT_class import c_datosMuestraRUT
from datosMuestraFECHA_class import c_datosMuestraFECHA

#############################################################
# FUNCIONES WRAPPER PARA EL LLAMADO A CLASES DE INTEGRACIÓN #
#############################################################

def crear(argumento, endpoint, config_entorno):
    """
    Wrapper para la creación de una muestra
    """

    o_crear = c_crearMuestras(config_entorno['accesskey'], config_entorno['dominio'] + endpoint)
    
    # Cargamos datos para la nueva muestra
    try:
        with open('nueva_muestra.json', 'r', encoding='utf-8') as json_file:
            datos_muestra = json.load(json_file)
    except:
        print("ERROR: No se pudo abrir el archivo de nueva muestra nueva_muestra.json")
        sys.exit(1)

    try:
        with open('nueva_muestra_2.json', 'r', encoding='utf-8') as json_file:
            datos_muestra_2 = json.load(json_file)
    except:
        print("ERROR: No se pudo abrir el archivo de nueva muestra nueva_muestra_2.json")
        sys.exit(1)

    # Cargamos los datos de muestra
    n = o_crear.agregaMuestra(datos_muestra)
    if n == 1:
        # Error en los datos para creación de la muestra
        print("ERROR: Error de validación de los datos de la muestra en nueva_muestra.json:")
        print(o_crear.validacion)

    n = o_crear.agregaMuestra(datos_muestra_2)
    if n == 1:
        # Error en los datos para creación de la muestra
        print("ERROR: Error de validación de los datos de la muestra en nueva_muestra_2.json:")
        print(o_crear.validacion)
        
    creacion = o_crear.llamar()
    if creacion == 0:
        # Éxito
        print("Código de respuesta: {}".format(o_crear.codigo_respuesta))
        if o_crear.codigo_respuesta == 200:
            # Recuperamos datos para los ID de muestra creados
            for res in o_crear.resultados:
                print("\nNUEVA MUESTRA CREADA")
                print("--------------------")
                print("ID Minsal de muestra : {}".format(res['id_muestra']))
                print("ID local de muestra  : {}".format(res['codigo_muestra_cliente']))
        else:
            # Se contactó a la API REST, pero la respuesta fue distinta a 200
            print("ERROR: Ocurrió el siguiente error al intentar crear la muestra:")
            print(o_crear.resultados)

    else:
        # Error
        print("Error al llamar al servicio...")
        if creacion == 1:
            # No se cargó ningún dato de muestra
            print("ERROR: No se cargó ningún dato de nueva muestra antes de llamar al servicio")
        elif creacion == 2:
            # Error de conexión a servicio
            print(o_crear.respuesta)
            print(o_crear.respuesta.text)

def recepcionar(argumento, endpoint, config_entorno):
    """
    Wrapper para la recepción de una muestra
    """

    o_crear = c_recepcionarMuestra(config_entorno['accesskey'], config_entorno['dominio'] + endpoint)

    creacion = o_crear.llamar(int(argumento))
    if creacion == 0:
        # Éxito
        print("Código de respuesta: {}".format(o_crear.codigo_respuesta))
        if o_crear.codigo_respuesta == 200:
            # Recuperamos datos para este ID de muestra
            print("\nMUESTRA RECEPCIONADA")
            print("--------------------")
            print("ID Minsal de muestra : {}".format(o_crear.resultados['id_muestra']))
            print("ID local de muestra  : {}".format(o_crear.resultados['codigo_muestra_cliente']))
        else:
            # Se contactó a la API REST, pero la respuesta fue distinta a 200
            print("ERROR: Ocurrió el siguiente error al intentar recepcionar la muestra:")
            print(o_crear.resultados)

    else:
        # Error
        print("Error al llamar al servicio...")
        if creacion == 1:
            # Error de validacion
            print("El argumento pasado para llamar al servicio no es correcto.")
        elif creacion == 2:
            # Error de conexión a servicio
            print(o_crear.respuesta)
            print(o_crear.respuesta.text)

def resultado(argumento, endpoint, config_entorno):
    """
    Wrapper para el informe de resultados de una muestra
    """

    o_crear = c_entregaResultado(config_entorno['accesskey'], config_entorno['dominio'] + endpoint)

    argumentos = argumento.split(",")

    creacion = o_crear.llamar(int(argumentos[0]), int(argumentos[1]))
    if creacion == 0:
        # Éxito
        print("Código de respuesta: {}".format(o_crear.codigo_respuesta))
        if o_crear.codigo_respuesta == 200:
            # Recuperamos datos para este ID de muestra
            print("\nMUESTRA CON RESULTADO ENTREGADO")
            print("-------------------------------")
        else:
            # Se contactó a la API REST, pero la respuesta fue distinta a 200
            print("ERROR: Ocurrió el siguiente error al intentar recepcionar la muestra:")
            print(o_crear.resultados)

    else:
        # Error
        print("Error al llamar al servicio...")
        if creacion == 1:
            # Error de validacion
            print("El argumento pasado para llamar al servicio no es correcto.")
        elif creacion == 2:
            # Error de conexión a servicio
            print(o_crear.respuesta)
            print(o_crear.respuesta.text)

def datos_id(argumento, endpoint, config_entorno):
    """
    Wrapper para obtener datos de una muestra por su ID Minsal
    """

    o_datos = c_datosMuestraID(config_entorno['accesskey'], config_entorno['dominio'] + endpoint)

    creacion = o_datos.llamar(int(argumento))
    if creacion == 0:
        # Éxito
        print("Código de respuesta: {}".format(o_datos.codigo_respuesta))
        if o_datos.codigo_respuesta == 200:
            # Recuperamos datos para este ID de muestra
            print("\nDATOS DE LA MUESTRA")
            print("-------------------")
            print("ID Minsal de muestra                   : {}".format(o_datos.resultados['id_muestra']))
            print("Estado de muestra en sistema           : {}".format(o_datos.resultados['estado_muestra']))
            print("Profesional que tomó la muestra        : {}".format(o_datos.resultados['nombre_profesional']))
            print("RUT de profesional que tomó la muestra : {}".format(o_datos.resultados['rut_profesional']))
            print("Establecimiento                        : {}".format(o_datos.resultados['establecimiento_toma_muestra']))
            print("Médico de indicación                   : {}".format(o_datos.resultados['rut_medico_toma_muestra']))
            print("Fecha                                  : {}".format(o_datos.resultados['fecha_muestra']))
            print("Técnica                                : {}".format(o_datos.resultados['tecnica_muestra']))
            print("Tipo                                   : {}".format(o_datos.resultados['tipo_muestra']))
            print("Laboratorio                            : {}".format(o_datos.resultados['laboratorio']))
            print("\nDATOS DEL PACIENTE")
            print("------------------")
            print("Documento            : {}".format(o_datos.resultados['id_paciente']))
            print("Tipo de documento    : {}".format(o_datos.resultados['paciente_tipodoc']))
            print("Nombre               : {}".format(o_datos.resultados['nombre_paciente']))
            print("Apellido paterno     : {}".format(o_datos.resultados['apellido_paterno_paciente']))
            print("Apellido materno     : {}".format(o_datos.resultados['apellido_materno_paciente']))
            print("Fecha de nacimiento  : {}".format(o_datos.resultados['fecha_nacimiento']))
            print("Comuna de residencia : {}".format(o_datos.resultados['comuna']))
            print("Dirección            : {}".format(o_datos.resultados['paciente_direccion']))
            print("Teléfono             : {}".format(o_datos.resultados['paciente_telefono']))
            print("Nacionalidad         : {}".format(o_datos.resultados['pais']))
            print("Sexo                 : {}".format(o_datos.resultados['paciente_sexo']))
            print("Es FONASA?           : {}".format(o_datos.resultados['paciente_es_fonasa']))
            print("Previsión            : {}".format(o_datos.resultados['paciente_prevision']))
        else:
            # Se contactó a la API REST, pero la respuesta fue distinta a 200
            print("ERROR: Ocurrió el siguiente error al intentar crear la muestra:")
            print(o_datos.resultados)

    else:
        # Error
        print("Error al llamar al servicio...")
        if creacion == 1:
            # Error de validacion
            print("El argumento pasado para llamar al servicio no es correcto.")
        elif creacion == 2:
            # Error de conexión a servicio
            print(o_datos.respuesta)
            print(o_datos.respuesta.text)

def datos_rut(argumento, endpoint, config_entorno):
    """
    Wrapper para obtener datos de una muestra por su ID Minsal
    """

    o_datos = c_datosMuestraRUT(config_entorno['accesskey'], config_entorno['dominio'] + endpoint)

    creacion = o_datos.llamar(argumento)
    if creacion == 0:
        # Éxito
        print("Código de respuesta: {}".format(o_datos.codigo_respuesta))
        print("Mostrando {} resultados de muestras para el paciente con RUT {}".format(len(o_datos.resultados), args.argumento))
        if o_datos.codigo_respuesta == 200:
            # Recuperamos datos para este ID de muestra
            # En el caso de la búsqueda de RUT, pueden haber más de un resultado, por lo que iteramos sobre la lista devuelta
            for idx, i in enumerate(o_datos.resultados):
                print("\n--- Resultado {} ---".format(idx + 1))
                print("\nDATOS DE LA MUESTRA")
                print("-------------------")
                print("ID Minsal de muestra                   : {}".format(i['id_muestra']))
                print("Estado de muestra en sistema           : {}".format(i['estado_muestra']))
                print("Profesional que tomó la muestra        : {}".format(i['nombre_profesional']))
                print("RUT de profesional que tomó la muestra : {}".format(i['rut_profesional']))
                print("Establecimiento                        : {}".format(i['establecimiento_toma_muestra']))
                print("Médico de indicación                   : {}".format(i['rut_medico_toma_muestra']))
                print("Fecha                                  : {}".format(i['fecha_muestra']))
                print("Técnica                                : {}".format(i['tecnica_muestra']))
                print("Tipo                                   : {}".format(i['tipo_muestra']))
                print("Laboratorio                            : {}".format(i['laboratorio']))
                print("\nDATOS DEL PACIENTE")
                print("------------------")
                print("Documento            : {}".format(i['id_paciente']))
                print("Tipo de documento    : {}".format(i['paciente_tipodoc']))
                print("Nombre               : {}".format(i['nombre_paciente']))
                print("Apellido paterno     : {}".format(i['apellido_paterno_paciente']))
                print("Apellido materno     : {}".format(i['apellido_materno_paciente']))
                print("Fecha de nacimiento  : {}".format(i['fecha_nacimiento']))
                print("Comuna de residencia : {}".format(i['comuna']))
                print("Dirección            : {}".format(i['paciente_direccion']))
                print("Teléfono             : {}".format(i['paciente_telefono']))
                print("Nacionalidad         : {}".format(i['pais']))
                print("Sexo                 : {}".format(i['paciente_sexo']))
                print("Es FONASA?           : {}".format(i['paciente_es_fonasa']))
                print("Previsión            : {}".format(i['paciente_prevision']))
        else:
            # Se contactó a la API REST, pero la respuesta fue distinta a 200
            print("ERROR: Ocurrió el siguiente error al intentar crear la muestra:")
            print(o_datos.resultados)

    else:
        # Error
        print("Error al llamar al servicio...")
        if creacion == 1:
            # Error de validacion
            print("El argumento pasado para llamar al servicio no es correcto.")
        elif creacion == 2:
            # Error de conexión a servicio
            print(o_datos.respuesta)
            print(o_datos.respuesta.text)

def datos_fecha(argumento, endpoint, config_entorno):
    """
    Wrapper para obtener datos de una muestra por su ID Minsal
    """

    o_datos = c_datosMuestraFECHA(config_entorno['accesskey'], config_entorno['dominio'] + endpoint)

    argumentos = argumento.split(",")

    creacion = o_datos.llamar(str(argumentos[0]), int(argumentos[1]))
    if creacion == 0:
        # Éxito
        print("Código de respuesta: {}".format(o_datos.codigo_respuesta))
        print("Mostrando {} resultados de muestras para el paciente en fecha {} y estado {}".format(len(o_datos.resultados), argumentos[0], argumentos[1]))
        if o_datos.codigo_respuesta == 200:
            # Recuperamos datos para este ID de muestra
            # En el caso de la búsqueda de RUT, pueden haber más de un resultado, por lo que iteramos sobre la lista devuelta
            for idx, i in enumerate(o_datos.resultados):
                print("\n--- Resultado {} ---".format(idx + 1))
                print("\nDATOS DE LA MUESTRA")
                print("-------------------")
                print("ID Minsal de muestra                   : {}".format(i['id_muestra']))
                print("Estado de muestra en sistema           : {}".format(i['estado_muestra']))
                print("Profesional que tomó la muestra        : {}".format(i['nombre_profesional']))
                print("RUT de profesional que tomó la muestra : {}".format(i['rut_profesional']))
                print("Establecimiento                        : {}".format(i['establecimiento_toma_muestra']))
                print("Médico de indicación                   : {}".format(i['rut_medico_toma_muestra']))
                print("Fecha                                  : {}".format(i['fecha_muestra']))
                print("Técnica                                : {}".format(i['tecnica_muestra']))
                print("Tipo                                   : {}".format(i['tipo_muestra']))
                print("Laboratorio                            : {}".format(i['laboratorio']))
                print("\nDATOS DEL PACIENTE")
                print("------------------")
                print("Documento            : {}".format(i['id_paciente']))
                print("Tipo de documento    : {}".format(i['paciente_tipodoc']))
                print("Nombre               : {}".format(i['nombre_paciente']))
                print("Apellido paterno     : {}".format(i['apellido_paterno_paciente']))
                print("Apellido materno     : {}".format(i['apellido_materno_paciente']))
                print("Fecha de nacimiento  : {}".format(i['fecha_nacimiento']))
                print("Comuna de residencia : {}".format(i['comuna']))
                print("Dirección            : {}".format(i['paciente_direccion']))
                print("Teléfono             : {}".format(i['paciente_telefono']))
                print("Nacionalidad         : {}".format(i['pais']))
                print("Sexo                 : {}".format(i['paciente_sexo']))
                print("Es FONASA?           : {}".format(i['paciente_es_fonasa']))
                print("Previsión            : {}".format(i['paciente_prevision']))
        else:
            # Se contactó a la API REST, pero la respuesta fue distinta a 200
            print("ERROR: Ocurrió el siguiente error al intentar crear la muestra:")
            print(o_datos.resultados)

    else:
        # Error
        print("Error al llamar al servicio...")
        if creacion == 1:
            # Error de validacion
            print("El argumento pasado para llamar al servicio no es correcto.")
        elif creacion == 2:
            # Error de conexión a servicio
            print(o_datos.respuesta)
            print(o_datos.respuesta.text)

####################
# PUNTO DE ENTRADA #
####################

# Parseo de argumentos
parser = argparse.ArgumentParser(description='Programa de demostración de conexión a API de trazabilidad de muestras Covid Minsal')
parser.add_argument('accion', action='store', type=str, metavar='accion_a_realizar', choices=[
    'crear', 'recepcionar', 'resultado', 'datos_id', 'datos_rut', 'datos_fecha'])
parser.add_argument('argumento', action='store', type=str, metavar='argumento_para_accion')
parser.add_argument('-c', '--config', action='store', default='config.json', type=str, metavar='archivo_configuracion.json')
args = parser.parse_args()

# Cargamos el archivo de configuración
try:
    with open(args.config, 'r', encoding='utf-8') as json_file:
        config = json.load(json_file)
except:
    print("ERROR: No se pudo abrir el archivo de configuración " + args.config)
    sys.exit(1)

print("Conexión a API REST Trazabilidad de muestras Covid Minsal")
print("2020 por Clínica Alemana de Santiago\n")

print("Usando configuración de entorno '{}'\n".format(config['entorno']))

# Cargamos los datos del entorno seleccionado en la configuración
try:
    config_entorno = next(x for x in config['entornos'] if x['nombre'] == config['entorno'])
except:
    print("ERROR: La configuración no contiene datos para el entorno '{}'".format(config['entorno']))
    sys.exit(1)

# Modos de operación. Determinan la API REST a utilizar.
modos_op = {
    "crear": {
        "nombre": "Crear nueva muestra",
        "endpoint": config['endpoints']['crearMuestra'],
        "funcion": crear
    },
    "recepcionar": {
        "nombre": "Recepcionar muestra en laboratorio",
        "endpoint": config['endpoints']['recepcionarMuestra'],
        "funcion": recepcionar
    },
    "resultado": {
        "nombre": "Informar resultado para una muestra",
        "endpoint": config['endpoints']['entregaResultado'],
        "funcion": resultado
    },
    "datos_id": {
        "nombre": "Obtener datos de muestra por ID",
        "endpoint": config['endpoints']['datosMuestraID'],
        "funcion": datos_id
    },
    "datos_rut": {
        "nombre": "Obtener datos de muestra por RUT",
        "endpoint": config['endpoints']['datosMuestraRUT'],
        "funcion": datos_rut
    },
    "datos_fecha": {
        "nombre": "Obtener datos de muestra por fecha y estado de muestra",
        "endpoint": config['endpoints']['datosMuestraFECHA'],
        "funcion": datos_fecha
    }
}

print("Modo de operación: {}, con argumento: {}\n".format(modos_op[args.accion]['nombre'], args.argumento))
modos_op[args.accion]['funcion'](args.argumento, modos_op[args.accion]['endpoint'], config_entorno)