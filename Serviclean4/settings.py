import os
#Access to mongo_db previusly configured and secret_key required for app:
MONGO_URI = 'mongodb+srv://programmer:Programmer1@bd2w-plwfv.azure.mongodb.net/bd2w'
SECRET_KEY = 'mysecret'
SECURITY_PASSWORD_SALT = 'my_precious_two'

#class BaseConfig(object):
#    """Base configuration."""

    # main config
#    SECRET_KEY = 'my_precious'
#    SECURITY_PASSWORD_SALT = 'my_precious_two'
#DEBUG = True
BCRYPT_LOG_ROUNDS = 13
WTF_CSRF_ENABLED = True
#DEBUG_TB_ENABLED = False
#DEBUG_TB_INTERCEPT_REDIRECTS = False

# mail settings
MAIL_SERVER = 'smtp.mailtrap.io'
print(MAIL_SERVER)
MAIL_PORT = 465
MAIL_USE_TLS = True
MAIL_USE_SSL = False

# gmail authentication
MAIL_USERNAME = 'a774df6afb105a'
MAIL_PASSWORD = '21a4071f573fdc'
#Bd2wpr@2020
# mail accounts
MAIL_DEFAULT_SENDER = 'g_cienfuegos@yahoo.com'