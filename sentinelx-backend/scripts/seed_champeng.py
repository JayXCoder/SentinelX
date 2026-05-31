#!/usr/bin/env python3
"""Seed ChamPeng company profile, competitor sources, and demo intelligence signals."""

from __future__ import annotations

import hashlib
import os
import sys
import time
import uuid
from datetime import datetime, timezone

import httpx

API_BASE = os.environ.get(
    "SENTINELX_API_URL",
    os.environ.get("API_INTERNAL_URL", "http://127.0.0.1:4000"),
).rstrip("/")
INTEL_BASE = os.environ.get(
    "SENTINELX_INTEL_URL",
    os.environ.get("INTELLIGENCE_INTERNAL_URL", "http://intelligence_api:4001"),
).rstrip("/")

COMPANY_NAME = "ChamPeng"
COMPANY_TAGLINE = "Coding agent platform with an IDE — own models plus third-party models, Cursor-style."

COMPETITORS = ["OpenAI", "Anthropic", "Cursor", "Antigravity"]

SOURCES = [
    {
        "name": "OpenAI News",
        "source_type": "web",
        "base_url": "https://openai.com/news/",
        "category": "competitor_openai",
        "scraping_strategy": "browser",
        "frequency_minutes": 360,
    },
    {
        "name": "Anthropic News",
        "source_type": "web",
        "base_url": "https://www.anthropic.com/news",
        "category": "competitor_anthropic",
        "scraping_strategy": "browser",
        "frequency_minutes": 360,
    },
    {
        "name": "Cursor Blog",
        "source_type": "web",
        "base_url": "https://cursor.com/blog",
        "category": "competitor_cursor",
        "scraping_strategy": "browser",
        "frequency_minutes": 360,
    },
    {
        "name": "Google Antigravity",
        "source_type": "web",
        "base_url": "https://antigravity.google/",
        "category": "competitor_antigravity",
        "scraping_strategy": "browser",
        "frequency_minutes": 360,
    },
    {
        "name": "ChamPeng — AI coding agents (HN)",
        "source_type": "web",
        "base_url": "https://news.ycombinator.com/",
        "category": "champeng_market",
        "scraping_strategy": "http",
        "frequency_minutes": 720,
    },
]

