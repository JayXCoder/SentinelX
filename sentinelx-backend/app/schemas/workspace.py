from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class WorkspaceProfileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    slug: str
    company_name: str
    profile: dict
    updated_at: datetime


class WorkspaceProfileUpdate(BaseModel):
    company_name: str | None = Field(default=None, min_length=1, max_length=255)
    profile: dict | None = None


class HumanNoteCreate(BaseModel):
    target_type: str = Field(min_length=1, max_length=64)
    target_id: str = Field(min_length=1, max_length=64)
    team_role: str = Field(default="general", max_length=32)
    author_name: str = Field(default="Analyst", max_length=128)
    content: str = Field(min_length=1, max_length=10000)


class HumanNoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    target_type: str
    target_id: str
    team_role: str
    author_name: str
    content: str
    created_at: datetime
    updated_at: datetime
