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

# Clase devolverMuestra: Deja una muestra en estado Informado de vuelta en estado Recepcionado, permitiendo informar de nuevo
# y rectificar un resultado informado anteriormente

import json
import requests

class c_devolverMuestra:
    def __init__(self, accesskey, endpoint):
        """
        Constructor de la clase. Carga las variables iniciales, y deja inicializada la variable que contendrá la respuesta a la llamada.
        """
        self.accesskey = accesskey
        self.endpoint = endpoint
        
        self.respuesta = None

    def llamar(self, muestra_id):
        """
        Llama a la API con un ID de muestra a devolver a estado recepcionado.
        De manera interesante, es posible hacerlo con el ID Minsal de la muestra, o con el ID interno del cliente (establecimiento).
        id_muestra: (int) El ID de muestra devuelto por Minsal al usar el método crearMuestras
        codigo_muestra_cliente: (str) el ID de muestra original del establecimiento, usado en el método crearMuestras
        Por el momento, está implementado solamente con el ID Minsal (que realmente es el que se usa siempre después de crear).
        Retorna 0 si es exitoso, 1 si el argumento pasado no es un integer, 2 si falla el llamado a API REST.
        Si es exitoso, carga las variables del resultado a propiedades de la clase.
        """

        # Validación de argumentos
        if isinstance(muestra_id, int):

            try:
                self.respuesta = requests.post(
                    self.endpoint,
                    headers = {
                        'ACCESSKEY': self.accesskey
                    },
                    json = [{"id_muestra": muestra_id}]
                )
                
                self.codigo_respuesta = self.respuesta.status_code
                self.resultados = self.respuesta.json()
                
                return 0

            except Exception as e:
                self.resultados = {'error': 'Fallo en conexión a endpoint, excepción {}'.format(e)}
                return 2

        else:
            return 1

    

