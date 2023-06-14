from app import app
from utils import get_db_connection
from models.search_model import get_master_service_list, get_service_list
from flask import render_template


@app.route('/search/<id>')
def search(id):
    return    