DEMO_SIGNALS = [
    {
        "signal_type": "gtm",
        "category": "competitor_product",
        "title": "Cursor positions multi-model agent routing as default IDE workflow",
        "summary": "Cursor continues to market unified agent chat with model picker across OpenAI, Anthropic, and others — direct overlap with ChamPeng's multi-model IDE strategy.",
        "entities": ["Cursor", "ChamPeng"],
        "severity": 6,
        "confidence": 0.88,
        "recommended_action": "Highlight ChamPeng model governance and on-prem routing in GTM collateral.",
    },
    {
        "signal_type": "gtm",
        "category": "competitor_launch",
        "title": "OpenAI Codex and agent tooling messaging intensifies",
        "summary": "OpenAI news flow emphasizes agentic coding and enterprise partnerships, increasing buyer confusion between ChamPeng and OpenAI-native stacks.",
        "entities": ["OpenAI", "ChamPeng"],
        "severity": 5,
        "confidence": 0.85,
        "recommended_action": "Publish comparison matrix: ChamPeng IDE vs OpenAI tooling for regulated teams.",
    },
    {
        "signal_type": "gtm",
        "category": "competitor_launch",
        "title": "Anthropic Claude developer surface expands for code agents",
        "summary": "Anthropic product updates stress long-context coding and safety — ChamPeng should stress hybrid model catalog and IDE-integrated workflows.",
        "entities": ["Anthropic", "ChamPeng"],
        "severity": 5,
        "confidence": 0.84,
        "recommended_action": "Ensure Claude routes are first-class in ChamPeng with clear pricing telemetry.",
    },
    {
        "signal_type": "gtm",
        "category": "competitor_launch",
        "title": "Google Antigravity IDE narrative targets agent-native development",
        "summary": "Antigravity positions agent-first engineering environments — monitor feature parity for ChamPeng's agent orchestration and repo-wide refactors.",
        "entities": ["Antigravity", "Google", "ChamPeng"],
        "severity": 7,
        "confidence": 0.82,
        "recommended_action": "Accelerate ChamPeng differentiators: multi-vendor models + unified enterprise policy layer.",
    },
    {
        "signal_type": "cyber",
        "category": "supply_chain",
        "title": "Third-party model API keys in IDE extensions remain a top exposure",
        "summary": "Competitor ecosystems rely on external inference endpoints; ChamPeng must enforce vault-backed credentials and audit logs for customer deployments.",
        "entities": ["ChamPeng"],
        "severity": 7,
        "confidence": 0.9,
        "recommended_action": "Ship mandatory secrets scanning in ChamPeng agent runs.",
    },
    {
        "signal_type": "vendor_risk",
        "category": "model_provider",
        "title": "OpenAI API availability impacts multi-model IDE uptime",
        "summary": "ChamPeng routes traffic across providers; OpenAI incidents directly affect blended SLA for customers using GPT models in the IDE.",
        "entities": ["OpenAI", "ChamPeng"],
        "severity": 6,
        "confidence": 0.87,
        "recommended_action": "Enable automatic failover to Anthropic and local Qwen/Qwen3.5-2B endpoints.",
    },
    {
        "signal_type": "vendor_risk",
        "category": "model_provider",
        "title": "Anthropic rate limits cited in enterprise coding pilots",
        "summary": "Teams evaluating ChamPeng alongside Cursor report throttling on Claude during large refactors — capacity planning required.",
        "entities": ["Anthropic", "ChamPeng"],
        "severity": 5,
        "confidence": 0.8,
        "recommended_action": "Offer ChamPeng-managed capacity pools and queue-aware agents.",
    },
    {
        "signal_type": "osint",
        "category": "market_sentiment",
        "title": "Developers compare ChamPeng to Cursor on pricing and model choice",
        "summary": "Social chatter highlights desire for Cursor-like UX with transparent multi-model billing — core ChamPeng positioning.",
        "entities": ["ChamPeng", "Cursor"],
        "severity": 4,
        "confidence": 0.78,
        "recommended_action": "Launch public pricing calculator for BYOK and hosted models.",
    },
    {
        "signal_type": "executive_summary",
        "category": "weekly_posture",
        "title": "ChamPeng competitive posture — agent IDE market",
        "summary": (
            f"{COMPANY_NAME} operates in the coding-agent IDE segment against {', '.join(COMPETITORS)}. "
            "Primary threats: Cursor UX leadership, OpenAI/Anthropic model gravity, Antigravity agent-native IDE. "
            "Primary opportunities: unified multi-model governance, enterprise policy, and owned Qwen/Qwen3.5-2B inference."
        ),
        "entities": [COMPANY_NAME, *COMPETITORS],
        "severity": 6,
        "confidence": 0.92,
        "recommended_action": "Review executive dashboard weekly; recalibrate GTM against Cursor launches.",
    },
]


def _api_client() -> httpx.Client:
    return httpx.Client(base_url=API_BASE, timeout=120.0)


def seed_sources(client: httpx.Client) -> list[dict]:
    existing = {s["name"]: s for s in client.get("/sources").json()}
    created: list[dict] = []
    for spec in SOURCES:
        if spec["name"] in existing:
            created.append(existing[spec["name"]])
            print(f"  source exists: {spec['name']}")
            continue
        response = client.post("/sources", json=spec)
        response.raise_for_status()
        source = response.json()
        created.append(source)
        print(f"  source created: {spec['name']}")
    return created


def trigger_scrapes(client: httpx.Client, sources: list[dict]) -> None:
    for source in sources:
        sid = source["id"]
        response = client.post(f"/scrape-jobs/run-source/{sid}")
        if response.status_code == 200:
            print(f"  scrape enqueued: {source['name']}")
        else:
            print(f"  scrape skipped ({response.status_code}): {source['name']}")


