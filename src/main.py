from fastapi import FastAPI
from infrastructure.controllers.tourist_controller import router as tourist_router
from lifecycle.events import startup, shutdown

app = FastAPI()

app.include_router(tourist_router, prefix="/tourists", tags=["tourists"])

app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)
