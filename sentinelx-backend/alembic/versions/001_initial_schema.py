"""Initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-28

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sources",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("source_type", sa.String(64), nullable=False),
        sa.Column("base_url", sa.Text(), nullable=False),
        sa.Column("category", sa.String(128)),
        sa.Column("scraping_strategy", sa.String(64), server_default="http"),
        sa.Column("frequency_minutes", sa.Integer(), server_default="60"),
        sa.Column("is_active", sa.Boolean(), server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "scrape_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sources.id")),
        sa.Column("status", sa.String(32), server_default="pending"),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("finished_at", sa.DateTime(timezone=True)),
        sa.Column("error_message", sa.Text()),
        sa.Column("records_collected", sa.Integer(), server_default="0"),
        sa.Column("retry_count", sa.Integer(), server_default="0"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "raw_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("sources.id")),
        sa.Column("scrape_job_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("scrape_jobs.id")),
        sa.Column("url", sa.Text(), nullable=False),
        sa.Column("raw_html", sa.Text()),
        sa.Column("raw_text", sa.Text()),
        sa.Column("content_hash", sa.Text(), nullable=False),
        sa.Column("fetched_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("metadata", postgresql.JSONB(), server_default="{}"),
    )
    op.create_table(
        "parsed_records",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("raw_record_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("raw_records.id"), unique=True),
        sa.Column("title", sa.Text()),
        sa.Column("clean_text", sa.Text(), nullable=False),
        sa.Column("detected_entities", postgresql.JSONB(), server_default="[]"),
        sa.Column("detected_language", sa.Text()),
        sa.Column("published_at", sa.DateTime(timezone=True)),
        sa.Column("parsed_metadata", postgresql.JSONB(), server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_table(
        "intelligence_signals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("parsed_record_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("parsed_records.id")),
        sa.Column("signal_type", sa.String(64), nullable=False),
        sa.Column("category", sa.String(128), nullable=False),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("entities", postgresql.JSONB(), server_default="[]"),
        sa.Column("severity", sa.Integer(), server_default="0"),
        sa.Column("confidence", sa.Float(), server_default="0"),
        sa.Column("source_reliability", sa.Float(), server_default="0"),
        sa.Column("evidence", postgresql.JSONB(), server_default="[]"),
        sa.Column("recommended_action", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("intelligence_signals")
    op.drop_table("parsed_records")
    op.drop_table("raw_records")
    op.drop_table("scrape_jobs")
    op.drop_table("sources")