def seed_demo_signals_db() -> int:
    """Insert demo signals and publish to Redis for the intelligence layer."""
    from app.db.models.intelligence_signal import IntelligenceSignal
    from app.db.models.parsed_record import ParsedRecord
    from app.db.models.raw_record import RawRecord
    from app.db.models.scrape_job import ScrapeJob
    from app.db.models.source import Source
    from app.db.session import SessionLocal
    from app.schemas.signal import KaiZheSignalExport
    from app.services.agent_processing_service import AgentProcessingService
    from app.services.redis_stream_service import SIGNAL_STREAM_BY_TYPE, get_redis_stream_service

    db = SessionLocal()
    streams = get_redis_stream_service()
    inserted = 0

    try:
        source = db.query(Source).filter(Source.category == "champeng_market").first()
        if not source:
            source = Source(
                name="ChamPeng Intelligence (seed)",
                source_type="web",
                base_url="https://champeng.local/intel",
                category="champeng_market",
                scraping_strategy="http",
                frequency_minutes=1440,
                is_active=True,
            )
            db.add(source)
            db.flush()

        job = ScrapeJob(source_id=source.id, status="completed")
        db.add(job)
        db.flush()

        for spec in DEMO_SIGNALS:
            title = spec["title"]
            existing = (
                db.query(IntelligenceSignal)
                .filter(IntelligenceSignal.title == title)
                .first()
            )
            if existing:
                continue

            raw = RawRecord(
                source_id=source.id,
                scrape_job_id=job.id,
                url=f"https://champeng.local/intel/{hashlib.sha256(title.encode()).hexdigest()[:12]}",
                raw_html=f"<html><body><h1>{title}</h1><p>{spec['summary']}</p></body></html>",
                content_hash=hashlib.sha256(title.encode()).hexdigest(),
                record_metadata={"seed": "champeng", "via_proxy": True},
            )
            db.add(raw)
            db.flush()

            parsed = ParsedRecord(
                raw_record_id=raw.id,
                title=title,
                clean_text=spec["summary"],
                detected_entities=spec["entities"],
                parsed_metadata={"seed": "champeng"},
            )
            db.add(parsed)
            db.flush()

            signal = IntelligenceSignal(
                parsed_record_id=parsed.id,
                signal_type=spec["signal_type"],
                category=spec["category"],
                title=title,
                summary=spec["summary"],
                entities=spec["entities"],
                severity=spec["severity"],
                confidence=spec["confidence"],
                source_reliability=0.9,
                evidence=[f"ChamPeng seed intelligence — {COMPANY_NAME} competitive monitoring."],
                recommended_action=spec.get("recommended_action"),
                created_at=datetime.now(timezone.utc),
            )
            db.add(signal)
            db.flush()

            export = AgentProcessingService.to_kai_zhe_export(signal, source, parsed)
            stream = SIGNAL_STREAM_BY_TYPE.get(spec["signal_type"], "cyber_signals")
            streams.publish(stream, export.model_dump(mode="json"))
            inserted += 1

        db.commit()
        return inserted
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def run_intelligence_pipeline() -> None:
    with httpx.Client(base_url=INTEL_BASE, timeout=300.0) as client:
        try:
            health = client.get("/health")
            health.raise_for_status()
        except Exception as exc:
            print(f"  intelligence API unavailable: {exc}")
            return

        print("  running correlation API...")
        client.post("/correlation/run", json={"time_window_hours": 168, "min_signals": 2})

        print("  rebuilding knowledge graph...")
        try:
            client.post("/graph/rebuild")
        except Exception as exc:
            print(f"    graph rebuild skipped: {exc}")

        print("  recalculating risk scores...")
        client.post("/risk-scores/recalculate", json={"force": True})


def wait_for_live_signals(client: httpx.Client, timeout_sec: int = 90) -> int:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        response = client.get("/agents/signals", params={"limit": 100})
        if response.status_code == 200:
            count = len(response.json())
            if count >= 5:
                return count
        time.sleep(5)
    return len(client.get("/agents/signals", params={"limit": 100}).json())


def main() -> int:
    print(f"=== ChamPeng SentinelX bootstrap ({COMPANY_NAME}) ===")
    print(f"Competitors: {', '.join(COMPETITORS)}")
    print(f"API: {API_BASE}  Intelligence: {INTEL_BASE}\n")

    with _api_client() as client:
        print("1) Seeding sources...")
        sources = seed_sources(client)

        print("1b) Ensuring ChamPeng workspace profile (AI context)...")
        profile = client.get("/workspace/profile")
        profile.raise_for_status()
        print(f"   workspace: {profile.json().get('company_name')}")

        print("2) Enqueueing Bright Data scrapes...")
        trigger_scrapes(client, sources)

        print("3) Seeding demo intelligence (DB + Redis)...")
        count = seed_demo_signals_db()
        print(f"   inserted {count} demo signals")

        print("4) Waiting for API signal count...")
        total = wait_for_live_signals(client)
        print(f"   signals visible: {total}")

    print("5) Intelligence correlation + risk scoring...")
    run_intelligence_pipeline()

    print("\nDone. Open http://localhost:4002/dashboard")
    return 0


if __name__ == "__main__":
    sys.exit(main())
