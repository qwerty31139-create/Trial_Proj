"""
ADO Service - Handles integration with Azure DevOps
"""

import logging
from typing import List, Optional, Dict, Any
from azure.devops.connection import Connection
from azure.identity import DefaultAzureCredential
from azure.devops.v7_0.work_item_tracking.models import JsonPatchOperation, WorkItem
from config.settings import get_settings
from backend.models.work_items import ADOWorkItem, WorkItemType, ADOSyncResult

logger = logging.getLogger(__name__)

class ADOService:
    def __init__(self):
        settings = get_settings()
        self.organization = settings.ado_organization
        self.project = settings.ado_project
        self.pat = settings.ado_pat
        
        # Initialize ADO client
        credentials = DefaultAzureCredential()
        self.connection = Connection(base_url=self.organization, creds=credentials)
        self.wit_client = self.connection.clients.get_work_item_tracking_client()
    
    def create_epic(self, title: str, description: str, business_value: str, 
                   success_criteria: List[str], tags: List[str] = None) -> ADOSyncResult:
        """Create an Epic in ADO"""
        return self._create_work_item(
            work_item_type="Epic",
            title=title,
            description=description,
            custom_fields={
                "Custom.BusinessValue": business_value,
                "Custom.SuccessCriteria": "\n".join(success_criteria)
            },
            tags=tags or []
        )
    
    def create_feature(self, title: str, description: str, epic_id: int,
                      acceptance_criteria: List[str], story_points: int) -> ADOSyncResult:
        """Create a Feature in ADO"""
        result = self._create_work_item(
            work_item_type="Feature",
            title=title,
            description=description,
            story_points=story_points,
            custom_fields={
                "Custom.AcceptanceCriteria": "\n".join(acceptance_criteria)
            }
        )
        
        # Link to epic
        if result.success and result.ado_work_item_id:
            self._link_work_items(epic_id, result.ado_work_item_id, "System.LinkTypes.Hierarchy-forward")
        
        return result
    
    def create_user_story(self, title: str, as_a: str, i_want: str, so_that: str,
                         acceptance_criteria: List[str], story_points: int,
                         feature_id: int) -> ADOSyncResult:
        """Create a User Story in ADO"""
        description = f"**As a** {as_a}\n**I want** {i_want}\n**So that** {so_that}"
        
        result = self._create_work_item(
            work_item_type="User Story",
            title=title,
            description=description,
            story_points=story_points,
            custom_fields={
                "Custom.AcceptanceCriteria": "\n".join(acceptance_criteria)
            }
        )
        
        # Link to feature
        if result.success and result.ado_work_item_id:
            self._link_work_items(feature_id, result.ado_work_item_id, "System.LinkTypes.Hierarchy-forward")
        
        return result
    
    def create_task(self, title: str, description: str, story_id: int,
                   estimated_hours: int = None) -> ADOSyncResult:
        """Create a Task in ADO"""
        custom_fields = {}
        if estimated_hours:
            custom_fields["Microsoft.VSTS.Scheduling.RemainingWork"] = estimated_hours
        
        result = self._create_work_item(
            work_item_type="Task",
            title=title,
            description=description,
            custom_fields=custom_fields
        )
        
        # Link to user story
        if result.success and result.ado_work_item_id:
            self._link_work_items(story_id, result.ado_work_item_id, "System.LinkTypes.Hierarchy-forward")
        
        return result
    
    def create_test_case(self, title: str, scenario: str, steps: List[str],
                        expected_result: str, story_id: int) -> ADOSyncResult:
        """Create a Test Case in ADO"""
        step_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps)])
        description = f"**Scenario:** {scenario}\n\n**Steps:**\n{step_text}\n\n**Expected:** {expected_result}"
        
        result = self._create_work_item(
            work_item_type="Test Case",
            title=title,
            description=description
        )
        
        # Link to user story
        if result.success and result.ado_work_item_id:
            self._link_work_items(story_id, result.ado_work_item_id, "System.LinkTypes.Tested")
        
        return result
    
    def _create_work_item(self, work_item_type: str, title: str, description: str = None,
                         story_points: int = None, custom_fields: Dict[str, Any] = None,
                         tags: List[str] = None) -> ADOSyncResult:
        """Internal method to create a work item"""
        try:
            patch_document = [
                JsonPatchOperation(op="add", path="/fields/System.Title", value=title)
            ]
            
            if description:
                patch_document.append(
                    JsonPatchOperation(op="add", path="/fields/System.Description", value=description)
                )
            
            if story_points is not None:
                patch_document.append(
                    JsonPatchOperation(op="add", path="/fields/Microsoft.VSTS.Scheduling.StoryPoints", 
                                     value=story_points)
                )
            
            if tags:
                patch_document.append(
                    JsonPatchOperation(op="add", path="/fields/System.Tags", value=";".join(tags))
                )
            
            # Add custom fields
            if custom_fields:
                for field_name, field_value in custom_fields.items():
                    patch_document.append(
                        JsonPatchOperation(op="add", path=f"/fields/{field_name}", value=field_value)
                    )
            
            # Create work item
            work_item = self.wit_client.create_work_item(
                document=patch_document,
                project=self.project,
                type=work_item_type
            )
            
            logger.info(f"Created {work_item_type} {work_item.id}: {title}")
            
            return ADOSyncResult(
                success=True,
                artifact_type=work_item_type.lower(),
                artifact_id=str(work_item.id),
                ado_work_item_id=work_item.id,
                ado_url=work_item.url
            )
        
        except Exception as e:
            logger.error(f"Failed to create {work_item_type}: {e}")
            return ADOSyncResult(
                success=False,
                artifact_type=work_item_type.lower(),
                artifact_id="",
                error_message=str(e)
            )
    
    def _link_work_items(self, source_id: int, target_id: int, rel_type: str) -> bool:
        """Link two work items"""
        try:
            patch_document = [
                JsonPatchOperation(
                    op="add",
                    path="/relations/-",
                    value={
                        "rel": rel_type,
                        "url": f"{self.organization}/{self.project}/_apis/wit/workitems/{target_id}"
                    }
                )
            ]
            
            self.wit_client.update_work_item(
                document=patch_document,
                id=source_id,
                project=self.project
            )
            
            logger.info(f"Linked work item {source_id} to {target_id}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to link work items {source_id} -> {target_id}: {e}")
            return False
    
    def get_work_item(self, work_item_id: int) -> Optional[ADOWorkItem]:
        """Fetch a work item from ADO"""
        try:
            work_item = self.wit_client.get_work_item(
                id=work_item_id,
                project=self.project
            )
            
            return ADOWorkItem(
                id=work_item.id,
                rev=work_item.rev,
                url=work_item.url,
                work_item_type=work_item.fields.get("System.WorkItemType"),
                state=work_item.fields.get("System.State"),
                title=work_item.fields.get("System.Title"),
                description=work_item.fields.get("System.Description")
            )
        
        except Exception as e:
            logger.error(f"Failed to fetch work item {work_item_id}: {e}")
            return None
