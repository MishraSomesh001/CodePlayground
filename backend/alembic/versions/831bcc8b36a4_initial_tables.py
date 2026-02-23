"""initial_tables
Revision ID: 831bcc8b36a4
Revises: 
Create Date: 2026-02-22 15:22:37.990705
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '831bcc8b36a4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ── users ─────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("password", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("email_verified", sa.DateTime(timezone=True), nullable=True),
        sa.Column("image", sa.String(), nullable=True),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )

    # ── accounts ──────────────────────────────────────────────────────
    op.create_table(
        "accounts",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("provider", sa.String(), nullable=False),
        sa.Column("provider_account_id", sa.String(), nullable=False),
        sa.Column("refresh_token", sa.String(), nullable=True),
        sa.Column("access_token", sa.String(), nullable=True),
        sa.Column("expires_at", sa.Integer(), nullable=True),
        sa.Column("token_type", sa.String(), nullable=True),
        sa.Column("scope", sa.String(), nullable=True),
        sa.Column("id_token", sa.String(), nullable=True),
        sa.Column("session_state", sa.String(), nullable=True),
        sa.UniqueConstraint("provider", "provider_account_id", name="uq_provider_account"),
    )

    # ── sessions ──────────────────────────────────────────────────────
    op.create_table(
        "sessions",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("session_token", sa.String(), unique=True, nullable=False),
        sa.Column("user_id", sa.String(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("expires", sa.DateTime(timezone=True), nullable=False),
    )

    # ── verification_tokens ───────────────────────────────────────────
    op.create_table(
        "verification_tokens",
        sa.Column("identifier", sa.String(), primary_key=True),
        sa.Column("token", sa.String(), unique=True, nullable=False),
        sa.Column("expires", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("identifier", "token", name="uq_identifier_token"),
    )

    # ── snaps ─────────────────────────────────────────────────────────
    op.create_table(
        "snaps",
        sa.Column("id", sa.String(), primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("language", sa.String(), nullable=False),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("visibility", sa.String(), server_default="private"),
        sa.Column("author_id", sa.String(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("snaps")
    op.drop_table("verification_tokens")
    op.drop_table("sessions")
    op.drop_table("accounts")
    op.drop_table("users")
