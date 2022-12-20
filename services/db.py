import psycopg2

from services.telegram import alert_admin
from settings import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

def select(table, param=None, param_value=None):
    try:
        connection = psycopg2.connect(user=DB_USER,
                                      password=DB_PASSWORD,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_NAME)


        cursor = connection.cursor()
        if type(param).__name__ == 'list':
            cursor.execute("SELECT * from " + table + " where " + param[0] + "='" + param_value[0] + "' and " + param[1] + "='" + param_value[1] + "'")
        elif param and param_value and not type(param).__name__ == 'list':
            cursor.execute("SELECT * from " + table + " where " + param + "='" + param_value + "'")
        else:
            cursor.execute("SELECT * from " + table)
        record = cursor.fetchall()
        if len(record) == 0:
            return False
        return record

    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar com PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("SELECT ALL - Conexão com PostgreSQL fechada!")


def is_in_db(value, table):
    try:
        connection = psycopg2.connect(user=DB_USER,
                                      password=DB_PASSWORD,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_NAME)


        cursor = connection.cursor()
        cursor.execute("SELECT name from " + table + " where name='" + value + "'")
        record = cursor.fetchall()
        if len(record) == 0:
            return False
        return True

    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar com PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("SELECT - Conexão com PostgreSQL fechada!")


def is_edition_in_db(value, title):
    try:
        connection = psycopg2.connect(user=DB_USER,
                                      password=DB_PASSWORD,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_NAME)


        cursor = connection.cursor()
        cursor.execute("SELECT * from editions where identifier='" + value + "'" + " and " + "title='" + title + "'")
        record = cursor.fetchall()
        if len(record) == 0:
            return False
        return True

    except (Exception, psycopg2.Error) as error:
        print("Erro ao conectar com PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("SELECT - Conexão com PostgreSQL fechada!")


def insert_publishers(publishers):
    for publisher in publishers:
        if not is_in_db(publisher, 'publishers'):
            try:
                connection = psycopg2.connect(user=DB_USER,
                                              password=DB_PASSWORD,
                                              host=DB_HOST,
                                              port=DB_PORT,
                                              database=DB_NAME)


                cursor = connection.cursor()
                insert_query = "INSERT INTO publishers (id, name) VALUES (DEFAULT, " + "'" + publisher + "'" + ")"
                cursor.execute(insert_query)
                connection.commit()
                alert_admin(f'A editora {publisher} foi inserida no banco')
                print(f'A editora {publisher} foi inserida no banco')


            except (Exception, psycopg2.Error) as error:
                print("Erro ao conectar com PostgreSQL", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
                    print("INSERT - Conexão com PostgreSQL fechada!")
        else:
            print(f'{publisher} já existe no banco')
            continue
    return


def insert_titles(name, publisher):
    if not is_in_db(name, 'hqs'):
        try:
            connection = psycopg2.connect(user=DB_USER,
                                          password=DB_PASSWORD,
                                          host=DB_HOST,
                                          port=DB_PORT,
                                          database=DB_NAME)
            cursor = connection.cursor()
            insert_query = "INSERT INTO hqs (id, name, publisher) VALUES (DEFAULT, " + "'" + name + "'" + ", " + "'" + publisher + "'" + ")"
            cursor.execute(insert_query)
            connection.commit()
            alert_admin(f'A HQ {name} ({publisher}) foi inserida no banco')
            print(f'A HQ {name} ({publisher}) foi inserida no banco')
        except (Exception, psycopg2.Error) as error:
            print("Erro ao conectar com PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
                print("INSERT - Conexão com PostgreSQL fechada!")
    else:
        print(f'{name} já existe no banco')
    return


def update_editions(editions, title):
    connection = psycopg2.connect(user=DB_USER,
                                  password=DB_PASSWORD,
                                  host=DB_HOST,
                                  port=DB_PORT,
                                  database=DB_NAME)

    for edition in editions:
        if not is_edition_in_db(edition, title):
            try:
                cursor = connection.cursor()
                insert_query = "INSERT INTO editions (id, identifier, title) VALUES (DEFAULT, " + "'" + edition + "'" + ", " + "'" + title + "'" + ")"
                cursor.execute(insert_query)
                connection.commit()
                print(f'A edição {edition} de {title} foi inserida no banco')
            except (Exception, psycopg2.Error) as error:
                print("Erro ao conectar com PostgreSQL", error)
            finally:
                cursor.close()
        else:
            print(f'A edição {edition} de {title} já existe no banco')
            continue

    connection.close()
    print("INSERT - Conexão com PostgreSQL fechada!")
    return


#insert_publishers('marvel')
#update_editions(['1'], 'thor')