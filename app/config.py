from decouple import config

class Config(object):

    OKTA_DOMAIN = config('OKTA_DOMAIN', cast=str)
    OKTA_CLIENT_ID = config('OKTA_CLIENT_ID', cast=str)
    OKTA_CLIENT_SECRET = config('OKTA_CLIENT_SECRET', cast=str)
    OKTA_ISSUER = config('OKTA_ISSUER', cast=str)
    OKTA_AUDIENCE = config('OKTA_AUDIENCE', cast=str)
    ZAP_API_USER = config('ZAP_API_USER', cast=str)
    ZAP_API_TOKEN = config('ZAP_API_TOKEN', cast=str)
    ZAP_OAUTH_CLIENT_SECRET = config('ZAP_OAUTH_CLIENT_SECRET', cast=str)
    ZENDESK_DOMAIN = config('ZENDESK_DOMAIN', cast=str)
