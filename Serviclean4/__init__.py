"""
The flask application package.
"""

from flask import Flask
from .extensions import mongo

app = Flask(__name__)

#imports from settings.py the mongo URI
config_object='Serviclean_v2.settings'
#configs the app with the previous settings and initializes it
app.config.from_object(config_object)
mongo.init_app(app)

if __name__ == '__main__':
    app.run(Debug = True)

#imports the different app routes from views.py file
import Serviclean4.views
