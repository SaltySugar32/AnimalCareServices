from app import app
from utils import get_db_connection
from flask import render_template, session
from models.about_service_model import get_master_service, get_review_list
from datetime import timedelta, date

@app.route('/service/<id>')
def master_service(id):
    session['m_service_id'] = id
    con = get_db_connection()
    master_service = get_master_service(con, id)
    review_list = get_review_list(con, id)
    html = render_template(
        'about_service.html', 
        title='Услуга', 
        m_service = master_service, 
        review_list = review_list, 
        date_today = date.today(), 
        date_max = date.today() + timedelta(days=30)
    )
    con.close()
    return html  