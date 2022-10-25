import os

from fastapi import FastAPI, Depends, Security
from fastapi_auth0 import Auth0, Auth0User


auth0_domain = os.getenv('AUTH0_DOMAIN', '')
auth0_api_audience = os.getenv('AUTH0_API_AUDIENCE', '')

auth = Auth0(domain=auth0_domain, api_audience=auth0_api_audience)

app = FastAPI()


@app.get("/secure", dependencies=[Depends(auth.implicit_scheme)])
async def get_secure(user: Auth0User = Security(auth.get_user)):
    return {"message": f"{user}"}
