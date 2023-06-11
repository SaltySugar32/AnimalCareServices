import pandas as pd
import datetime as dt

def get_master_service_list(conn):
    df = pd.read_sql('''
    WITH get_rating AS(
        SELECT
            master_service_id,
            AVG(review_score) AS rating
        FROM service_order
        JOIN review USING (order_id)
        GROUP BY master_service_id
    ),
    get_ms AS(
        SELECT * 
        FROM master_service
    )
    SELECT
        master_service_id,
        service_name,
        master_name,
        work_day_start,
        work_day_end,
        rating
    FROM get_ms
    JOIN service USING(service_id)
    JOIN master USING(master_id)
    LEFT JOIN get_rating USING(master_service_id)
    ORDER BY rating DESC, service_name, master_name
    ''', conn)
    # df['work_day_start'] = pd.to_datetime(df['work_day_start']).dt.strftime('%H:%M')
    # df['work_day_end'] = pd.to_datetime(df['work_day_end']).dt.strftime('%H:%M')
    # df['rating'] = df['rating'].apply(lambda x: '-' if pd.isna(x) else round(x, 1))
    return df
