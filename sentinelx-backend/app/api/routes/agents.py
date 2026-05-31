from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.agents import DEFAULT_AGENTS
from app.core.pagination import DEFAULT_PAGE_LIMIT, LimitQuery
from app.core.security import verify_api_key
from app.db.models.intelligence_signal import IntelligenceSignal
from app.db.models.parsed_record import ParsedRecord
from app.db.models.raw_record import RawRecord
from app.db.session import get_db
from app.schemas.signal import (
    IntelligenceSignalRead,
    KaiZheSignalExport,
    ProcessBatchRequest,
)
from app.schemas.signal_detail import SignalDetailResponse
from app.services.agent_processing_service import AgentProcessingService
from app.services.signal_detail_service import SignalDetailService
from app.workers.ai_worker import process_parsed_record_task

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/process/{parsed_record_id}")
def process_parsed_record(
    parsed_record_id: UUID,
    agents: list[str] | None = None,
    async_mode: bool = False,
    db: Session = Depends(get_db),
    _: None = Depends(verify_api_key),
):
    parsed = db.get(ParsedRecord, parsed_record_id)
    if not parsed:
        raise HTTPException(status_code=404, detail="Parsed record not found")

    if async_mode:
        process_parsed_record_task.delay(str(parsed_record_id), agents)
        return {"status": "queued", "parsed_record_id": str(parsed_record_id)}

    service = AgentProcessingService(db)
    return service.process_record(parsed_record_id, agents=agents)


@router.post("/process-batch")
def process_batch(
    payload: ProcessBatchRequest,
    async_mode: bool = True,
    _: None = Depends(verify_api_key),
) -> dict:
    for record_id in payload.parsed_record_ids:
        process_parsed_record_task.delay(
            str(record_id),
            payload.agents,
        )
    return {"queued": len(payload.parsed_record_ids), "async": async_mode}


@router.get("/status")
def agent_status() -> dict:
    return {
        "available_agents": DEFAULT_AGENTS,
        "default_pipeline": DEFAULT_AGENTS,
    }


@router.get("/signals", response_model=list[IntelligenceSignalRead])
def list_signals(
    db: Session = Depends(get_db),
    signal_type: str | None = None,
    limit: LimitQuery = DEFAULT_PAGE_LIMIT,
) -> list[IntelligenceSignal]:
    query = db.query(IntelligenceSignal)
    if signal_type:
        query = query.filter(IntelligenceSignal.signal_type == signal_type)
    return query.order_by(IntelligenceSignal.created_at.desc()).limit(limit).all()


@router.get("/signals/{signal_id}/detail", response_model=SignalDetailResponse)
def get_signal_detail(signal_id: UUID, db: Session = Depends(get_db)) -> SignalDetailResponse:
    detail = SignalDetailService(db).get_detail(signal_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Signal not found")
    return detail


@router.get("/signals/{signal_id}", response_model=IntelligenceSignalRead)
def get_signal(signal_id: UUID, db: Session = Depends(get_db)) -> IntelligenceSignal:
    signal = db.get(IntelligenceSignal, signal_id)
    if not signal:
        raise HTTPException(status_code=404, detail="Signal not found")
    return signal


@router.get("/signals/{signal_id}/export", response_model=KaiZheSignalExport)
def export_signal_for_kai_zhe(
    signal_id: UUID,
    db: Session = Depends(get_db),
) -> KaiZheSignalExport:
    signal = (
        db.query(IntelligenceSignal)
        .options(
            joinedload(IntelligenceSignal.parsed_record)
            .joinedload(ParsedRecord.raw_record)
            .joinedload(RawRecord.source),
        )
        .filter(IntelligenceSignal.id == signal_id)
        .first()
    )
    if not signal:
        raise HTTPException(status_code=404, detail="Signal not found")
    source = signal.parsed_record.raw_record.source
    return AgentProcessingService.to_kai_zhe_export(
        signal, source, signal.parsed_record
    )
