import pandas

def get_master_service_list(conn):
    return pandas.read_sql('SELECT * FROM master_service', conn)
