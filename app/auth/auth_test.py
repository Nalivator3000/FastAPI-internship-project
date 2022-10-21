from fastapi import Depends, Security, APIRouter
from fastapi_auth0 import Auth0, Auth0User
import os

router = APIRouter(
    tags=['authentication']
)

auth = Auth0(domain=os.environ["AUTH0_DOMAIN"], api_audience=os.environ["AUTH0_API_AUDIENCE"])


@router.get("/public")
def get_public():
    return {"message": "Anonymous user"}


@router.get("/secure", dependencies=[Depends(auth.implicit_scheme)])
def get_secure(user: Auth0User = Security(auth.get_user)):
    return {"message": f"{user}"}
