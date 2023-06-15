from app import app
from flask import render_template, session, request, redirect, url_for
from models.order_checkout_model import get_order_list, get_available_time_slots, add_order
from models.about_service_model import get_master_service
from utils import get_db_connection

@app.route('/order', methods=['GET', 'POST'])
def order_checkout():
    m_service_id = session['m_service_id']
    date = request.values.get('order_date')
    con = get_db_connection()

    if request.method == 'POST':
        if 'client_id' in session:
            client_id = session['client']
        else:
            client_id = 21
        time = request.values.get('time')
        add_order(con, client_id, m_service_id, date, time)
        return redirect(url_for('master_service', id = m_service_id))
    
    table = get_order_list(con, m_service_id)
    time_slots = get_available_time_slots(con, m_service_id, date, step='30T')
    m_service = get_master_service(con, m_service_id)

    html = render_template(
        'order_checkout.html', 
        title = 'Заказ',
        content = table,
        date = date,
        time_slots = time_slots,
        m_service = m_service
        )
    con.close()
    return html

