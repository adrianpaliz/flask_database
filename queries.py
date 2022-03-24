import sqlite3

con = sqlite3.connect()

cur = con.cursor()

cur.execute('''
            select day, hour, concept, income, amount
            from movements
            order by day
        ''')

cursor_instantiated = cur.fetchall()
print(cursor_instantiated)
con.close

