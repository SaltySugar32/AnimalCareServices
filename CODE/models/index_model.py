import pandas

def get_service(conn):
    return pandas.read_sql('SELECT * FROM service', conn)
