from app import app
from flask import render_template
from utils import get_db_connection

con = get_db_connection()

@app.route("/")
def index():
    html = render_template('index.html', title='Главная', content = 'test')
    return html