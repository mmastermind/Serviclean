import os
#Access to mongo_db previusly configured and secret_key required for app:
MONGO_URI = 'mongodb+srv://programmer:Programmer1@bd2w-plwfv.azure.mongodb.net/bd2w'
SECRET_KEY = 'mysecret'
SECURITY_PASSWORD_SALT = 'my_precious_two'

class BaseConfig(object):
    """Base configuration."""

    # main config
#    SECRET_KEY = 'my_precious'
#    SECURITY_PASSWORD_SALT = 'my_precious_two'
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # mail settings
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    # gmail authentication
    MAIL_USERNAME = 'bdwpro'
    MAIL_PASSWORD = 'xxxx'

    # mail accounts
    MAIL_DEFAULT_SENDER = 'bd2wpro@gmail.com'