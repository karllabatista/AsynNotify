from fastapi import FastAPI

from api_gateway.routers.users import router as router_user
from api_gateway.routers.notification import router as router_notification

app = FastAPI()

app.include_router(router_user)
app.include_router(router_notification)