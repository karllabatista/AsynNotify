from fastapi import FastAPI
from routers.users import router as router_user
from routers.notification import router as router_notification

app = FastAPI()

app.include_router(router_user)
app.include_router(router_notification)