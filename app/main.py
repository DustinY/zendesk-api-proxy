from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers.okta import okta
from routers.tickets import tickets

api_app = FastAPI()

api_app.include_router(okta.okta_router)
api_app.include_router(tickets.ticket_router)


@api_app.get("/", include_in_schema=False)
def index():
    data = {"message": "check out the docs at http://127.0.0.1:8000/docs or http://127.0.0.1:8000/redoc"}
    return JSONResponse(content=data)
