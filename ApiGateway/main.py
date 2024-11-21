from fastapi import FastAPI
from ApiGateway.routers import messenger

app = FastAPI(title="API Gateway")


app.include_router(messenger.router, prefix="/messenger", tags=["Messenger"])

