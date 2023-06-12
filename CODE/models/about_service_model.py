import pandas

def get_master_service(conn, id):
    print(f'SELECT * FROM master_service WHERE master_service_id={id}')
    print(pandas.read_sql(f'SELECT * FROM master_service WHERE master_service_id={id}', conn))
    return pandas.read_sql(f'SELECT * FROM master_service WHERE master_service_id={id}', conn)