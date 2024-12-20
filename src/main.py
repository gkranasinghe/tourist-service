from fastapi import FastAPI
from infrastructure.controllers.tourist_controller import router as tourist_router

app = FastAPI()
app.include_router(tourist_router, prefix="/tourists", tags=["tourists"])
