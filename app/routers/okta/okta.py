from fastapi import APIRouter, Request
from internal.okta.okta import Okta
from config import Config

okta_router = APIRouter()

@okta_router.post("/token", include_in_schema=False)
# Get auth token endpoint
def login(request: Request):
    return Okta.retrieve_token(
        request.headers['authorization'],
        Config.OKTA_ISSUER
    )