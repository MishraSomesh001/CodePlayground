import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the backend root directory
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    def __init__(self) -> None:
        self.DATABASE_HOSTNAME = os.getenv("DATABASE_HOSTNAME", "localhost")
        self.DATABASE_PORT = os.getenv("DATABASE_PORT", "")
        self.DATABASE_NAME = os.getenv("DATABASE_NAME", "")
        self.DATABASE_USERNAME = os.getenv("DATABASE_USERNAME", "")
        self.DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")

        # Auth / CORS
        self.CORS_ORIGINS: list[str] = [
            origin.strip()
            for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
            if origin.strip()
        ]
        self.GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "")
        self.GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "")

        self._validate()

    def _validate(self) -> None:
        required_fields = {
            "DATABASE_HOSTNAME": self.DATABASE_HOSTNAME,
            "DATABASE_PORT": self.DATABASE_PORT,
            "DATABASE_NAME": self.DATABASE_NAME,
            "DATABASE_USERNAME": self.DATABASE_USERNAME,
            "DATABASE_PASSWORD": self.DATABASE_PASSWORD,
        }

        missing = [name for name, value in required_fields.items() if not value]
        if missing:
            raise ValueError(
                f"Missing required environment variable(s): {', '.join(missing)}. "
                "Please set them in your .env file or environment."
            )

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        """Sync URL used by Alembic migrations."""
        return (
            f"postgresql://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}"
            f"@{self.DATABASE_HOSTNAME}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )


try:
    settings = Settings()
except ValueError as e:
    raise SystemExit(f"Configuration error: {e}") from e
