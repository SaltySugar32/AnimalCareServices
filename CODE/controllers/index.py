from app import app
from flask import render_template, session, request
from utils import get_db_connection
from models.index_model import get_master_service_list, get_service_list

@app.route("/")
def index():
    
    if(request.values.get('service')):
        service_id = request.values.get('service')
    else:
        service_id = 1
    con = get_db_connection()
    service_list = get_service_list(con)
    table = get_master_service_list(con, service_id)
    html = render_template(
        'index.html', 
        title='Главная',
        service_list = service_list,
        service_id = service_id,
        m_service_list = table
    )
    con.close()
    return html