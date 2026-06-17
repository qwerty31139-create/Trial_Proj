"""
Data models for engineering artifacts (epics, features, user stories, etc.)
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class PriorityLevel(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class EffortLevel(str, Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"

# ===== EPIC =====
class EpicCreate(BaseModel):
    title: str
    description: str
    business_value: str
    success_criteria: List[str]
    estimated_effort: EffortLevel
    priority: PriorityLevel
    technical_tags: List[str] = Field(default_factory=list)

class Epic(EpicCreate):
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    ado_work_item_id: Optional[str] = None

# ===== FEATURE =====
class FeatureCreate(BaseModel):
    title: str
    description: str
    epic_id: str
    acceptance_criteria: List[str]
    dependencies: List[str] = Field(default_factory=list)
    estimated_story_points: int
    priority: PriorityLevel

class Feature(FeatureCreate):
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    ado_work_item_id: Optional[str] = None

# ===== USER STORY =====
class AcceptanceCriteria(BaseModel):
    given: str
    when: str
    then: str

class UserStoryCreate(BaseModel):
    title: str
    as_a: str
    i_want: str
    so_that: str
    acceptance_criteria: List[str]  # Gherkin format
    story_points: int
    priority: PriorityLevel
    feature_id: str
    dependencies: List[str] = Field(default_factory=list)

class UserStory(UserStoryCreate):
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    ado_work_item_id: Optional[str] = None

# ===== TASK =====
class TaskType(str, Enum):
    DEVELOPMENT = "Development"
    TESTING = "Testing"
    DOCUMENTATION = "Documentation"
    DEVOPS = "DevOps"

class TaskCreate(BaseModel):
    title: str
    description: str
    task_type: TaskType
    estimated_hours: int
    user_story_id: str
    dependencies: List[str] = Field(default_factory=list)
    assigned_to: Optional[str] = None
    checklist: List[str] = Field(default_factory=list)

class Task(TaskCreate):
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    ado_work_item_id: Optional[str] = None

# ===== TEST CASE =====
class TestCase(BaseModel):
    title: str
    scenario: str
    steps: List[str]
    expected_result: str
    priority: PriorityLevel
    user_story_id: str
    id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    ado_work_item_id: Optional[str] = None

# ===== REQUIREMENT PROCESSING RESPONSE =====
class RequirementProcessResponse(BaseModel):
    epic: Epic
    features: List[Feature]
    user_stories: List[UserStory]
    tasks: List[Task]
    test_cases: List[TestCase]
    sync_status: str = "pending"  # pending, in_progress, completed, failed
