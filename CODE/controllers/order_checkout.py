from app import app
from flask import render_template, session, request
from models.order_checkout_model import get_order_list, get_available_time_slots
from utils import get_db_connection

@app.route('/order')
def order_checkout():
    con = get_db_connection()
    m_service_id = session['m_service_id']
    date = request.values.get('order_date')
    table = get_order_list(con, m_service_id)
    time_slots = get_available_time_slots(con, m_service_id, date)
    html = render_template(
        'order_checkout.html', 
        title = 'Заказ',
        content = table,
        date = date,
        content2 = time_slots
        )
    con.close()
    return html