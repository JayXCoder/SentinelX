# SentinelX Master Documentation

## Project Overview

SentinelX is an AI-powered enterprise intelligence platform designed to transform massive amounts of fragmented internet data into actionable enterprise intelligence.

The platform continuously:

- collects
- processes
- correlates
- analyzes
- summarizes
- scores
- explains

signals from:

- public web sources
- social media
- technical intelligence feeds
- cybersecurity sources
- market intelligence
- vendor ecosystems
- financial indicators
- OSINT platforms

The objective is not simply monitoring data.

The objective is to:

- reason over intelligence
- correlate unrelated signals
- identify opportunities
- identify risks
- generate explainable insights
- produce executive-level intelligence
- support enterprise decision making

SentinelX combines:

- cybersecurity intelligence
- GTM intelligence
- vendor risk analysis
- financial intelligence
- executive intelligence
- AI reasoning systems

inside a unified AI-native platform.

---

# Team Structure

## Jay

### Responsibilities

- Web Data Sources
- Bright Data Infrastructure
- Distributed Scraping
- Redis Streaming Pipeline
- AI Processing Layer
- Intelligence Agents

### Ownership

Jay owns:

- scraping infrastructure
- ingestion pipelines
- distributed workers
- streaming architecture
- AI enrichment pipelines
- event processing
- intelligence generation

---

## Kai Zhe

### Responsibilities

- Correlation Engine
- Risk Scoring Engine
- Knowledge Graph
- RAG Memory Layer

### Ownership

Kai Zhe owns:

- signal correlation
- multi-source reasoning
- intelligence fusion
- explainable scoring
- semantic retrieval
- knowledge graph systems
- contextual AI memory

---

## Raymond

### Responsibilities

Frontend development together with Geng Xin.

### Ownership

Raymond owns:

- frontend architecture
- dashboard implementation
- API integration
- frontend state management
- realtime rendering
- dashboard functionality

---

## Geng Xin

### Responsibilities

Frontend design and frontend UX systems.

### Ownership

Geng Xin owns:

- UI/UX systems
- reusable components
- design systems
- visual analytics
- responsive design
- realtime dashboard interactions

---

# Technology Stack

## Backend

- FastAPI
- Celery
- Redis
- PostgreSQL
- Docker

## AI Layer

- Qwen
- SGLang

## Vector Database

- Qdrant

## Frontend

- Next.js
- TypeScript
- Tailwind CSS v4

---

# High-Level System Architecture

```text
Web Data Sources
    ↓
Bright Data Infrastructure
    ↓
Distributed Scraping + Collection
    ↓
Redis Streaming Pipeline
    ↓
AI Processing Layer
    ├── Cyber Intelligence Agents
    ├── GTM Intelligence Agents
    ├── Financial Intelligence Agents
    ├── Vendor Risk Agents
    ├── OSINT Agents
    └── Executive Summary Agents
            ↓
Correlation Engine
            ↓
Risk Scoring Engine
            ↓
Knowledge Graph / RAG Memory
            ↓
Dashboard + Alerts + APIs
```

---

# Core Platform Modules

## GTM Intelligence Module

### Capabilities

- competitor tracking
- pricing monitoring
- feature launch detection
- customer sentiment analysis
- market movement tracking
- buying intent discovery
- sales opportunity detection
- hiring trend analysis
- technology adoption detection

### Example Use Cases

- detecting competitor market expansion
- identifying companies likely to buy infrastructure products
- discovering emerging market trends
- monitoring product adoption signals

---

## Cyber Threat Intelligence Module

### Capabilities

- leaked credential detection
- exposed API key detection
- CVE monitoring
- phishing intelligence
- malware tracking
- ransomware monitoring
- GitHub leak analysis
- infrastructure exposure analysis
- dark web intelligence

### Example Use Cases

- detecting exposed company credentials
- identifying emerging vulnerabilities
- monitoring targeted attack campaigns
- analyzing threat actor behavior

---

## Vendor Risk Intelligence Module

### Capabilities

- vendor breach monitoring
- outage monitoring
- SSL monitoring
- operational instability detection
- compliance monitoring
- legal issue tracking
- infrastructure instability analysis
- vendor health scoring

### Example Use Cases

- identifying risky vendors
- detecting operational degradation
- monitoring third-party exposure risks
- analyzing vendor security posture

---

## Financial Intelligence Module

### Capabilities

- funding round monitoring
- acquisition tracking
- executive movement monitoring
- expansion analysis
- bankruptcy risk detection
- financial signal analysis
- market movement tracking

### Example Use Cases

- detecting aggressive expansion
- identifying financial distress
- monitoring market positioning
- analyzing company growth trajectories

---

## Executive Intelligence Layer

### Capabilities

- executive summaries
- strategic recommendations
- explainable intelligence
- executive reporting
- AI-generated insights
- opportunity prioritization
- intelligence contextualization

### Example Use Cases

