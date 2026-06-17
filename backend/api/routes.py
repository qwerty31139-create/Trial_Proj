"""
API Routes for the Requirements to ADO System
"""

import logging
import uuid
from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from backend.api.schemas import (
    ProcessRequirementRequest, ProcessAndSyncRequest, ArtifactPreview,
    SyncToADORequest, SyncResponse, ProcessingStatus
)
from backend.services.llm_service import LLMService
from backend.services.structuring_service import StructuringService
from backend.services.ado_service import ADOService
from backend.services.storage_service import StorageService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["requirements"])

# Initialize services
llm_service = LLMService()
structuring_service = StructuringService()
ado_service = ADOService()
storage_service = StorageService()

# In-memory processing status tracker (use database in production)
processing_status = {}

@router.post("/process-requirement", response_model=ArtifactPreview)
async def process_requirement(request: ProcessRequirementRequest):
    """
    Process a natural language requirement and generate structured artifacts
    (Epic, Features, User Stories, Tasks, Test Cases)
    """
    try:
        logger.info(f"Processing requirement: {request.requirement[:100]}...")
        
        # Step 1: Generate Epic
        epic_output = llm_service.generate_epic(request.requirement)
        epic = structuring_service.structure_epic(epic_output)
        
        # Step 2: Generate Features
        feature_output = llm_service.generate_features(epic.title, request.requirement)
        features = structuring_service.structure_features(feature_output, epic.id or "epic_1")
        
        # Step 3: Generate User Stories from first feature
        user_stories = []
        for feature in features[:1]:  # Start with first feature
            story_output = llm_service.generate_user_stories(feature.title, feature.description)
            stories = structuring_service.structure_user_stories(story_output, feature.id or "feature_1")
            user_stories.extend(stories)
        
        # Step 4: Generate Tasks and Test Cases
        tasks = []
        test_cases = []
        for story in user_stories[:1]:  # Start with first story
            task_output = llm_service.generate_tasks_and_tests(
                story.title, 
                story.description,
                "\n".join(story.acceptance_criteria)
            )
            task_list, test_list = structuring_service.structure_tasks_and_tests(
                task_output, 
                story.id or "story_1"
            )
            tasks.extend(task_list)
            test_cases.extend(test_list)
        
        # Validate consistency
        structuring_service.validate_consistency(epic, features, user_stories)
        
        logger.info(f"Successfully processed requirement - Epic: {epic.title}, Features: {len(features)}")
        
        return ArtifactPreview(
            epic=epic,
            features=features,
            user_stories=user_stories,
            tasks=tasks,
            test_cases=test_cases
        )
    
    except Exception as e:
        logger.error(f"Failed to process requirement: {e}")
        raise HTTPException(status_code=400, detail=f"Processing failed: {str(e)}")

