import pandas

def get_master_service(conn, id):
    df = pandas.read_sql(f'''
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
        WHERE master_service_id={id}
    )
    SELECT
        service_name,
        master_name,
        work_day_start,
        work_day_end,
        rating,
        price,
        duration
    FROM get_ms
    JOIN service USING(service_id)
    JOIN master USING(master_id)
    LEFT JOIN get_rating USING(master_service_id)
    ''', conn)
    return df

def get_review_list(conn, id):
    df = pandas.read_sql(f'''
        SELECT
            username,
            review_title,
            review_description,
            review_score
        FROM review
        JOIN service_order USING(order_id)
        JOIN client USING(client_id)
        WHERE master_service_id={id}
    ''', conn)
    return df