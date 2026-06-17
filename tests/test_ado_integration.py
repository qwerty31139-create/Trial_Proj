"""
Test suite for ADO Integration Service
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.services.ado_service import ADOService
from backend.models.work_items import ADOSyncResult

@pytest.fixture
def ado_service():
    with patch('backend.services.ado_service.DefaultAzureCredential'):
        with patch('backend.services.ado_service.Connection'):
            return ADOService()

def test_create_epic(ado_service):
    """Test epic creation in ADO"""
    # Mock the work item client
    mock_work_item = Mock()
    mock_work_item.id = 12345
    mock_work_item.url = "https://dev.azure.com/org/project/_workitems/edit/12345"
    
    ado_service.wit_client.create_work_item = MagicMock(return_value=mock_work_item)
    
    # Call service
    result = ado_service.create_epic(
        title="Auth System",
        description="Authentication",
        business_value="Security",
        success_criteria=["MFA", "OAuth"],
        tags=["auth"]
    )
    
    # Assertions
    assert result.success is True
    assert result.ado_work_item_id == 12345
    assert result.artifact_type == "epic"

def test_create_feature(ado_service):
    """Test feature creation and linking"""
    mock_work_item = Mock()
    mock_work_item.id = 12346
    mock_work_item.url = "https://dev.azure.com/org/project/_workitems/edit/12346"
    
    ado_service.wit_client.create_work_item = MagicMock(return_value=mock_work_item)
    ado_service.wit_client.update_work_item = MagicMock()
    
    result = ado_service.create_feature(
        title="Email MFA",
        description="MFA via email",
        epic_id=12345,
        acceptance_criteria=["Deliver within 30s"],
        story_points=5
    )
    
    assert result.success is True
    assert result.ado_work_item_id == 12346

def test_create_user_story(ado_service):
    """Test user story creation"""
    mock_work_item = Mock()
    mock_work_item.id = 12347
    mock_work_item.url = "https://dev.azure.com/org/project/_workitems/edit/12347"
    
    ado_service.wit_client.create_work_item = MagicMock(return_value=mock_work_item)
    ado_service.wit_client.update_work_item = MagicMock()
    
    result = ado_service.create_user_story(
        title="User receives MFA code",
        as_a="user",
        i_want="to get code",
        so_that="verify identity",
        acceptance_criteria=["Given login"],
        story_points=3,
        feature_id=12346
    )
    
    assert result.success is True
    assert result.ado_work_item_id == 12347

def test_create_task(ado_service):
    """Test task creation"""
    mock_work_item = Mock()
    mock_work_item.id = 12348
    mock_work_item.url = "https://dev.azure.com/org/project/_workitems/edit/12348"
    
    ado_service.wit_client.create_work_item = MagicMock(return_value=mock_work_item)
    ado_service.wit_client.update_work_item = MagicMock()
    
    result = ado_service.create_task(
        title="Implement email service",
        description="Integrate SendGrid",
        story_id=12347,
        estimated_hours=8
    )
    
    assert result.success is True
    assert result.ado_work_item_id == 12348

def test_create_test_case(ado_service):
    """Test case creation"""
    mock_work_item = Mock()
    mock_work_item.id = 12349
    mock_work_item.url = "https://dev.azure.com/org/project/_workitems/edit/12349"
    
    ado_service.wit_client.create_work_item = MagicMock(return_value=mock_work_item)
    ado_service.wit_client.update_work_item = MagicMock()
    
    result = ado_service.create_test_case(
        title="Verify email sent",
        scenario="User requests MFA",
        steps=["1. Login", "2. Request code"],
        expected_result="Email received",
        story_id=12347
    )
    
    assert result.success is True
    assert result.ado_work_item_id == 12349

def test_get_work_item(ado_service):
    """Test fetching work item"""
    mock_work_item = Mock()
    mock_work_item.id = 12345
    mock_work_item.rev = 1
    mock_work_item.url = "https://..."
    mock_work_item.fields = {
        "System.WorkItemType": "Epic",
        "System.State": "Active",
        "System.Title": "Auth System",
        "System.Description": "Desc"
    }
    
    ado_service.wit_client.get_work_item = MagicMock(return_value=mock_work_item)
    
    result = ado_service.get_work_item(12345)
    
    assert result.id == 12345
    assert result.title == "Auth System"

def test_link_work_items(ado_service):
    """Test linking work items"""
    ado_service.wit_client.update_work_item = MagicMock()
    
    result = ado_service._link_work_items(12345, 12346, "System.LinkTypes.Hierarchy-forward")
    
    assert result is True
