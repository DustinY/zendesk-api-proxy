import httpx
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.config import Config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

class Okta:

    @staticmethod
    def validate_remotely(token, issuer, clientId, clientSecret):
        headers = {
            'accept': 'application/json',
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded',
        }
        data = {
            'client_id': clientId,
            'client_secret': clientSecret,
            'token': token,
        }
        url = issuer + '/v1/introspect'

        response = httpx.post(url, headers=headers, data=data)

        return response.status_code == httpx.codes.OK and response.json()['active']

    @staticmethod
    def validate(token: str = Depends(oauth2_scheme)):
        res = Okta.validate_remotely(
            token,
            Config.OKTA_ISSUER,
            Config.OKTA_CLIENT_ID,
            Config.OKTA_CLIENT_SECRET
        )

        if res:
            return True
        else:
            raise HTTPException(status_code=400)

    @staticmethod
    # Call the Okta API to get an access token
    def retrieve_token(authorization, issuer, scope='zap'):
        headers = {
            'accept': 'application/json',
            'authorization': authorization,
            'cache-control': 'no-cache',
            'content-type': 'application/x-www-form-urlencoded'
        }
        data = {
            'grant_type': 'client_credentials',
            'scope': scope,
        }
        url = issuer + '/v1/token'

        response = httpx.post(url, headers=headers, data=data)

        if response.status_code == httpx.codes.OK:
            return response.json()
        else:
            raise HTTPException(status_code=400, detail=response.text)
