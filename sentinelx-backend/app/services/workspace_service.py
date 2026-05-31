from app.db.models.workspace_profile import WorkspaceProfile
from app.schemas.workspace import WorkspaceProfileUpdate

DEFAULT_CHAMPENG_PROFILE = {
    "tagline": "AI coding agents + IDE with hosted Qwen and third-party models",
    "product_summary": (
        "ChamPeng is a Cursor-style IDE for developers. It routes prompts to "
        "Qwen/Qwen3.5-2B (self-hosted via SGLang) and external APIs (OpenAI, Anthropic). "
        "Positioning: cost-aware, multi-model routing, enterprise-friendly agent workflows."
    ),
    "competitors": [
        {
            "name": "OpenAI",
            "focus": "Codex, ChatGPT, API ecosystem",
            "threat": "Model quality and developer mindshare",
        },
        {
            "name": "Anthropic",
            "focus": "Claude for coding, safety brand",
            "threat": "Enterprise adoption in regulated industries",
        },
        {
            "name": "Cursor",
            "focus": "AI-native IDE, tab completion, agent mode",
            "threat": "Direct product substitute",
        },
        {
            "name": "Antigravity",
            "focus": "Google agentic IDE experiments",
            "threat": "Distribution via Google ecosystem",
        },
    ],
    "team_lenses": {
        "hr": "Hiring signals, culture posts, layoffs, talent poaching from competitors",
        "sales": "Pricing, packaging, enterprise deals, GTM launches, customer wins",
        "tech": "Model releases, security/CVEs, API changes, benchmarks, infra moves",
    },
    "comparison_prompts": [
        "How does this signal affect ChamPeng vs Cursor on agent UX?",
        "What should sales say when prospects mention OpenAI Codex?",
        "Does this raise vendor risk for our Anthropic API dependency?",
    ],
}


class WorkspaceService:
    @staticmethod
    def get_or_create_default(db) -> WorkspaceProfile:
        profile = db.query(WorkspaceProfile).filter(WorkspaceProfile.slug == "champeng").first()
        if profile:
            return profile
        profile = WorkspaceProfile(
            slug="champeng",
            company_name="ChamPeng",
            profile=DEFAULT_CHAMPENG_PROFILE,
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def update(db, payload: WorkspaceProfileUpdate) -> WorkspaceProfile:
        profile = WorkspaceService.get_or_create_default(db)
        if payload.company_name is not None:
            profile.company_name = payload.company_name
        if payload.profile is not None:
            merged = {**(profile.profile or {}), **payload.profile}
            profile.profile = merged
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def context_for_rag(profile: WorkspaceProfile) -> str:
        p = profile.profile or {}
        competitors = p.get("competitors", [])
        comp_lines = "\n".join(
            f"- {c.get('name')}: {c.get('focus')} (threat: {c.get('threat')})"
            for c in competitors
            if isinstance(c, dict)
        )
        lenses = p.get("team_lenses", {})
        lens_lines = "\n".join(f"- {k}: {v}" for k, v in lenses.items())
        return (
            f"Company: {profile.company_name}\n"
            f"{p.get('tagline', '')}\n"
            f"{p.get('product_summary', '')}\n\n"
            f"Competitors monitored:\n{comp_lines}\n\n"
            f"Team analysis lenses:\n{lens_lines}"
        )
