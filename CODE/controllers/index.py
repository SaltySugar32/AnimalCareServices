from app import app
from flask import render_template
from utils import get_db_connection
from models.index_model import get_master_service_list

@app.route("/")
def index():
    con = get_db_connection()
    table = get_master_service_list(con)
    html = render_template('index.html', title='Главная', content = table.to_html(index=False))
    con.close()
    return html