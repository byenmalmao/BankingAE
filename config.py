
class Config():
    SECRET_KEY = 'mysecretkey'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Bismuto888@#' 
    MYSQL_DB = 'dbbankgm'

config= {
    'development': DevelopmentConfig
}

