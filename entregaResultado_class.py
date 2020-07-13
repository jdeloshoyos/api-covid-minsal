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

# Clase entregaResultado: gestiona la entrega de resultado final de una muestra por parte del laboratorio (paso de estado 3 a 4)

import json
import requests

class c_entregaResultado:
    def __init__(self, accesskey, endpoint):
        """
        Constructor de la clase. Carga las variables iniciales, y deja inicializada la variable que contendrá la respuesta a la llamada.
        """
        self.accesskey = accesskey
        self.endpoint = endpoint
        
        self.respuesta = None

    def llamar(self, muestra_id, resultado):
        """
        Llama a la API con un ID de muestra a entregar resultado.
        muestra_id: (int) El ID de muestra devuelto por Minsal al usar el método crearMuestras
        Retorna 0 si es exitoso, 1 si el argumento pasado no es un integer, 2 si falla el llamado a API REST.
        Opcionalmente, este método puede pasar un archivo binario con informe del resultado; en este momento, esa función
        no está implementada en esta clase.
        Si es exitoso, carga las variables del resultado a propiedades de la clase.
        """

        tipos_resultado = {
            1: "Positivo",
            2: "Negativo",
            3: "Indeterminado",
            4: "Muestra no apta"
        }

        # Validación de argumentos
        if isinstance(resultado, int):
            if not resultado in range(1, len(tipos_resultado) + 1):
                return 1
        else:
            return 1

        if isinstance(muestra_id, int):
            parametros = json.dumps({"id_muestra": muestra_id, "resultado": tipos_resultado[resultado]})

            try:
                self.respuesta = requests.post(
                    self.endpoint,
                    headers = {
                        'ACCESSKEY': self.accesskey
                    },
                    data = {
                        "parametros": parametros
                    },
                    files = {
                        'upfile': ('resultado.txt', tipos_resultado[resultado])
                    }
                )

                self.codigo_respuesta = self.respuesta.status_code
                self.resultados = self.respuesta.json()[0]  # Viene como un array con 0 a 1 único elemento

                return 0

            except Exception as e:
                self.resultados = {'error': 'Fallo en conexión a endpoint, excepción {}'.format(e)}
                return 2

        else:
            return 1

    

