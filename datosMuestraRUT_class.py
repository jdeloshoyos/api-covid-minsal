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

# Clase datosMuestraRUT: Obtiene los datos de muestras por RUT del paciente (pueden ser varias)

import json
import requests

class c_datosMuestraRUT:
    def __init__(self, accesskey, endpoint):
        """
        Constructor de la clase. Carga las variables iniciales, y deja inicializada la variable que contendrá la respuesta a la llamada.
        """
        self.accesskey = accesskey
        self.endpoint = endpoint
        
        self.respuesta = None

    def llamar(self, rut_paciente):
        """
        Llama a la API con un RUT de paciente a consultar.
        rut_paciente: (str) El RUT del paciente, sin puntos, con guión y con dígito verificador (ej.: "22222222-2")
        Retorna 0 si es exitoso, 1 si el argumento pasado no es un string, 2 si falla el llamado a API REST.
        Si es exitoso, carga las variables del resultado a propiedades de la clase.
        """

        if isinstance(rut_paciente, str):
            parametros = json.dumps({"rut_paciente": rut_paciente})
            
            try:
                self.respuesta = requests.post(
                    self.endpoint,
                    headers = {
                        'ACCESSKEY': self.accesskey
                    },
                    data = {
                        'parametros': parametros
                    }
                )

                self.codigo_respuesta = self.respuesta.status_code
                self.resultados = self.respuesta.json()  # Es un array, que podría tener de 0 a n elementos 

                return 0

            except Exception as e:
                self.resultados = {'error': 'Fallo en conexión a endpoint, excepción {}'.format(e)}
                return 2

        else:
            return 1

    

