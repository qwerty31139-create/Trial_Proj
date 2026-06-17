"""
Test suite for LLM Service
"""

import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from backend.services.llm_service import LLMService

@pytest.fixture
def llm_service():
    with patch('backend.services.llm_service.AzureOpenAI'):
        return LLMService()

def test_generate_epic(llm_service):
    """Test epic generation from requirement"""
    requirement = "Build a user authentication system with MFA"
    
    # Mock LLM response
    mock_response = {
        "title": "User Authentication & Authorization",
        "description": "Implement secure authentication system",
        "business_value": "Improved security",
        "success_criteria": ["Support MFA", "OAuth integration"],
        "estimated_effort": "Large",
        "priority": "High",
        "technical_tags": ["auth", "security"]
    }
    
    llm_service.client.chat.completions.create = MagicMock()
    llm_service.client.chat.completions.create.return_value.choices[0].message.content = json.dumps(mock_response)
    
    # Call service
    result = llm_service.generate_epic(requirement)
    
    # Assertions
    assert result["title"] == "User Authentication & Authorization"
    assert result["priority"] == "High"
    assert len(result["success_criteria"]) == 2

def test_generate_features(llm_service):
    """Test feature generation"""
    mock_response = {
        "features": [
            {
                "title": "Email-based MFA",
                "description": "MFA via email",
                "acceptance_criteria": ["Code within 30s"],
                "estimated_story_points": 5,
                "priority": "High"
            }
        ]
    }
    
    llm_service.client.chat.completions.create = MagicMock()
    llm_service.client.chat.completions.create.return_value.choices[0].message.content = json.dumps(mock_response)
    
    result = llm_service.generate_features("Epic Title", "Requirement")
    
    assert len(result["features"]) == 1
    assert result["features"][0]["title"] == "Email-based MFA"

def test_generate_user_stories(llm_service):
    """Test user story generation"""
    mock_response = {
        "user_stories": [
            {
                "title": "User receives MFA code",
                "as_a": "user",
                "i_want": "to receive MFA code",
                "so_that": "I can verify identity",
                "acceptance_criteria": ["Given...", "When...", "Then..."],
                "story_points": 3,
                "priority": "High"
            }
        ]
    }
    
    llm_service.client.chat.completions.create = MagicMock()
    llm_service.client.chat.completions.create.return_value.choices[0].message.content = json.dumps(mock_response)
    
    result = llm_service.generate_user_stories("Feature", "Description")
    
    assert len(result["user_stories"]) == 1
    assert result["user_stories"][0]["as_a"] == "user"

def test_invalid_json_response(llm_service):
    """Test handling of invalid JSON from LLM"""
    llm_service.client.chat.completions.create = MagicMock()
    llm_service.client.chat.completions.create.return_value.choices[0].message.content = "Invalid JSON"
    
    with pytest.raises(ValueError):
        llm_service.generate_epic("Requirement")
