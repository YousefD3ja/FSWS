from Site import env_var

class Config:

    SECRET_KEY = env_var.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = env_var["DB"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.google.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = env_var.get("EMAIL")
    MAIL_PASSWORD = env_var.get("APP_PWD")
    MAIL_DEFAULT_SENDER = env_var.get('MAIL_DEFAULT_SENDER')