import ssl

## Server configurations
#
class DevelopmentConfig(object):
    SERVER_NAME = "127.0.0.1:8080"
    DEBUG = True
    SSL_CERTIFICATE = '/etc/letsencrypt/live/api.cipherbytesdb.com/fullchain.pem'
    SSL_PRIVATE_KEY = '/etc/letsencrypt/live/api.cipherbytesdb.com/privkey.pem'
    SSL_TLS_VERSION = ssl.PROTOCOL_TLS
