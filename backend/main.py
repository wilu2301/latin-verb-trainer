from fastapi import FastAPI
from backend.router import verb

app = FastAPI()

app.include_router(verb.router)
