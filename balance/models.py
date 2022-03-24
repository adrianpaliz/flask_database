import sqlite3

class ProcessData :
    def __init__(self, file=":memory:"):
        self.origen_datos = file

    def create_dictionary(self, cur):
        rows = cur.fetchall()

        fields  = []
        for item in cur.description:
            fields.append(item[0])

        result = []

        for row in rows:
            record = {}

            for key, value in zip(fields , row):
                record[key] = value

            result.append(record)
        return result 

    def results(self, cur, con):
 
        if cur.description:
            result = self.create_dictionary(cur)
        else:
            result = None
            con.commit()
        return result

    def haz_consulta(self, consulta, params=[]):
        con = sqlite3.connect(self.origen_datos)
        cur = con.cursor()

        cur.execute(consulta, params)

        result = self.results(cur, con)

        con.close()

        return result



    def recupera_datos(self):
        return self.haz_consulta("""
                        SELECT fecha, hora, concepto, es_ingreso, cantidad, id
                        FROM movimientos
                        ORDER BY fecha
                    """
        )


    def consulta_id(self, id):
        return self.haz_consulta("""
                        SELECT fecha, hora, concepto, es_ingreso, cantidad, id
                          FROM movimientos
                         WHERE id = ?      
                    """, (id,))



    def modifica_datos(self, params):
        self.haz_consulta("""
                    INSERT INTO movimientos (fecha, hora, concepto, es_ingreso, cantidad)
                                    values (?, ?, ?, ?, ?)
                    """, params)


    def update_datos(self, params):
        self.haz_consulta("""
                        UPDATE movimientos set fecha = ?, hora = ?, concepto = ?, es_ingreso = ?, cantidad = ?
                        WHERE id = ?
                        """, params)


