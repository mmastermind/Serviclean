from itsdangerous import URLSafeTimedSerializer
from Serviclean4 import app
#from .settings import BaseConfig

#imports from settings.py the mongo URI
config_object='Serviclean4.settings'
#configs the app with the previous settings and initializes it

#config_object='Serviclean4.settings'
ts = URLSafeTimedSerializer(app.config['SECRET_KEY'])

