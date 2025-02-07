from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dependencies import init_db, init_jwt, init_mongo, init_oauth, init_socketio
from routers import register_all_routes

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4430, http://localhost:5173, https://picks-sous.xyz"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db(app)
init_jwt(app)
init_mongo(app)
init_oauth(app)
init_socketio(app)

register_all_routes(app)

@app.get("/")
def root():
    return {"msg": "FASTAPI backend setup"}

