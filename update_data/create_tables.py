import psycopg2


def create_tables():

    """Create tabless in the Postgresql database"""

    command = ("""CREATE TABLE comparacion(
                  id SERIAL PRIMARY KEY,
                  numero VARCHAR(128) NOT NULL,
                  numero_aleatorio VARCHAR(128) NOT NULL,
                  resultado VARCHAR(128) NOT NULL)""")

    connection = None
    try:
        # read the connection parameters
        dbconfg = {'host': '127.0.0.1',
                   'user': 'diana',
                   'password': '123',
                   'database': 'diana', }
        connection = psycopg2.connect(**dbconfg)
        cursor = connection.cursor()
        # Create table one by one
        cursor.execute(command)
        # close communication with the PostgreSQLdatabase server
        cursor.close()
        # commit the changes
        connection.commit()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()


if __name__ == '__main__':
    create_tables()
