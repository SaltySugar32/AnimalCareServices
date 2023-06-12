from app import app
from utils import get_db_connection
from flask import render_template
from models.about_service_model import get_master_service

@app.route('/service/<id>')
def master_service(id):
    con = get_db_connection()
    master_service = get_master_service(con, id)
    html = render_template('about_service.html', title='Услуга', content = master_service.to_html(index=False))
    con.close()
    return html  