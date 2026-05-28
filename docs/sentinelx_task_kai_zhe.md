# SentinelX — task.md for Kai Zhe

## Owner

**Kai Zhe**

## Assigned Scope

Kai Zhe is responsible for the intelligence reasoning layer of SentinelX.

Kai Zhe owns the following architecture section:

```text
Correlation Engine
    ↓
Risk Scoring Engine
    ↓
Knowledge Graph / RAG Memory
```

---

# 1. Main Objective

Build the core intelligence reasoning layer that receives structured intelligence signals from Jay’s AI Processing Layer, correlates them across domains, scores their risk or opportunity level, stores them in a knowledge graph, and makes the intelligence searchable through a RAG memory system.

The goal is to make SentinelX capable of moving from simple signal detection into real intelligence reasoning.

Kai Zhe’s layer must be able to:

- consume structured intelligence signals
- correlate related signals across domains
- identify relationships between companies, vendors, risks, threats and opportunities
- calculate explainable risk scores
- store entities and relationships in a knowledge graph structure
- store semantic memory in Qdrant
- support RAG-based questioning
- provide APIs for the frontend dashboard
- provide contextual evidence for executive summaries

---

# 2. Technology Stack

Kai Zhe’s assigned stack:

- FastAPI
- Celery
- Redis
- PostgreSQL
- Qdrant
- Qwen
- SGLang
- Docker

---

# 3. Service Responsibilities

Kai Zhe needs to build these backend service areas:

## 3.1 Correlation Engine

Responsible for:

- consuming intelligence signals
- grouping related events
- linking entities
- detecting patterns
- building composite intelligence events

## 3.2 Risk Scoring Engine

Responsible for:

- calculating risk scores
- calculating opportunity scores
- explaining score reasoning
- storing score history
- exposing score APIs

## 3.3 Knowledge Graph Layer

Responsible for:

- storing entities
- storing relationships
- linking signals to entities
- building timelines
- enabling graph-based intelligence analysis

## 3.4 RAG Memory Layer

Responsible for:

- storing embeddings
- retrieving relevant context
- answering intelligence questions
- supporting executive explanations

---

# 4. Suggested Folder Structure

```text
sentinelx-intelligence/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── scoring_config.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── health.py
│   │   │   ├── correlation.py
│   │   │   ├── risk_scores.py
│   │   │   ├── knowledge_graph.py
│   │   │   ├── rag.py
│   │   │   └── analytics.py
│   ├── db/
│   │   ├── session.py
│   │   ├── base.py
│   │   └── models/
│   │       ├── intelligence_signal.py
│   │       ├── correlated_event.py
│   │       ├── risk_score.py
│   │       ├── entity.py
│   │       ├── relationship.py
│   │       └── rag_memory.py
│   ├── schemas/
│   │   ├── signal.py
│   │   ├── correlation.py
│   │   ├── risk_score.py
│   │   ├── graph.py
│   │   └── rag.py
│   ├── services/
│   │   ├── correlation_service.py
│   │   ├── risk_scoring_service.py
│   │   ├── knowledge_graph_service.py
│   │   ├── qdrant_service.py
│   │   ├── rag_service.py
│   │   └── sglang_service.py
│   ├── workers/
│   │   ├── celery_app.py
│   │   ├── correlation_worker.py
│   │   ├── risk_worker.py
│   │   └── graph_worker.py
│   └── rules/
│       ├── cyber_rules.py
│       ├── gtm_rules.py
│       ├── vendor_rules.py
│       ├── financial_rules.py
│       └── scoring_rules.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── alembic/
└── README.md
```

---

# 5. Input Contract From Jay

Kai Zhe’s system receives structured intelligence signals from Jay.

## Expected Input Signal Format

```json
{
  "signal_id": "string",
  "signal_type": "cyber | gtm | financial | vendor_risk | osint | executive_summary",
  "category": "string",
  "title": "string",
  "summary": "string",
  "entities": [],
  "source": {
    "source_id": "string",
    "source_name": "string",
    "source_url": "string",
    "source_type": "string"
  },
  "timestamp": "datetime",
  "severity": 0,
  "confidence": 0.0,
  "source_reliability": 0.0,
  "evidence": [],
  "recommended_action": "string"
}
```

---

# 6. Database Tables

## 6.1 intelligence_signals

Stores processed signals received from Jay’s AI layer.

Required fields:

