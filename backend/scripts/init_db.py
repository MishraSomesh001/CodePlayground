"""
One-time database initialisation script.

Creates all tables defined in the SQLAlchemy models if they don't already exist.
Safe to re-run — uses CREATE TABLE IF NOT EXISTS under the hood.

Usage:
    cd backend
    python -m scripts.init_db
"""

import asyncio
import sys
from pathlib import Path

# Ensure the backend directory is on sys.path so `app.*` imports work
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import Base, engine  # noqa: E402

# Import all models so Base.metadata knows about every table
from app.models import Account, Session, Snap, User, VerificationToken  # noqa: E402, F401


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()
    print("✅ All tables created (or already exist).")


if __name__ == "__main__":
    asyncio.run(init_db())
