import psycopg2

class c_db:
    """Mantiene y ejecuta funciones de conexión a base de datos"""
    # Esta implementación está usando mysqlclient, que es compatible con Python3 y además usa la interfaz casi idéntica a
    # la de otras librerías estándar de acceso a base de datos. Instalarla no fue nada intuitivo; básicamente, hay que instalar
    # un archivo wheel, pero en el sitio oficial de la librería, no estaba el correcto para Windows y para Python 3.7 32 bits.
    # En esta respuesta de StackOverflow está todo lo necesario para instalar de inmediato:
    # https://stackoverflow.com/a/51164104/878998
    # Página con todos los Wheel necesarios para instalar la librería:
    # https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient

    # Parámetros pueden ser leídos de un archivo de configuración en el proyecto, en vez de en duro

    def __init__(self, config):
        # Creamos la conexión
        # passwd para MySQLdb, password para psycopg2
        # db para MySQLdb, dbname para psycopg2
        self.dbconn=psycopg2.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            dbname=config['database'])
        self.dbconn.autocommit=True   # Sin un commit explícito al cerrar la conexión, o bien usar este parámetro, los INSERTS nunca se completan... En MySQL, es autocommit(True); en Postgres, es autocommit=True o bien usar conn.set_isolation_level(0) justo antes de cada sentencia que lo requiera, ver https://wiki.postgresql.org/wiki/Psycopg2_Tutorial para detalles de uso

    def exec_query_noreturn(self, query):
        """Ejecuta una query que no devuelve un recordset, como INSERT, UPDATE, etc...
        Recibe un parámetro, un diccionario con la query (stmt) y una tupla de parámetros (prms)"""
        
        c=self.dbconn.cursor()
        #dbconn.set_isolation_level(0)   # Equivalente al autocommit para MySQL (innecesario por la directiva autocommit=True)
        if 'prms' in query:
            c.execute(query['stmt'], query['prms']) # Query parametrizada
        else:
            c.execute(query['stmt'])    # Query sin parámetros
        c.close()

    def exec_query_fetchall(self, query):
        """Ejecuta una query. Devuelve una lista de tuplas con los resultados (recordset) de la query.
        query es la consulta misma, los valores a reemplazar se especifican como %s.
        values es una lista con 0 a n argumentos que serán reemplazados en los %s.
        Recibe un parámetro, un diccionario con la query (stmt) y una tupla de parámetros (prms)"""

        c=self.dbconn.cursor()
        if 'prms' in query:
            c.execute(query['stmt'], query['prms']) # Query parametrizada
        else:
            c.execute(query['stmt'])    # Query sin parámetros
        res=c.fetchall()
        c.close()
        return res

class c_filtrosquery:
    """Herramienta para construir fácilmente una cláusula WHERE para una consulta SQL,
    parametrizada. Retorna una tupla con dos elementos: la cláusula WHERE con los respectivos
    placeholders (%s) donde corresponda, y una lista con todos los respectivos parámetros.
    """

    def __init__(self):
        self.lista_clausulas = []
        self.lista_parms = []

    def agregar(self, clausula, param):
        self.lista_clausulas.append(clausula)
        self.lista_parms.append(param)

    def limpiar(self):
        self.lista_clausulas = []
        self.lista_parms = []

    def resultado(self):
        if len(self.lista_clausulas) > 0:
            clausula = " WHERE "

            for indice, elem in enumerate(self.lista_clausulas):
                if indice > 0:
                    clausula = clausula + "AND "
                clausula = clausula + elem + " "

            return (clausula, self.lista_parms)
        else:
            return ("", [])