- generating board-level summaries
- producing executive briefings
- highlighting strategic threats
- explaining market implications

---

# AI Agent System

## Scraper Agent

### Responsibilities

- distributed scraping
- browser automation
- source collection
- structured extraction

---

## Parser Agent

### Responsibilities

- metadata extraction
- normalization
- structured parsing
- entity extraction

---

## Cyber Agent

### Responsibilities

- cybersecurity analysis
- threat classification
- vulnerability detection
- incident enrichment

---

## GTM Agent

### Responsibilities

- market analysis
- competitor monitoring
- opportunity detection
- buying intent analysis

---

## Financial Agent

### Responsibilities

- financial signal extraction
- executive movement analysis
- market trend analysis

---

## Correlation Agent

### Responsibilities

- multi-source reasoning
- event correlation
- temporal analysis
- intelligence fusion

---

## Risk Agent

### Responsibilities

- risk score calculation
- severity estimation
- explainable scoring
- risk prioritization

---

## Executive Agent

### Responsibilities

- executive summarization
- recommendation generation
- contextual explanation
- strategic reporting

---

# Infrastructure Architecture

## Redis

### Purpose

Redis acts as:

- Celery broker
- streaming pipeline
- pub/sub infrastructure
- realtime messaging layer
- event distribution layer
- queue management system

### Redis Streams

Potential streams:

- scrape_records
- parsed_records
- cyber_signals
- gtm_signals
- vendor_signals
- financial_signals
- correlated_events
- risk_scores

---

## PostgreSQL

### Purpose

PostgreSQL stores:

- intelligence records
- structured metadata
- audit logs
- signal history
- risk scoring history
- vendors
- entities
- users
- correlation records

---

## Qdrant

### Purpose

Qdrant is used for:

- vector embeddings
- semantic retrieval
- similarity search
- contextual memory
- RAG systems
- semantic intelligence search

---

## Docker

### Purpose

Docker provides:

- isolated services
- environment consistency
- deployment portability
- local orchestration
- scalable service architecture

---

# AI Processing Pipeline

## Step 1 — Data Collection

Data sources are scraped using:

- Bright Data proxies
- browser automation
- distributed scraping workers

Collected data includes:

- websites
- social media
- GitHub repositories
- CVE databases
- public records
- forums
- technical blogs

---

## Step 2 — Parsing and Normalization

Raw content is:

- parsed
- normalized
- structured
- enriched

The parser extracts:

- metadata
- entities
- timestamps
- links
- content categories
- relationships

---

## Step 3 — AI Processing

The AI layer performs:

- summarization
- classification
- sentiment analysis
- entity analysis
- intelligence extraction
- event generation

This stage uses:

- Qwen
- SGLang
- Celery workers

---

## Step 4 — Correlation

Signals from multiple intelligence domains are correlated together.

Examples:

- GitHub leak
- hiring freeze
- infrastructure instability
- negative sentiment

can collectively indicate:

- operational instability
- breach risk
- financial distress
- strategic movement

---

## Step 5 — Risk Scoring

The system generates:

- cyber risk scores
- vendor risk scores
- GTM opportunity scores
- market threat scores
- reputation scores

Scores are:

- explainable
- evidence-backed
- contextualized

---

## Step 6 — RAG Memory and Intelligence Retrieval

The RAG system stores:

- embeddings
- semantic relationships
- contextual memory
- entity histories
- event timelines

The platform can later:

- answer contextual questions
- reconstruct event timelines
- explain intelligence decisions
- provide historical analysis

---

# Frontend Dashboard

## Executive Overview

Displays:

- organization risk posture
- vendor health
- cybersecurity overview
- market movement
- strategic opportunities

---

## Threat Feed

Displays:

- vulnerabilities
- breaches
- phishing campaigns
- ransomware activity
- threat alerts

---

## Competitor Intelligence

Displays:

- competitor pricing
- feature launches
- market movement
- customer sentiment
- expansion activity

---

## Vendor Monitoring

Displays:

- vendor risk scores
- breach history
- operational health
- infrastructure stability
- compliance status

---

## Alerts System

Supports:

- Slack
- Telegram
- Discord
- Email
- Webhooks
- Dashboard notifications

---

# Security Considerations

## Security Goals

- secure API communication
- role-based authorization
- authentication systems
- audit logging
- secrets management
- rate limiting
- event traceability

---

# Future Roadmap

Potential future features:

- autonomous investigation agents
- predictive risk forecasting
- digital twin intelligence
- multi-agent debate systems
- enterprise intelligence copilots
- AI-powered simulations
- autonomous reasoning pipelines

---

# Final Vision

SentinelX aims to become:

> The AI Operating System for Enterprise Intelligence

A platform capable of:

- understanding enterprise risks
- detecting opportunities
- monitoring cyber threats
- reasoning over intelligence
- generating executive insights
- orchestrating AI-powered strategic intelligence
