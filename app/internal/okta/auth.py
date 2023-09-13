import requests
from app.config import Config
import urllib

class OktaAuthn:

    def authenticate(self, username: str, password: str):
        url = f'{Config.OKTA_DOMAIN}/api/v1/authn'
        r = requests.post(url, json={'username': username, 'password': password})
        return r.json()

    def verify_mfa(self, factor_id: str, state_token: str, passcode: str):
        url = f'{Config.OKTA_DOMAIN}/api/v1/authn/factors/{factor_id}/verify'
        r = requests.post(url, json={
            'stateToken': state_token,
            'passCode': passcode
        })
        return r.json()
    
    def authorize(self, data):
        query_params = [f'{k}={v}' for k,v in data.items]
        qp = f'{"&".join(query_params)}'
        url = urllib.parse.urlencode(f"{Config.OKTA_DOMAIN}/oauth2/v1/authorize?{qp}")
        r = requests.get(url)
        return r.json()