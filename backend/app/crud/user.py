import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.account import Account
from app.models.user import User
from app.schemas.auth import GoogleAccountRequest


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Return user matching the given email, or None."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession,
    *,
    name: str,
    email: str,
    hashed_password: str,
) -> User:
    """Insert a new credentials-based user and return it."""
    user = User(
        id=str(uuid.uuid4()),
        name=name,
        email=email,
        password=hashed_password,
    )
    db.add(user)
    await db.flush()          # populate defaults before returning
    await db.refresh(user)
    return user


async def get_or_create_google_user(
    db: AsyncSession,
    payload: GoogleAccountRequest,
) -> User:
    """
    Find a user by email, or create one.
    Then ensure an Account row is linked for the Google provider.
    Returns the User.
    """
    # 1. Find or create user
    user = await get_user_by_email(db, payload.email)

    if user is None:
        user = User(
            id=str(uuid.uuid4()),
            name=payload.name,
            email=payload.email,
            image=payload.image,
        )
        db.add(user)
        await db.flush()

    # 2. Upsert account link
    result = await db.execute(
        select(Account).where(
            Account.provider == payload.provider,
            Account.provider_account_id == payload.provider_account_id,
        )
    )
    account = result.scalar_one_or_none()

    if account is None:
        account = Account(
            id=str(uuid.uuid4()),
            user_id=user.id,
            type="oauth",
            provider=payload.provider,
            provider_account_id=payload.provider_account_id,
            access_token=payload.access_token,
            refresh_token=payload.refresh_token,
            expires_at=payload.expires_at,
            token_type=payload.token_type,
            scope=payload.scope,
            id_token=payload.id_token,
        )
        db.add(account)
    else:
        # Update tokens on subsequent logins
        account.access_token = payload.access_token
        account.refresh_token = payload.refresh_token
        account.expires_at = payload.expires_at
        account.id_token = payload.id_token

    await db.flush()
    await db.refresh(user)
    return user