- id
- signal_type
- category
- title
- summary
- entities
- source_id
- source_url
- timestamp
- severity
- confidence
- source_reliability
- evidence
- recommended_action
- created_at

---

## 6.2 correlated_events

Stores grouped intelligence events after correlation.

Required fields:

- id
- event_type
- title
- summary
- involved_entities
- signal_ids
- correlation_reason
- confidence
- severity
- first_seen
- last_seen
- created_at

Event types:

- cyber_incident
- vendor_risk_event
- market_opportunity
- competitor_movement
- financial_instability
- reputation_event
- executive_alert

---

## 6.3 risk_scores

Stores calculated scores.

Required fields:

- id
- entity_id
- entity_name
- score_type
- score_value
- risk_level
- explanation
- evidence_signal_ids
- correlated_event_ids
- calculated_at

Score types:

- cyber_exposure
- vendor_risk
- gtm_opportunity
- market_threat
- financial_risk
- reputation_risk

Risk levels:

- low
- medium
- high
- critical

---

## 6.4 entities

Stores entities discovered from intelligence signals.

Required fields:

- id
- name
- entity_type
- aliases
- description
- metadata
- first_seen
- last_seen
- created_at

Entity types:

- company
- vendor
- product
- technology
- vulnerability
- person
- threat_actor
- location
- domain
- ip_address

---

## 6.5 relationships

Stores graph relationships between entities.

Required fields:

- id
- source_entity_id
- target_entity_id
- relationship_type
- confidence
- evidence_signal_ids
- first_seen
- last_seen
- metadata

Relationship types:

- competes_with
- owns
- uses
- affected_by
- associated_with
- acquired
- supplies
- mentioned_with
- vulnerable_to
- located_in

---

## 6.6 rag_memory

Stores RAG memory references.

Required fields:

- id
- qdrant_vector_id
- source_signal_id
- entity_id
- memory_type
- text_chunk
- metadata
- created_at

Memory types:

- signal_summary
- evidence_chunk
- executive_summary
- correlated_event
- risk_explanation

---

# 7. Redis Stream Design

Kai Zhe consumes the intelligence streams created by Jay.

## Input Streams

```text
cyber_signals
gtm_signals
financial_signals
vendor_risk_signals
osint_signals
executive_summaries
```

## Output Streams

```text
correlated_events
risk_scores
graph_updates
rag_memory_updates
executive_alerts
```

## Stream Flow

```text
intelligence signal streams
    ↓
correlation_worker
    ↓
correlated_events
    ↓
risk_worker
    ↓
risk_scores
    ↓
graph_worker
    ↓
graph_updates + rag_memory_updates
```

---

# 8. FastAPI Endpoints

## 8.1 Health Endpoints

```text
GET /health
GET /health/redis
GET /health/postgres
GET /health/qdrant
GET /health/sglang
```

---

## 8.2 Correlation Endpoints

```text
POST /correlation/run
POST /correlation/run/{signal_id}
GET /correlation/events
GET /correlation/events/{event_id}
GET /correlation/entities/{entity_id}/events
```

---

## 8.3 Risk Score Endpoints

```text
POST /risk-scores/recalculate
POST /risk-scores/recalculate/{entity_id}
GET /risk-scores
GET /risk-scores/{score_id}
GET /risk-scores/entity/{entity_id}
GET /risk-scores/type/{score_type}
```

---

## 8.4 Knowledge Graph Endpoints

```text
GET /graph/entities
GET /graph/entities/{entity_id}
GET /graph/entities/{entity_id}/relationships
GET /graph/relationships
GET /graph/timeline/{entity_id}
POST /graph/rebuild
```

---

## 8.5 RAG Endpoints

```text
POST /rag/query
POST /rag/ask
GET /rag/memory/{entity_id}
POST /rag/reindex
```

---

## 8.6 Analytics Endpoints

```text
GET /analytics/overview
GET /analytics/top-risks
GET /analytics/top-opportunities
GET /analytics/vendor-risk-summary
GET /analytics/cyber-risk-summary
GET /analytics/market-movement-summary
```

---

# 9. Correlation Engine Requirements

## Purpose

The Correlation Engine links multiple individual signals into a higher-level intelligence event.

Example:

```text
Signal 1: Vendor downtime reported
Signal 2: Negative user complaints increasing
Signal 3: Vendor security advisory released
Signal 4: Vendor hiring freeze detected
```

Correlated event:

```text
Vendor operational and security risk increasing
```

---

## Correlation Methods

The engine should support:

