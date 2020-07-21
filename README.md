# IMPLEMENTACIÓN DE EJEMPLO DE CONEXIÓN Y CONSUMO DE APIs REST PARA SEGUIMIENTO Y TRAZABILIDAD DE MUESTRAS PARA SARS-COV-2 DEL MINISTERIO DE SALUD

El presente repositorio presenta una demostración de código, en Python 3, para conectarse y consumir las APIs REST que el Ministerio de Salud de Chile se encuentra preparando para efectos de informar, seguir y trazar las muestras de PCR para Coronavirus, sus proceso de laboratorio, y los resultados de las mismas, sin necesidad de llevar a cabo procesos manuales de elaboración y envío de informes, sino que por medio de una interfaz electrónica que pueda ser alimentada desde los mismos sistemas informáticos de laboratorio.

El elemento principal en este repositorio es un conjunto de *clases* que encapsulan y validan los parámetros a utilizar para cada uno de los *endpoints* expuestos en dicha API. En este momento, se encuentran implementados en este conjunto de clases los siguientes *endpoints*:

- /datosMuestraID
- ​/datosMuestraRUT
- ​/datosMuestraFECHA
- ​/crearMuestras
- ​/recepcionarMuestra
- ​/entregaResultado

El *endpoint* faltante por implementar aún es ​/cambioLaboratorio .

Se incluye un programa de prueba (api-covid-minsal.py) que muestra cómo llamar y utilizar estas clases. La implementación misma de cada clase muestra cómo se llama cada uno de los *endpoints* de la API.

[La documentación oficial de estas APIs se encuentra aquí](https://tomademuestras.apidocs.openagora.org/).

Para más contexto, dudas y discusión al respecto, [ver la publicación relacionada en el Foro de Salud Digital](https://discourse.forosaluddigital.cl/t/api-rest-minsal-para-informe-y-seguimiento-de-muestras-pcr-para-sars-cov-2).

## Requerimientos

- Python 3 (probado con Python 3.8, aunque debería funcionar perfectamente con versiones anteriores de Python 3)
- Librería "requests" para Python. Se puede instalar simplemente con:  
``pip install requests``