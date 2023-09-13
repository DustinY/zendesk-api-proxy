from fastapi import APIRouter, Request
from app.internal.okta.okta import Okta
from app.internal.okta.auth import OktaAuthn
from app.config import Config
import urllib

okta_router = APIRouter()

@okta_router.post("/token", include_in_schema=False)
# Get auth token endpoint
def token(request: Request):
    return Okta.retrieve_token(
        request.headers['authorization'],
        Config.OKTA_ISSUER
    )

# Below is a method of using MFA to verify login and getting the bearer tokens.
# You can also interact with the /token endpoint directly, which has a series of different requirements.
# The below flow allows for easy adaptations to implement with an Okta UI if needed in the future.

# AUTHENTICATION ENDPOINTS
@okta_router.post("/login", include_in_schema=False)
async def login(request: Request):
    okta_auth = OktaAuthn()
    data = await request.json()
    # OR
    # url = f'{Config.OKTA_DOMAIN}/api/v1/authn'
    # r = requests.post(url, json={'username': data['username'], 'password': data['password']})
    # return r.json()
    return okta_auth.authenticate(data['username'], data['password'])


@okta_router.post("/verify-mfa/{factor_id}", include_in_schema=False)
async def verify_mfa(request: Request):
    okta_auth = OktaAuthn()
    params = request.path_params
    data = await request.json()

    # OR
    # url = f"{Config.OKTA_DOMAIN}/api/v1/authn/factors/{params['factor_id']}/verify"
    # r = requests.post(url, json={
    #     'stateToken': data['stateToken],
    #     'passCode': data['passCode']
    # })
    # return r.json()

    return okta_auth.verify_mfa(params['factor_id'], data['stateToken'], data['passCode'])

    # OR
    # IF Successful
    # Return redirect to /authorize OR authorize call


# AUTHORIZATION ENDPOINTS
# If you are able to import a 3rd party libraries, you could use authlib which has a starlette client
#   Then you can use the startlet client to with `client.authorize_redirect`.
#   It will handle most of the code.
@okta_router.get('/authorize', include_in_schema=False)
def authorize(request: Request):
    okta_auth = OktaAuthn()
    redirect_uri = request.url_for("callabck")
    state = urllib.parse.urlencode(request.query_parameters) if request.query_parameters else '/'
     # session token is extracted from a valid auth response
     # Must then be added as a url param here.
    token = request.query_params.get('sessionToken')
    data = {
        'client_id': Config.OKTA_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'response_type': 'code',
        'scope': 'open_id',
        'state': state,
        'sessionToken': token
    }
    # query_params = [f'{k}={v}' for k,v in data.items]
    # qp = f'{"&".join(query_params)}'
    # url = urllib.parse.urlencode(f"{Config.OKTA_DOMAIN}/oauth2/v1/authorize?{qp}")
    # r = requests.get(url)
    # return r.json()
    return okta_auth.authorize(data)

    
# If using an authlib clinet, you could use client.authorize_access_token(reuqest) to get the tokens
# Without testing, I am not sure if okta will access the sessionToken from before and immediately
#   return the access token, of it you would still need to go through authorization_code endpoints
#   authoriation_code endpoints could be added to accommodate that.
@okta_router.get("/authorization/callback", include_in_schema=False)
def authorization_callback(request: Request):
    data = request.json()