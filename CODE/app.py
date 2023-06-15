from flask import Flask, session

app = Flask(__name__)
app.secret_key = b'supersecretkey'

# без учеток пока


import controllers.index
import controllers.about_service
import controllers.order_checkout