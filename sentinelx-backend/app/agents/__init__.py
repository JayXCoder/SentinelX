from app.agents.cyber_agent import CyberAgent
from app.agents.executive_summary_agent import ExecutiveSummaryAgent
from app.agents.financial_agent import FinancialAgent
from app.agents.gtm_agent import GTMAgent
from app.agents.osint_agent import OSINTAgent
from app.agents.vendor_risk_agent import VendorRiskAgent

AGENT_REGISTRY = {
    "cyber": CyberAgent,
    "gtm": GTMAgent,
    "financial": FinancialAgent,
    "vendor_risk": VendorRiskAgent,
    "osint": OSINTAgent,
    "executive_summary": ExecutiveSummaryAgent,
}

DEFAULT_AGENTS = list(AGENT_REGISTRY.keys())
