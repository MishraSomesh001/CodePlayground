from pydantic import BaseModel, EmailStr, Field


# ── Requests ──────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class GoogleAccountRequest(BaseModel):
    """Payload sent by NextAuth signIn callback after Google OAuth."""
    email: EmailStr
    name: str | None = None
    image: str | None = None
    provider: str = "google"
    provider_account_id: str
    access_token: str | None = None
    refresh_token: str | None = None
    expires_at: int | None = None
    token_type: str | None = None
    scope: str | None = None
    id_token: str | None = None


# ── Responses ─────────────────────────────────────────────────────────

class UserResponse(BaseModel):
    id: str
    name: str | None = None
    email: str | None = None
    image: str | None = None

    model_config = {"from_attributes": True}
