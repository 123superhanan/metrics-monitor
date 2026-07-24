from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes_predict import router
from .routes_lstm import router as lstm_router

app = FastAPI(
    title="Metrics Monitor API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
app.include_router(lstm_router)

@app.get("/")
def home():
    return {
        "message": "Metrics Monitor API running"
    }