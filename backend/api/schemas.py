"""
API schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from backend.models.artifacts import (
    Epic, Feature, UserStory, Task, TestCase,
    PriorityLevel, EffortLevel, TaskType
)

class ProcessRequirementRequest(BaseModel):
    """Request to process a natural language requirement"""
    requirement: str = Field(..., description="Natural language requirement from stakeholder")
    epic_title: Optional[str] = Field(None, description="Override auto-generated epic title")
    include_architecture_diagram: bool = False
    include_code_skeleton: bool = False

class ArtifactPreview(BaseModel):
    """Preview of generated artifacts before ADO sync"""
    epic: Epic
    features: List[Feature]
    user_stories: List[UserStory]
    tasks: List[Task]
    test_cases: List[TestCase]
    
    class Config:
        json_schema_extra = {
            "example": {
                "epic": {
                    "title": "User Authentication System",
                    "description": "Implement secure authentication with MFA"
                },
                "features": [],
                "user_stories": []
            }
        }

class SyncToADORequest(BaseModel):
    """Request to sync artifacts to Azure DevOps"""
    epic_id: str
    auto_create_links: bool = True
    send_notifications: bool = True
    assign_to_team: Optional[str] = None

class SyncResponse(BaseModel):
    """Response from ADO sync operation"""
    success: bool
    epic_ado_id: Optional[int]
    feature_ado_ids: List[int]
    story_ado_ids: List[int]
    task_ado_ids: List[int]
    test_case_ado_ids: List[int]
    errors: List[str] = []
    ado_dashboard_url: Optional[str]

class ProcessAndSyncRequest(BaseModel):
    """Combined request to process requirement and sync to ADO in one call"""
    requirement: str
    auto_sync: bool = True
    assign_to_team: Optional[str] = None

class ProcessingStatus(BaseModel):
    """Status of requirement processing"""
    processing_id: str
    status: str  # pending, processing, completed, failed
    progress_percent: int
    current_step: str
    artifacts_count: int
    ado_sync_status: str  # not_started, in_progress, completed, failed
    error_message: Optional[str] = None
