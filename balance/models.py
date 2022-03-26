import sqlite3

class ProcessData:
    def __init__(self, file):
        self.data_source = file

    def create_dictionary(self, cur):
        rows = cur.fetchall()

        fields  = []
        for item in cur.description:
            fields.append(item[0])

        result = []

        for row in rows:
            record = {}

            for key, value in zip(fields, row):
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

    def make_a_query(self, query, params=[]):
        con = sqlite3.connect(self.data_source)
        cur = con.cursor()

        cur.execute(query, params)

        result = self.results(cur, con)

        con.close()

        return result

    def recover_data(self):
        return self.make_a_query("""
                        SELECT day, time, concept, type, amount, id
                        FROM movements
                        ORDER BY day
                    """
        )


    def consulta_id(self, id):
        return self.make_a_query("""
                        SELECT day, time, concept, type, amount, id
                          FROM movements
                         WHERE id = ?      
                    """, (id,))



    def modifica_datos(self, params):
        self.make_a_query("""
                    INSERT INTO movements (day, time, concept, type, amount)
                                    values (?, ?, ?, ?, ?)
                    """, params)


    def update_datos(self, params):
        self.make_a_query("""
                        UPDATE movements set day = ?, time = ?, concept = ?, type = ?, amount = ?
                        WHERE id = ?
                        """, params)


