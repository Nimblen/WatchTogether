from fastapi import FastAPI
from routers import messenger, auth

app = FastAPI(title="API Gateway")


app.include_router(messenger.router, prefix="/messenger", tags=["Messenger"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
