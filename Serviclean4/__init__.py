"""
The flask application package.
"""

from flask import Flask
from flask_mail import Mail
from .extensions import mongo
from .extensions import login_manager

mail = Mail()

app = Flask(__name__)

#imports from settings.py the mongo URI
config_object='Serviclean4.settings'
#configs the app with the previous settings and initializes it
app.config.from_object(config_object)
mongo.init_app(app)

if __name__ == '__main__':
    app.run(Debug = True)

#imports the different app routes from views.py file
login_manager.init_app(app)
mail.init_app(app)

import Serviclean4.views