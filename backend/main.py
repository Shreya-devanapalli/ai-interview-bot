from routers.interview import router as interview_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import engine
from database.models import Base

from routers.auth import router as auth_router

# ---------------- APP SETUP ----------------

app = FastAPI()
app.include_router(interview_router)
app.include_router(auth_router)
Base.metadata.create_all(bind=engine)


# ✅ CORS (required for React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

