from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown lifecycle."""
    # Verify database connectivity on startup
    async with engine.connect() as conn:
        await conn.execute(
            __import__("sqlalchemy").text("SELECT 1")
        )
    print("✅ Database connected")
    yield
    # Shutdown: dispose of the engine connection pool
    await engine.dispose()
    print("🛑 Database connection closed")


app = FastAPI(
    title="SnippetShare API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "SnippetShare API is running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
