from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from ..core.analyzer import Analyzer
from ..core.file_processor import FileProcessor
from .routes import router

VERSION = "v1"

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    analyzer = await Analyzer.create()
    file_processor = FileProcessor()
    app.state.analyzer = analyzer
    app.state.file_processor = file_processor
    print("Analyzer and FileProcessor initialized.")

    yield  # app runs

    # Shutdown
    await analyzer.close()
    print("Analyzer closed.")

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],  # Streamlit default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=f"/api/{VERSION}")
