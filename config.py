SQLALCHEMY_DATABASE_URI = 'mysql://wargame:wargame123@localhost:3306/wargame?charset=utf8'

SECRET_KEY = 'development-key'
SQLALCHEMY_TRACK_MODIFICATIONS = True
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
TRAP_BAD_REQUEST_ERRORS = True
SQLALCHEMY_POOL_RECYCLE = 3600
SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_TRACKABLE = True
SECURITY_PASSWORD_SALT = 'development-password-salt'
