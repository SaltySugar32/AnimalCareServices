from app import app
from flask import render_template, session
from models.order_checkout_model import get_order_list
from utils import get_db_connection

@app.route('/order')
def order_checkout():
    con = get_db_connection()
    table = get_order_list(con, session['m_service_id'])
    html = render_template(
        'order_checkout.html', 
        title = 'Заказ',
        content = table
        )
    con.close()
    return html