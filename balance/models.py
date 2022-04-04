import sqlite3

class ProcessData:
    def __init__(self, file=":memory:"):
        self.data_source = file

    def create_dictionary(self, cur):
        rows = cur.fetchall()

        fields = []
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
                                    SELECT day, hour, concept, income, amount, id
                                    FROM movements
                                    ORDER BY day
                                """)

    def consult_id(self, variable_id):
        return self.make_a_query("""
                                    SELECT day, hour, concept, income, amount, id
                                    FROM movements
                                    WHERE id = ?      
                                """,(variable_id,))

    def edit_data(self, params):
        self.make_a_query("""
                            INSERT INTO movements (day, hour, concept, income, amount)
                                            values (?, ?, ?, ?, ?)
                        """,params)

    def update_data(self, params):
        self.make_a_query("""
                            UPDATE movements set day = ?, hour = ?, concept = ?, income = ?, amount = ?
                            WHERE id = ?
                        """,params)