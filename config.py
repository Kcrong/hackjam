SQLALCHEMY_DATABASE_URI = 'mysql://wargame:wargame123@localhost:3306/wargame?charset=utf8'

host = '0.0.0.0'
port = 5000
debug = False
SECRET_KEY = 'development-key'
SQLALCHEMY_TRACK_MODIFICATIONS = True
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
TRAP_BAD_REQUEST_ERRORS = True

#this is test