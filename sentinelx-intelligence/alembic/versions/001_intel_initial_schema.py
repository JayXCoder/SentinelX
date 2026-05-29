"""Intel initial schema

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
        "intel_signals",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("signal_id", sa.String(255), nullable=False, unique=True),
        sa.Column("signal_type", sa.String(64), nullable=False),
        sa.Column("category", sa.String(128), nullable=False),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("entities", postgresql.JSONB(), server_default="[]"),
        sa.Column("source_id", sa.String(255)),
        sa.Column("source_name", sa.String(255)),
        sa.Column("source_url", sa.Text()),
        sa.Column("source_type", sa.String(64)),
        sa.Column("timestamp", sa.DateTime(timezone=True)),
        sa.Column("severity", sa.Integer(), server_default="0"),
        sa.Column("confidence", sa.Float(), server_default="0"),
        sa.Column("source_reliability", sa.Float(), server_default="0"),
        sa.Column("evidence", postgresql.JSONB(), server_default="[]"),
        sa.Column("recommended_action", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "correlated_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("event_type", sa.String(64), nullable=False),
        sa.Column("title", sa.String(512), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("involved_entities", postgresql.JSONB(), server_default="[]"),
        sa.Column("signal_ids", postgresql.JSONB(), server_default="[]"),
        sa.Column("correlation_reason", sa.Text(), nullable=False),
        sa.Column("confidence", sa.Float(), server_default="0"),
        sa.Column("severity", sa.Integer(), server_default="0"),
        sa.Column("first_seen", sa.DateTime(timezone=True)),
        sa.Column("last_seen", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "entities",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, index=True),
        sa.Column("entity_type", sa.String(64), nullable=False),
        sa.Column("aliases", postgresql.JSONB(), server_default="[]"),
        sa.Column("description", sa.Text()),
        sa.Column("metadata", postgresql.JSONB(), server_default="{}"),
        sa.Column("first_seen", sa.DateTime(timezone=True)),
        sa.Column("last_seen", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "risk_scores",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("entities.id"), nullable=False),
        sa.Column("entity_name", sa.String(255), nullable=False),
        sa.Column("score_type", sa.String(64), nullable=False),
        sa.Column("score_value", sa.Float(), nullable=False),
        sa.Column("risk_level", sa.String(32), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("evidence_signal_ids", postgresql.JSONB(), server_default="[]"),
        sa.Column("correlated_event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("correlated_events.id")),
        sa.Column("calculated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "entity_relationships",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("source_entity_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("entities.id"), nullable=False),
        sa.Column("target_entity_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("entities.id"), nullable=False),
        sa.Column("relationship_type", sa.String(64), nullable=False),
        sa.Column("confidence", sa.Float(), server_default="0"),
        sa.Column("evidence_signal_ids", postgresql.JSONB(), server_default="[]"),
        sa.Column("first_seen", sa.DateTime(timezone=True)),
        sa.Column("last_seen", sa.DateTime(timezone=True)),
        sa.Column("metadata", postgresql.JSONB(), server_default="{}"),
    )

    op.create_table(
        "rag_memory",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("qdrant_vector_id", sa.String(255), nullable=False, unique=True),
        sa.Column("source_signal_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("intel_signals.id")),
        sa.Column("correlated_event_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("correlated_events.id")),
        sa.Column("entity_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("entities.id")),
        sa.Column("memory_type", sa.String(64), nullable=False),
        sa.Column("text_chunk", sa.Text(), nullable=False),
        sa.Column("metadata", postgresql.JSONB(), server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("rag_memory")
    op.drop_table("entity_relationships")
    op.drop_table("risk_scores")
    op.drop_table("entities")
    op.drop_table("correlated_events")
    op.drop_table("intel_signals")
