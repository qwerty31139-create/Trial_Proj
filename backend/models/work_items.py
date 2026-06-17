"""
Azure DevOps Work Item models and helpers
"""

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from enum import Enum

class WorkItemType(str, Enum):
    EPIC = "Epic"
    FEATURE = "Feature"
    USER_STORY = "User Story"
    TASK = "Task"
    TEST_CASE = "Test Case"
    BUG = "Bug"

class WorkItemState(str, Enum):
    NEW = "New"
    ACTIVE = "Active"
    RESOLVED = "Resolved"
    CLOSED = "Closed"

class WorkItemLink(BaseModel):
    rel: str  # "System.LinkTypes.Hierarchy-forward", etc.
    url: str

class WorkItemField(BaseModel):
    """Represents a field in ADO work item"""
    name: str
    value: Any

class ADOWorkItem(BaseModel):
    """Azure DevOps Work Item"""
    id: int
    rev: int
    url: str
    work_item_type: WorkItemType
    state: WorkItemState
    title: str
    description: Optional[str]
    assigned_to: Optional[str]
    story_points: Optional[int]
    tags: List[str] = []
    links: List[WorkItemLink] = []
    custom_fields: Dict[str, Any] = {}

class ADOLinkRelation(BaseModel):
    """Link between work items"""
    source_id: int
    target_id: int
    rel_type: str  # "System.LinkTypes.Hierarchy-forward"

class ADOSyncResult(BaseModel):
    """Result of syncing artifacts to ADO"""
    success: bool
    artifact_type: str  # epic, feature, etc.
    artifact_id: str
    ado_work_item_id: Optional[int] = None
    ado_url: Optional[str] = None
    error_message: Optional[str] = None
