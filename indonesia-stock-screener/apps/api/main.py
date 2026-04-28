import sys
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel

# Add the monorepo root to path to import shared packages
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from packages.shared import models
from database import engine
from routers import screener, valuation

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="Indonesia Stock Screener API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(screener.router, prefix="/api/screener", tags=["screener"])
app.include_router(valuation.router, prefix="/api/valuation", tags=["valuation"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Indonesia Stock Screener API"}

