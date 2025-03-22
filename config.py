
class Config():
    SECRET_KEY = 'mysecretkey'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '' 
    MYSQL_DB = 'fidebank'

config= {
    'development': DevelopmentConfig
}