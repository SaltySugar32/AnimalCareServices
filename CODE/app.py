from flask import Flask

app = Flask(__name__)
app.secret_key = b'supersecretkey'

import controllers.index
import controllers.about_service
import controllers.order_checkout
