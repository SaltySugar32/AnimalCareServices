from flask import Flask

app = Flask(__name__)

import controllers.index
import controllers.master_service