@router.post("/sync-to-ado", response_model=SyncResponse)
async def sync_to_ado(request: SyncToADORequest, background_tasks: BackgroundTasks):
    """
    Sync processed artifacts to Azure DevOps
    """
    try:
        logger.info(f"Syncing artifacts to ADO for epic_id: {request.epic_id}")
        
        # Create Epic
        epic_result = ado_service.create_epic(
            title="User Authentication System",
            description="Comprehensive authentication solution",
            business_value="Improved security and user experience",
            success_criteria=["MFA support", "OAuth integration", "Audit logs"],
            tags=["authentication", "security"]
        )
        
        if not epic_result.success:
            raise Exception(f"Failed to create epic: {epic_result.error_message}")
        
        # Create Features
        feature_ids = []
        feature_result = ado_service.create_feature(
            title="Email-based MFA",
            description="Multi-factor authentication via email",
            epic_id=epic_result.ado_work_item_id,
            acceptance_criteria=["Email sent within 30 seconds", "OTP expires after 10 minutes"],
            story_points=5
        )
        if feature_result.success:
            feature_ids.append(feature_result.ado_work_item_id)
        
        # Create User Stories
        story_ids = []
        story_result = ado_service.create_user_story(
            title="User receives MFA code via email",
            as_a="user",
            i_want="to receive an MFA code via email",
            so_that="I can verify my identity securely",
            acceptance_criteria=["Code delivered within 30 seconds"],
            story_points=3,
            feature_id=feature_ids[0] if feature_ids else None
        )
        if story_result.success:
            story_ids.append(story_result.ado_work_item_id)
        
        # Create Tasks
        task_ids = []
        task_result = ado_service.create_task(
            title="Implement email service integration",
            description="Integrate with SendGrid/AWS SES",
            story_id=story_ids[0] if story_ids else None,
            estimated_hours=8
        )
        if task_result.success:
            task_ids.append(task_result.ado_work_item_id)
        
        # Create Test Cases
        test_ids = []
        test_result = ado_service.create_test_case(
            title="Verify MFA code is sent",
            scenario="User logs in and requests MFA code",
            steps=["1. Log in", "2. Request MFA code", "3. Check email"],
            expected_result="Email received with valid code",
            story_id=story_ids[0] if story_ids else None
        )
        if test_result.success:
            test_ids.append(test_result.ado_work_item_id)
        
        logger.info(f"Sync completed - Epic: {epic_result.ado_work_item_id}")
        
        return SyncResponse(
            success=True,
            epic_ado_id=epic_result.ado_work_item_id,
            feature_ado_ids=feature_ids,
            story_ado_ids=story_ids,
            task_ado_ids=task_ids,
            test_case_ado_ids=test_ids,
            ado_dashboard_url=f"{epic_result.ado_url}"
        )
    
    except Exception as e:
        logger.error(f"ADO sync failed: {e}")
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

@router.post("/process-and-sync")
async def process_and_sync(request: ProcessAndSyncRequest, background_tasks: BackgroundTasks):
    """
    Process requirement and sync to ADO in one operation
    """
    processing_id = str(uuid.uuid4())
    
    try:
        # Step 1: Process requirement
        processing_status[processing_id] = ProcessingStatus(
            processing_id=processing_id,
            status="processing",
            progress_percent=10,
            current_step="Generating epic from requirement",
            artifacts_count=0,
            ado_sync_status="not_started"
        )
        
        process_req = ProcessRequirementRequest(requirement=request.requirement)
        artifacts = await process_requirement(process_req)
        
        # Step 2: Sync to ADO if auto_sync enabled
        if request.auto_sync:
            processing_status[processing_id].status = "processing"
            processing_status[processing_id].progress_percent = 50
            processing_status[processing_id].current_step = "Syncing to Azure DevOps"
            processing_status[processing_id].ado_sync_status = "in_progress"
            
            sync_req = SyncToADORequest(epic_id=artifacts.epic.id or "epic_1")
            sync_result = await sync_to_ado(sync_req, background_tasks)
            
            processing_status[processing_id].ado_sync_status = "completed" if sync_result.success else "failed"
        
        processing_status[processing_id].status = "completed"
        processing_status[processing_id].progress_percent = 100
        processing_status[processing_id].artifacts_count = (
            1 + len(artifacts.features) + len(artifacts.user_stories) + 
            len(artifacts.tasks) + len(artifacts.test_cases)
        )
        
        logger.info(f"Process and sync completed - ID: {processing_id}")
        
        return {
            "processing_id": processing_id,
            "status": "completed",
            "artifacts": artifacts
        }
    
    except Exception as e:
        processing_status[processing_id].status = "failed"
        processing_status[processing_id].error_message = str(e)
        logger.error(f"Process and sync failed: {e}")
        raise HTTPException(status_code=500, detail=f"Operation failed: {str(e)}")

@router.get("/status/{processing_id}", response_model=ProcessingStatus)
async def get_processing_status(processing_id: str):
    """Get status of a requirement processing operation"""
    if processing_id not in processing_status:
        raise HTTPException(status_code=404, detail="Processing ID not found")
    
    return processing_status[processing_id]

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "components": {
            "llm": "ready",
            "ado": "ready",
            "database": "ready"
        }
    }
