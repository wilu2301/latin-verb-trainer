import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .router import verb

app = FastAPI()

# DEVELOPMENT ONLY

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# KEEP THIS ORDER !

# Add the API
app.include_router(verb.router)


# Add the index Page
@app.get("/")
async def index():
    return FileResponse(os.path.join("static", "app.html"))


# Add the resources for the frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
