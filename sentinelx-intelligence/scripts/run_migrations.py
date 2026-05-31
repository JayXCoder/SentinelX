"""Apply Alembic migrations; recover from partial schema without intel_alembic_version."""

from __future__ import annotations

import os
import subprocess
import sys

from sqlalchemy import create_engine, inspect, text

EXPECTED_TABLES = frozenset(
    {
        "intel_signals",
        "correlated_events",
        "entities",
        "risk_scores",
        "entity_relationships",
        "rag_memory",
    }
)
DROP_ORDER = (
    "rag_memory",
    "entity_relationships",
    "risk_scores",
    "entities",
    "correlated_events",
    "intel_signals",
)


def _alembic(*args: str) -> None:
    subprocess.check_call([sys.executable, "-m", "alembic", *args])


def main() -> None:
    database_url = os.environ["DATABASE_URL"]
    engine = create_engine(database_url)
    tables = set(inspect(engine).get_table_names())

    if "intel_alembic_version" in tables:
        _alembic("upgrade", "head")
        return

    intel_tables = tables & EXPECTED_TABLES
    if intel_tables == EXPECTED_TABLES:
        print("Intelligence schema present without version table; stamping head.")
        _alembic("stamp", "head")
        return

    if intel_tables:
        print(
            "Partial intelligence schema detected; resetting tables:",
            ", ".join(sorted(intel_tables)),
        )
        with engine.begin() as conn:
            for name in DROP_ORDER:
                if name in intel_tables:
                    conn.execute(text(f'DROP TABLE IF EXISTS "{name}" CASCADE'))

    _alembic("upgrade", "head")


if __name__ == "__main__":
    main()