- entity-based correlation
- time-window correlation
- category-based correlation
- semantic similarity correlation
- severity-based correlation
- source reliability weighting

---

## Correlation Rule Example

```json
{
  "rule_name": "vendor_instability_risk",
  "required_signal_types": ["vendor_risk", "financial", "osint"],
  "time_window_hours": 72,
  "minimum_signals": 2,
  "entity_match_required": true,
  "output_event_type": "vendor_risk_event"
}
```

---

# 10. Risk Scoring Requirements

## Purpose

The Risk Scoring Engine converts correlated events into explainable scores.

Scores must be:

- evidence-backed
- explainable
- normalized
- comparable
- time-aware

---

## Suggested Score Range

```text
0 - 24   = low
25 - 49  = medium
50 - 74  = high
75 - 100 = critical
```

---

## Suggested Scoring Formula

```text
final_score =
    severity_weight
  + confidence_weight
  + source_reliability_weight
  + recency_weight
  + frequency_weight
  + entity_importance_weight
```

---

## Score Types

### Cyber Exposure Score

Factors:

- severity
- exploitability
- number of threat signals
- source reliability
- affected asset importance

---

### Vendor Risk Score

Factors:

- breach history
- downtime reports
- compliance issues
- negative sentiment
- financial instability

---

### GTM Opportunity Score

Factors:

- buying intent
- hiring signals
- customer complaints
- competitor weakness
- market movement

---

### Market Threat Score

Factors:

- competitor expansion
- pricing changes
- new product launch
- funding activity
- market sentiment

---

### Reputation Risk Score

Factors:

- social sentiment
- news frequency
- public complaints
- legal issues
- influencer discussions

---

# 11. Knowledge Graph Requirements

## Purpose

The Knowledge Graph stores relationships between entities and intelligence events.

It should answer questions like:

- Which vendors are connected to this company?
- Which vulnerabilities affect this technology?
- Which competitors are moving into this market?
- What events are linked to this entity?
- What is the timeline of risk for this vendor?

---

## Node Types

```text
company
vendor
product
technology
vulnerability
person
threat_actor
location
domain
ip_address
```

---

## Edge Types

```text
competes_with
owns
uses
affected_by
associated_with
acquired
supplies
mentioned_with
vulnerable_to
located_in
```

---

# 12. RAG Memory Requirements

## Purpose

The RAG Memory Layer allows SentinelX to answer questions using stored intelligence context.

Example questions:

- Why is Vendor X considered risky?
- What happened to Company Y in the last 30 days?
- Which competitors are showing AI expansion signals?
- What cyber risks are currently most important?

---

## RAG Flow

```text
User Query
    ↓
Embed Query
    ↓
Search Qdrant
    ↓
Retrieve Relevant Intelligence Context
    ↓
Send Context to Qwen via SGLang
    ↓
Generate Evidence-Based Answer
```

---

## RAG Response Format

```json
{
  "answer": "string",
  "confidence": 0.0,
  "supporting_evidence": [],
  "related_entities": [],
  "related_events": [],
  "recommended_action": "string"
}
```

---

# 13. Qdrant Requirements

## Collections

Suggested Qdrant collections:

```text
signals_memory
correlated_events_memory
risk_explanations_memory
entity_memory
executive_memory
```

## Metadata Fields

Each vector should include:

- entity_id
- signal_id
- event_id
- score_id
- memory_type
- timestamp
- source_type
- confidence

---

# 14. Qwen + SGLang Usage

Kai Zhe should use Qwen via SGLang for:

- summarizing correlated events
- generating risk explanations
- answering RAG questions
- creating executive-friendly explanations
- explaining score reasons

## Output Rules

AI outputs must be:

- structured
- evidence-based
- parseable
- confidence-scored
- not hallucinated
- grounded in retrieved context

---

# 15. Celery Worker Tasks

## 15.1 Correlation Worker

Task name:

```text
correlate_signals_task
```

Responsibilities:

- consume intelligence signals
- group related signals
- apply correlation rules
- generate correlated event
- store event in PostgreSQL
- publish to correlated_events stream

---

## 15.2 Risk Worker

Task name:

```text
calculate_risk_score_task
```

Responsibilities:

- consume correlated event
- calculate score
- assign risk level
- generate explanation
- store risk score
- publish to risk_scores stream

---

## 15.3 Graph Worker

Task name:

```text
update_knowledge_graph_task
```

Responsibilities:

