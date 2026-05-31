import pytest
from pydantic import ValidationError

from app.schemas.rag import RAGAskRequest, RAGQueryRequest


def test_rag_ask_top_k_bounds():
    with pytest.raises(ValidationError):
        RAGAskRequest(question="What is the risk?", top_k=0)
    with pytest.raises(ValidationError):
        RAGAskRequest(question="What is the risk?", top_k=21)
    ok = RAGAskRequest(question="What is the risk?", top_k=5)
    assert ok.top_k == 5


def test_rag_query_score_threshold_bounds():
    with pytest.raises(ValidationError):
        RAGQueryRequest(text="competitor pricing", score_threshold=1.5)
    ok = RAGQueryRequest(text="competitor pricing", score_threshold=0.7)
    assert ok.score_threshold == 0.7
