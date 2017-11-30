import psycopg2


def modificar():
    params = {'host': '127.0.0.1',
              'user': 'diana',
              'password': '123',
              'database': 'diana', }
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute("SELECT id, numero, numero_aleatorio FROM comparacion WHERE id = 3")
    rows = cur.fetchall()
    contents = []
    for row in rows:
        contents.append(row)
    id = contents[0][0]
    numero = contents[0][1]
    numero_aleatorio = contents[0][2]
    print(id, numero, numero_aleatorio)


modificar()
