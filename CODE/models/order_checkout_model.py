import pandas
import datetime

def get_order_list(conn, m_service_id):
    df = pandas.read_sql(f"""
    SELECT *
    FROM service_order
    WHERE master_service_id = {m_service_id}
    """, conn)
    return df

def get_order_time(conn, m_service_id, date):
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

'''
def remove_conflicting_times(time_slots, order_time, delta):
    # Convert 'time' and 'order_date' columns to datetime objects
    time_slots['time'] = pandas.to_datetime(time_slots['time'], format='%H:%M:%S').dt.time
    order_time['order_date'] = pandas.to_datetime(order_time['order_date'], format='%Y-%m-%d %H:%M:%S').dt.time
    
    # Convert delta to a timedelta object
    delta = pandas.to_timedelta(delta)
    
    # Create a list of booked time slots
    booked_slots = order_time['order_date'].tolist()
    
    # Filter out conflicting time slots
    available_slots = time_slots[~time_slots['time'].isin(booked_slots)]
    
    # Convert 'time' column back to the desired format
    available_slots['time'] = available_slots['time'].apply(lambda x: x.strftime('%H:%M:%S'))
    
    return available_slots
'''

def remove_time_slots(time_slots, order_time, delta):
    # Convert time columns to datetime format
    time_slots['time'] = pandas.to_datetime(time_slots['time'])
    order_time['order_date'] = pandas.to_datetime(order_time['order_date'])

    # Add delta to order_date to get end_time
    order_time['end_time'] = order_time['order_date'] + pandas.to_timedelta(delta)

    # Iterate over each row in order_time DataFrame
    for _, row in order_time.iterrows():
        # Filter time_slots DataFrame based on the current row's order_date and end_time
        mask = (time_slots['time'] + pandas.to_timedelta(delta) <= row['order_date']) | (time_slots['time'] >= row['end_time'])
        time_slots = time_slots.loc[mask]

    return time_slots

def get_available_time(conn, m_service_id, date):
    m_service_hours = pandas.read_sql(f'''
    SELECT
        work_day_start,
        work_day_end,
        duration
    FROM master_service
    JOIN service USING(service_id)
    WHERE master_service_id = {m_service_id}
    ''', conn)

    start = m_service_hours['work_day_start'][0]
    delta = m_service_hours['duration'][0]
    end = pandas.Timestamp(m_service_hours['work_day_end'][0]) - pandas.Timedelta(delta)
    time_slots = pandas.DataFrame({'time': pandas.date_range(start, end, freq='30T').strftime('%H:%M:%S')})
    
    order_time = get_order_time(conn,m_service_id, date)
    order_time['order_date'] = pandas.to_datetime(order_time['order_date']).dt.strftime('%H:%M:%S')
   
    df = remove_time_slots(time_slots, order_time, delta)
    df['time'] = pandas.to_datetime(df['time']).dt.strftime('%H:%M:%S')

    print(df)
    return df
