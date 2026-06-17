"""
Test suite for Structuring Service
"""

import pytest
from datetime import datetime
from backend.services.structuring_service import StructuringService
from backend.models.artifacts import Epic, Feature, UserStory

@pytest.fixture
def structuring_service():
    return StructuringService()

def test_structure_epic(structuring_service):
    """Test epic structuring and validation"""
    epic_data = {
        "title": "User Authentication System",
        "description": "Implement secure authentication",
        "business_value": "Improved security",
        "success_criteria": ["Support MFA", "OAuth"],
        "estimated_effort": "Large",
        "priority": "High",
        "technical_tags": ["auth", "security"]
    }
    
    epic = structuring_service.structure_epic(epic_data)
    
    assert isinstance(epic, Epic)
    assert epic.title == "User Authentication System"
    assert epic.priority.value == "High"
    assert len(epic.success_criteria) == 2

def test_structure_features(structuring_service):
    """Test feature structuring"""
    features_data = {
        "features": [
            {
                "title": "Email MFA",
                "description": "MFA via email",
                "acceptance_criteria": ["Deliver within 30s"],
                "estimated_story_points": 5,
                "priority": "High"
            }
        ]
    }
    
    features = structuring_service.structure_features(features_data, "epic_1")
    
    assert len(features) == 1
    assert features[0].title == "Email MFA"
    assert features[0].epic_id == "epic_1"

def test_structure_user_stories(structuring_service):
    """Test user story structuring"""
    stories_data = {
        "user_stories": [
            {
                "title": "Receive MFA code",
                "as_a": "user",
                "i_want": "to get MFA code",
                "so_that": "I verify identity",
                "acceptance_criteria": ["Given login", "When request code"],
                "story_points": 3,
                "priority": "High",
                "dependencies": []
            }
        ]
    }
    
    stories = structuring_service.structure_user_stories(stories_data, "feature_1")
    
    assert len(stories) == 1
    assert stories[0].as_a == "user"
    assert stories[0].feature_id == "feature_1"

def test_structure_tasks_and_tests(structuring_service):
    """Test task and test case structuring"""
    data = {
        "tasks": [
            {
                "title": "Implement email service",
                "description": "Integrate SendGrid",
                "task_type": "Development",
                "estimated_hours": 8,
                "dependencies": [],
                "checklist": ["Research", "Implement", "Test"]
            }
        ],
        "test_cases": [
            {
                "title": "Verify email sent",
                "scenario": "User requests MFA",
                "steps": ["Login", "Request code"],
                "expected_result": "Email received",
                "priority": "Critical"
            }
        ]
    }
    
    tasks, tests = structuring_service.structure_tasks_and_tests(data, "story_1")
    
    assert len(tasks) == 1
    assert tasks[0].title == "Implement email service"
    assert len(tests) == 1
    assert tests[0].priority.value == "Critical"

def test_validate_consistency(structuring_service):
    """Test consistency validation"""
    epic = Epic(
        id="epic_1",
        title="Auth System",
        description="Desc",
        business_value="Value",
        success_criteria=[],
        estimated_effort="Large",
        priority="High"
    )
    
    features = [Feature(
        id="feature_1",
        epic_id="epic_1",
        title="Email MFA",
        description="Desc",
        acceptance_criteria=[],
        estimated_story_points=5,
        priority="High"
    )]
    
    stories = [UserStory(
        id="story_1",
        feature_id="feature_1",
        title="Receive code",
        as_a="user",
        i_want="code",
        so_that="verify",
        acceptance_criteria=[],
        story_points=3,
        priority="High"
    )]
    
    result = structuring_service.validate_consistency(epic, features, stories)
    
    assert result is True

def test_invalid_epic_data(structuring_service):
    """Test handling of invalid epic data"""
    invalid_data = {
        "title": "Title",
        # Missing required fields
    }
    
    with pytest.raises(ValueError):
        structuring_service.structure_epic(invalid_data)
