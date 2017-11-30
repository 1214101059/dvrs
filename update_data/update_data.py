import psycopg2
from flask import Flask, request, render_template, redirect
from random import randint
from comparacion import menor_mayor


app = Flask(__name__)


def insertar(num: int, num_ale: int) -> None:
    dbconfg = {'host': '127.0.0.1',
               'user': 'diana',
               'password': '123',
               'database': 'diana', }
    connection = psycopg2.connect(**dbconfg)
    resultado = menor_mayor(num, num_ale)
    _SQL = """INSERT INTO comparacion(numero, numero_aleatorio, resultado) VALUES(%s, %s, %s)"""
    cursor = connection.cursor()
    cursor.execute(_SQL, (num,
                          num_ale,
                          resultado,))
    connection.commit()
    cursor.close()
    connection.close()


@app.route('/')
def home() -> '302':
    return redirect('/entry')


@app.route('/resultados', methods=['POST'])
def do_search() -> 'html':
    numero = int(request.form['numero'])
    title = 'Este es el resultado de la comparacion:'
    num_ale = randint(1, 100)
    resultado = menor_mayor(numero, num_ale)
    insertar(numero, num_ale)
    return render_template('results.html',
                           the_title=title,
                           the_number=numero,
                           the_random_number=num_ale,
                           the_result=resultado)


@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Bienvenido a mi pagina web')


@app.route('/delete', methods=['POST'])
def delete_data() -> 'html':
    params = {'host': '127.0.0.1',
              'user': 'diana',
              'password': '123',
              'database': 'diana', }
    iden = request.form['id']
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur.execute("DELETE FROM comparacion WHERE id = %s", (iden,))
    conn.commit()
    cur.close()
    conn.close()
    return render_template('entry.html')


@app.route('/registros')
def view_data() -> 'html':
    params = {'host': '127.0.0.1',
              'user': 'diana',
              'password': '123',
              'database': 'diana', }
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    cur2 = conn.cursor()
    _sql = """SELECT id, numero, numero_aleatorio, resultado FROM comparacion ORDER BY id"""
    _sql2 = """SELECT id FROM comparacion ORDER BY id"""
    cur.execute(_sql)
    cur2.execute(_sql2)
    rows = cur.fetchall()
    rows2 = cur2.fetchall()
    contents = []
    contentsid = []
    for row in rows:
        contents.append(row)
    for iden in rows2:
        contentsid.append(iden)
    cur.close()
    cur2.close()
    conn.close()
    titles = ('Id', 'Numero', 'Numero aleatorio', 'Resultado')
    return render_template('datos.html',
                           the_title='Vista de la informacion',
                           the_row_titles=titles,
                           the_data=contents,
                           ids=contentsid,)


@app.route('/modificar', methods=['POST'])
def modificar() -> 'html':
    params = {'host': '127.0.0.1',
              'user': 'diana',
              'password': '123',
              'database': 'diana', }
    conn = psycopg2.connect(**params)
    iden = request.form['iden']
    cur = conn.cursor()
    cur.execute("SELECT id, numero, numero_aleatorio FROM comparacion WHERE id = %s", (iden,))
    rows = cur.fetchall()
    contents = []
    for row in rows:
        contents.append(row)
    id = contents[0][0]
    numero = contents[0][1]
    numero_aleatorio = contents[0][2]
    print(id, numero, numero_aleatorio)
    cur.close()
    conn.close()
    titles = ('Id', 'Numero', 'Numero aleatorio', 'Resultado')
    return render_template('modificar.html',
                           the_title='Mofique los datos deseados',
                           the_row_titles=titles,
                           the_id=id,
                           the_num=numero,
                           the_rand_num=numero_aleatorio,)


@app.route('/update', methods=['POST'])
def update() -> 'html':
    params = {'host': '127.0.0.1',
              'user': 'diana',
              'password': '123',
              'database': 'diana', }
    conn = psycopg2.connect(**params)
    iden = request.form['id']
    num = int(request.form['numero'])
    num_ale = int(request.form['numero_ale'])
    resultado = menor_mayor(num, num_ale)
    cur = conn.cursor()
    sql = """UPDATE comparacion
                    set numero = %s, numero_aleatorio = %s, resultado = %s
                    WHERE  id = %s"""
    cur.execute(sql, (num, num_ale, resultado, iden,))
    conn.commit()
    cur.close()
    conn.close()
    return render_template('entry.html')


app.run(debug=True)
