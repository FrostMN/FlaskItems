import os

_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# Database Config
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_USER = "inv_items_user"
MYSQL_PASSWORD = "(8tEH3gfGfTJEotxufYouEpgIr2SlM5sKrFZbPtEtxRKFUGwkfE3tM5clwf1m5Ms)"
MYSQL_DB = "inv_items"
MYSQL_TEMPLATE = "mysql://{}:{}@{}:{}/{}"

MYSQL_CONN = MYSQL_TEMPLATE.format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

# # Mail Config
# MAIL_SERVER = 'smtp.gmail.com'
# MAIL_PORT = 587
# MAIL_USE_TLS = True
# # MAIL_USE_SSL = True
# # MAIL_DEBUG = app.debug
# MAIL_USERNAME = 'account@gmail.com'
# MAIL_PASSWORD = 'GmailPassword'
# MAIL_DEFAULT_SENDER = "account@gmail.com"
# # MAIL_MAX_EMAILS = None
# # MAIL_SUPPRESS_SEND = app.testing
# MAIL_ASCII_ATTACHMENTS = False

# User API URL
USER_PORT = "8085"
USER_HOST = "localhost"
USER_TEMPLATE = "http://{}:{}"
USER_URL = USER_TEMPLATE.format(USER_HOST, USER_PORT)

del os

if __name__ == '__main__':
    print(MYSQL_CONN)