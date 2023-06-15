import pandas
import datetime

# для теста
def get_order_list(conn, m_service_id):
    df = pandas.read_sql(f"""
    SELECT *
    FROM service_order
    WHERE master_service_id = {m_service_id}
    ORDER BY order_date
    """, conn)
    return df

def get_order_booked_time(conn, m_service_id, date):
    df = pandas.read_sql(f'''
    WITH get_orders AS(
        SELECT *
        FROM service_order
        WHERE master_service_id = {m_service_id}
    )
    SELECT
        order_date
    FROM get_orders
    WHERE DATE(order_date) = '{date}'
    ''', conn)
    return df

def remove_time_slots(time_slots, order_time, delta):
    time_slots['time'] = pandas.to_datetime(time_slots['time'])
    order_time['order_date'] = pandas.to_datetime(order_time['order_date'])

    order_time['end_time'] = order_time['order_date'] + pandas.to_timedelta(delta)

    for _, row in order_time.iterrows():
        # Filter 
        mask = (time_slots['time'] + pandas.to_timedelta(delta) <= row['order_date']) | (time_slots['time'] >= row['end_time'])
        time_slots = time_slots.loc[mask]

    return time_slots

def get_available_time_slots(conn, m_service_id, date, step=None):
    m_service_hours = pandas.read_sql(f'''
    SELECT
        work_day_start,
        work_day_end,
        duration
    FROM master_service
    JOIN service USING(service_id)
    WHERE master_service_id = {m_service_id}
    ''', conn)

    # init time_slots
    start = m_service_hours['work_day_start'][0]
    delta = m_service_hours['duration'][0]
    end = pandas.Timestamp(m_service_hours['work_day_end'][0]) - pandas.Timedelta(delta)
    freq = step if step else pandas.Timedelta(delta)
    time_slots = pandas.DataFrame({'time': pandas.date_range(start, end, freq=freq).strftime('%H:%M:%S')})
    
    # get booked time
    order_time = get_order_booked_time(conn,m_service_id, date)
    order_time['order_date'] = pandas.to_datetime(order_time['order_date']).dt.strftime('%H:%M:%S')
   
    # remove booked slots
    df = remove_time_slots(time_slots, order_time, delta)
    df['time'] = pandas.to_datetime(df['time']).dt.strftime('%H:%M:%S')
    df = df.reset_index()
    return df

def add_order(conn, client_id, m_service_id, date, time):
    order_date = date + ' ' + time
    conn.executescript(f'''
    INSERT INTO service_order (client_id, master_service_id, order_date)
    VALUES ('{client_id}', '{m_service_id}', '{order_date}')
    ''')