"""
LLM Service - Handles all communication with Azure OpenAI
"""

import json
import logging
from typing import Dict, Any
from openai import AzureOpenAI
from config.settings import get_settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        settings = get_settings()
        self.client = AzureOpenAI(
            api_key=settings.azure_openai_api_key,
            api_version="2024-02-15-preview",
            azure_endpoint=settings.azure_openai_endpoint
        )
        self.deployment_name = settings.azure_openai_deployment_name
    
    def generate_epic(self, requirement: str) -> Dict[str, Any]:
        """Generate an epic from a natural language requirement"""
        return self._call_llm(
            "epic",
            requirement,
            template_vars={"requirement": requirement}
        )
    
    def generate_features(self, epic_title: str, requirement: str) -> Dict[str, Any]:
        """Generate features from an epic"""
        return self._call_llm(
            "feature",
            requirement,
            template_vars={
                "epic_title": epic_title,
                "feature_description": requirement
            }
        )
    
    def generate_user_stories(self, feature_title: str, feature_desc: str) -> Dict[str, Any]:
        """Generate user stories from a feature"""
        return self._call_llm(
            "story",
            feature_desc,
            template_vars={
                "feature_title": feature_title,
                "feature_description": feature_desc
            }
        )
    
    def generate_tasks_and_tests(self, story_title: str, story_desc: str, criteria: str) -> Dict[str, Any]:
        """Generate tasks and test cases from a user story"""
        return self._call_llm(
            "task",
            story_desc,
            template_vars={
                "user_story_title": story_title,
                "user_story_description": story_desc,
                "acceptance_criteria": criteria
            }
        )
    
    def _call_llm(self, artifact_type: str, user_input: str, template_vars: Dict[str, str]) -> Dict[str, Any]:
        """Call Azure OpenAI with prompt template"""
        try:
            # Load prompt template
            prompt = self._load_prompt_template(artifact_type)
            
            # Format template with variables
            for key, value in template_vars.items():
                prompt = prompt.replace(f"{{{key}}}", value)
            
            # Call LLM
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that converts requirements into structured engineering artifacts. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            # Extract and parse response
            content = response.choices[0].message.content
            result = json.loads(content)
            
            logger.info(f"Successfully generated {artifact_type} from LLM")
            return result
        
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM response as JSON: {e}")
            raise ValueError(f"Invalid JSON response from LLM: {e}")
        except Exception as e:
            logger.error(f"LLM call failed: {e}")
            raise
    
    def _load_prompt_template(self, artifact_type: str) -> str:
        """Load prompt template from file"""
        template_path = f"/workspaces/Trial_Proj/config/prompt_templates/{artifact_type}_prompt.txt"
        try:
            with open(template_path, 'r') as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Prompt template not found: {template_path}")
            raise