- consume signals and events
- upsert entities
- create relationships
- update timelines
- create RAG memory entries
- publish graph updates

---

# 16. Frontend Integration Contract

Kai Zhe must provide APIs for Raymond and Geng Xin.

Frontend needs:

- correlated event list
- risk score summaries
- top risk entities
- top opportunity entities
- entity timelines
- graph relationship data
- RAG answer responses
- dashboard analytics

---

# 17. Integration Contract With Jay

Kai Zhe depends on Jay’s structured intelligence signals.

Required from Jay:

- consistent entity names
- signal categories
- confidence values
- severity values
- source metadata
- evidence fields
- timestamps

If fields are missing, Kai Zhe should:

- validate payload
- reject invalid records
- log validation errors
- expose error in monitoring endpoint

---

# 18. Logging and Monitoring

## Required Logs

- signal consumption logs
- correlation rule logs
- scoring calculation logs
- graph update logs
- Qdrant retrieval logs
- RAG prompt logs
- AI response validation logs

## Required Metrics

- signals consumed
- correlated events created
- scores calculated
- graph nodes created
- graph relationships created
- RAG queries processed
- failed correlation attempts
- failed scoring attempts

---

# 19. Error Handling

## Must Handle

- invalid signal payload
- missing entity data
- duplicate signals
- Redis stream failure
- PostgreSQL failure
- Qdrant failure
- Qwen/SGLang failure
- malformed AI response
- scoring formula failure

## Failure Strategy

- validate input before processing
- retry safe failures
- log failed payloads
- mark failed events
- expose error monitoring
- avoid corrupting graph data

---

# 20. MVP Completion Checklist

## Correlation Engine

- [ ] Consume cyber signals
- [ ] Consume GTM signals
- [ ] Consume financial signals
- [ ] Consume vendor risk signals
- [ ] Consume OSINT signals
- [ ] Create correlated events
- [ ] Store correlated events
- [ ] Publish correlated event stream

## Risk Scoring Engine

- [ ] Cyber exposure scoring complete
- [ ] Vendor risk scoring complete
- [ ] GTM opportunity scoring complete
- [ ] Market threat scoring complete
- [ ] Reputation scoring complete
- [ ] Risk level mapping complete
- [ ] Explanation generation complete

## Knowledge Graph

- [ ] Entity model complete
- [ ] Relationship model complete
- [ ] Entity upsert logic complete
- [ ] Relationship creation logic complete
- [ ] Entity timeline endpoint complete

## RAG Memory

- [ ] Qdrant collections created
- [ ] Signal memory stored
- [ ] Event memory stored
- [ ] Risk explanation memory stored
- [ ] RAG query endpoint complete
- [ ] Qwen answer generation complete

## API

- [ ] Correlation endpoints complete
- [ ] Risk score endpoints complete
- [ ] Graph endpoints complete
- [ ] RAG endpoints complete
- [ ] Analytics endpoints complete

## Docker

- [ ] Dockerfile complete
- [ ] docker-compose service configured
- [ ] Environment variables documented
- [ ] Service starts successfully

---

# 21. Suggested Build Order

## Phase 1 — Foundation

- setup FastAPI service
- setup PostgreSQL models
- setup Redis consumers
- setup Celery worker
- setup Qdrant connection

## Phase 2 — Signal Intake

- consume Jay’s signal streams
- validate signal schema
- store received signals

## Phase 3 — Correlation Engine

- implement entity matching
- implement time-window matching
- implement rule engine
- generate correlated events

## Phase 4 — Risk Scoring

- implement score formulas
- map risk levels
- generate explanations
- store score history

## Phase 5 — Knowledge Graph

- create entity nodes
- create relationships
- link signals and events
- build timeline APIs

## Phase 6 — RAG Layer

- store memory embeddings
- implement Qdrant retrieval
- call Qwen via SGLang
- return evidence-backed answers

## Phase 7 — Frontend Integration

- expose analytics APIs
- expose graph APIs
- expose score APIs
- provide sample responses

---

# 22. Final Deliverable

Kai Zhe’s final deliverable is a working intelligence reasoning layer that can:

1. consume structured intelligence signals from Jay
2. correlate related signals into higher-level events
3. calculate explainable risk and opportunity scores
4. store entities and relationships in a knowledge graph
5. store semantic memory in Qdrant
6. answer contextual questions through RAG
7. expose APIs for the frontend dashboard
8. provide evidence-backed intelligence explanations

This is the reasoning and intelligence fusion layer of SentinelX.

