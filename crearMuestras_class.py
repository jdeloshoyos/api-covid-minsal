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

# Clase crearMuestras: gestiona la creación de una muestra a la API Minsal

import json
import requests
import re

class c_crearMuestras:
    def __init__(self, accesskey, endpoint):
        """
        Constructor de la clase. Carga las variables iniciales, y deja inicializada la variable que contendrá la respuesta a la llamada.
        """
        self.accesskey = accesskey
        self.endpoint = endpoint
        self.muestras_a_cargar = []
        self.respuesta = None

    def valida_campo(self, datos_muestra, nombre_campo, tipo_dato, num_opciones=0, patron=""):
        """
        Valida que un campo exista el en objeto de datos, y que sea del tipo especificado..
        Recibe como argumentos el objeto con los datos de la muestra a crear, y el nombre del campo a validar.
        Devuelve un string vacío si la validación es correcta, o un string con el nombre del campo y el tipo de error si no se valida.
        """
        
        if not (nombre_campo in datos_muestra):
            return "OBJETO INVÁLIDO: Campo {} no está presente\n".format(nombre_campo)

        if not(isinstance(datos_muestra[nombre_campo], tipo_dato)):
            return "OBJETO INVÁLIDO: Campo {} no es de tipo {}\n".format(nombre_campo, tipo_dato)

        if tipo_dato == int and num_opciones > 0:
            # Validación de campos estructurados que deben tener opción numérica entre 1 y num_opciones
            if datos_muestra[nombre_campo] not in range(1, num_opciones + 1):
                return "OBJETO INVÁLIDO: Campo {} fuera de rango permitido (1 a {})\n".format(nombre_campo, num_opciones)

        if tipo_dato == str and patron != "":
            # Validación de patrón requerido en campo string. patron es una expresión regular
            if re.match(patron, datos_muestra[nombre_campo]) is None:
                return "OBJETO INVÁLIDO: Campo {} no se ajusta a patrón {}\n".format(nombre_campo, patron)

        # Si llegamos aquí, pasamos todas las validaciones. Devolvemos un string vacío en ese caso.
        return ""

    def agregaMuestra(self, datos_muestra):
        """
        Agrega una muestra a enviar en la solicitud. Debe agregarse al menos una muestra antes de usar el método llamar.
        El objeto datos_muestra debe ajustarse a la definición de lo que requiere este endpoint, pero los campos
        de selección discreta se pasan como integers; es esta clase la que realiza la conversión al dato correspondiente a enviar
        al endpoint Minsal.
        Los campos del objeto son:
        {
            "codigo_muestra_cliente": (str),
            "id_laboratorio": (str) (parece referirse al código DEIS),
            "rut_responsable": (str) (formato: sin puntos, con guión y con DV),
            "cod_deis": (int),
            "rut_medico": (str) (formato: sin puntos, con guión y con DV),
            "paciente_run": (int) (sin puntos, guión ni DV),
            "paciente_dv": (int) (sólo el DV),
            "paciente_nombres": (str),
            "paciente_ap_pat": (str),
            "paciente_ap_mat": (str),
            "paciente_fecha_nac": (str) (dd-mm-aaaa),
            "paciente_comuna": (int) (código DEIS),
            "paciente_direccion": (str),
            "paciente_telefono": (str),
            "paciente_tipodoc": (int) (ESTRUCTURADO; Opciones: 1="RUN", 2="PASAPORTE", 3="SIN DOCUMENTACION"),
            "paciente_sexo": (int) (ESTRUCTURADO; Opciones: 1="M", 2="F", 3="Intersex", 4="Desconocido"),
            "paciente_prevision": (int) (ESTRUCTURADO; Opciones: 1="FONASA", 2="ISAPRE", 3="CAPREDENA", 4="SISAN", 5="SISAE", 6="DIPRECA", 7="SIN PREVISIÓN"),
            "fecha_muestra": (str) (dd-mm-aaaa),
            "tecnica_muestra": (int) (ESTRUCTURADO; Opciones: 1="RT-PCR", 2="Test Pack"),
            "tipo_muestra": (int) (ESTRUCTURADO; Opciones: 1="Lavado Broncoalveolar", 2="Esputo", 3="Aspirado Traqueal", 4="Aspirado Nasofaríngeo", 5="Tórulas Nasofaríngeas", 6="Muestra sanguínea", 7="Tejido pulmonar", 8="Saliva", 9="Otro")
        }
        Hasta donde sabemos, todos los campos parecen ser obligatorios.
        Este método valida la existencia y corrección de todos los campos a enviar.
        Retorna 0 si está todo OK, 1 si hay errores de validación, con el detalle en la propiedad self.validacion.
        """

        # Validación de datos de la muestra a crear
        patron_rut = r"^\d{4,8}-[0-9kK]$"
        patron_fecha = r"^((0[1-9]|[1-2][0-9]|3[01])-(0[13578]|1[02])|(0[1-9]|[1-2][0-9])-02|(0[1-9]|[1-2][0-9]|30)-(0[469]|11))-\d{4}$"
        self.validacion = ""

        self.validacion += self.valida_campo(datos_muestra, "codigo_muestra_cliente", str)
        self.validacion += self.valida_campo(datos_muestra, "id_laboratorio", str)
        self.validacion += self.valida_campo(datos_muestra, "rut_responsable", str, patron=patron_rut)
        self.validacion += self.valida_campo(datos_muestra, "cod_deis", int)
        self.validacion += self.valida_campo(datos_muestra, "rut_medico", str, patron=patron_rut)
        self.validacion += self.valida_campo(datos_muestra, "paciente_run", int)
        self.validacion += self.valida_campo(datos_muestra, "paciente_dv", str, patron="^[0-9kK]$")
        self.validacion += self.valida_campo(datos_muestra, "paciente_nombres", str)
        self.validacion += self.valida_campo(datos_muestra, "paciente_ap_pat", str)
        self.validacion += self.valida_campo(datos_muestra, "paciente_ap_mat", str)
        self.validacion += self.valida_campo(datos_muestra, "paciente_fecha_nac", str, patron=patron_fecha)
        self.validacion += self.valida_campo(datos_muestra, "paciente_comuna", int)
        self.validacion += self.valida_campo(datos_muestra, "paciente_direccion", str)
        self.validacion += self.valida_campo(datos_muestra, "paciente_telefono", str)
        self.validacion += self.valida_campo(datos_muestra, "paciente_tipodoc", int, num_opciones=2)
        self.validacion += self.valida_campo(datos_muestra, "paciente_sexo", int, num_opciones=4)
        self.validacion += self.valida_campo(datos_muestra, "paciente_prevision", int, num_opciones=7)
        self.validacion += self.valida_campo(datos_muestra, "fecha_muestra", str, patron=patron_fecha)
        self.validacion += self.valida_campo(datos_muestra, "tecnica_muestra", int, num_opciones=2)
        self.validacion += self.valida_campo(datos_muestra, "tipo_muestra", int, num_opciones=9)

        if self.validacion != "":
            # Hay uno o más errores de validación
            return 1

        # Campos validados. Hacemos la conversión de los campos estructurados.
        tipos_doc = {
            1: "RUN",
            2: "PASAPORTE",
            3: "SIN DOCUMENTACION"
        }

        tipos_sexo = {
            1: "M",
            2: "F",
            3: "Intersex",
            4: "Desconocido"
        }

        tipos_prevision = {
            1: "FONASA",
            2: "ISAPRE",
            3: "CAPREDENA",
            4: "SISAN",
            5: "SISAE",
            6: "DIPRECA",
            7: "SIN PREVISIÓN"
        }

        tipos_tecnicas = {
            1: "RT-PCR",
            2: "Test Pack"
        }

        tipos_muestras = {
            1: "Lavado Broncoalveolar",
            2: "Esputo",
            3: "Aspirado Traqueal",
            4: "Aspirado Nasofaríngeo",
            5: "Tórulas Nasofaríngeas",
            6: "Muestra sanguínea",
            7: "Tejido pulmonar",
            8: "Saliva",
            9: "Otro"
        }

        datos_muestra['paciente_tipodoc'] = tipos_doc[datos_muestra['paciente_tipodoc']]
        datos_muestra['paciente_sexo'] = tipos_sexo[datos_muestra['paciente_sexo']]
        datos_muestra['paciente_prevision'] = tipos_prevision[datos_muestra['paciente_prevision']]
        datos_muestra['tecnica_muestra'] = tipos_tecnicas[datos_muestra['tecnica_muestra']]
        datos_muestra['tipo_muestra'] = tipos_muestras[datos_muestra['tipo_muestra']]

        self.muestras_a_cargar.append(datos_muestra)

    def llamar(self):
        """
        Llama a la API para la creación de una nueva muestra en el sistema.
        Previo a esto, se DEBE agregar al menos una muestra con el método agregaMuestra.

        Valores de retorno:
        0 = Llamado a API REST completado correctamente (igual podría contener una respuesta de error por parte del servidor, revisar código
            200 [OK] para saber que la muestra se creó correctamente)
        1 = no hay al menos una muestra agregada para enviar, no se llamó la API REST
        2 = Llamada a la API REST falló
        """

        if len(self.muestras_a_cargar) > 0:
            # Enviamos el payload. Debe ir dentro de un array (es posible crear más de una muestra en un único request)
            try:
                self.respuesta = requests.post(
                    self.endpoint,
                    headers = {
                        'ACCESSKEY': self.accesskey,
                        'Content-Type': 'application/json'
                    },
                    json = self.muestras_a_cargar
                )

                self.codigo_respuesta = self.respuesta.status_code
                self.resultados = self.respuesta.json()  # Es un array con 1 a n objetos, uno por cada muestra que se intentó cargar.

                return 0

            except Exception as e:
                self.resultados = {'error': 'Fallo en conexión a endpoint, excepción {}'.format(e)}
                return 2

        else:
            return 1    # No se cargó ningún dato de muestra previamente
