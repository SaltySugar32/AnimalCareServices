import pandas

def get_order_list(conn, m_service_id):
    df = pandas.read_sql(f"""
    SELECT *
    FROM service_order
    WHERE master_service_id = {m_service_id}
    """, conn)
    return df