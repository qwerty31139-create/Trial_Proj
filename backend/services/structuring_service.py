"""
Structuring Service - Converts LLM output to validated artifacts
"""

import json
import logging
from typing import Dict, Any
from pydantic import ValidationError
from backend.models.artifacts import (
    Epic, Feature, UserStory, Task, TestCase,
    EpicCreate, FeatureCreate, UserStoryCreate, TaskCreate
)

logger = logging.getLogger(__name__)

class StructuringService:
    @staticmethod
    def structure_epic(llm_output: Dict[str, Any]) -> Epic:
        """Convert LLM output to Epic model with validation"""
        try:
            epic_data = EpicCreate(**llm_output)
            epic = Epic(**epic_data.dict())
            logger.info(f"Structured epic: {epic.title}")
            return epic
        except ValidationError as e:
            logger.error(f"Epic validation failed: {e}")
            raise ValueError(f"Invalid epic structure: {e}")
    
    @staticmethod
    def structure_features(llm_output: Dict[str, Any], epic_id: str) -> list[Feature]:
        """Convert LLM output to Features with validation"""
        features = []
        try:
            if "features" in llm_output:
                features_data = llm_output["features"]
            else:
                # Single feature case
                features_data = [llm_output]
            
            for feature_data in features_data:
                feature_data["epic_id"] = epic_id
                feature_obj = Feature(**feature_data)
                features.append(feature_obj)
                logger.info(f"Structured feature: {feature_obj.title}")
            
            return features
        except ValidationError as e:
            logger.error(f"Feature validation failed: {e}")
            raise ValueError(f"Invalid feature structure: {e}")
    
    @staticmethod
    def structure_user_stories(llm_output: Dict[str, Any], feature_id: str) -> list[UserStory]:
        """Convert LLM output to User Stories with validation"""
        user_stories = []
        try:
            stories_data = llm_output.get("user_stories", [])
            
            for story_data in stories_data:
                story_data["feature_id"] = feature_id
                story_obj = UserStory(**story_data)
                user_stories.append(story_obj)
                logger.info(f"Structured user story: {story_obj.title}")
            
            return user_stories
        except ValidationError as e:
            logger.error(f"User story validation failed: {e}")
            raise ValueError(f"Invalid user story structure: {e}")
    
    @staticmethod
    def structure_tasks_and_tests(llm_output: Dict[str, Any], story_id: str) -> tuple[list[Task], list[TestCase]]:
        """Convert LLM output to Tasks and Test Cases with validation"""
        tasks = []
        test_cases = []
        
        try:
            # Process tasks
            tasks_data = llm_output.get("tasks", [])
            for task_data in tasks_data:
                task_data["user_story_id"] = story_id
                task_obj = Task(**task_data)
                tasks.append(task_obj)
                logger.info(f"Structured task: {task_obj.title}")
            
            # Process test cases
            tests_data = llm_output.get("test_cases", [])
            for test_data in tests_data:
                test_data["user_story_id"] = story_id
                test_obj = TestCase(**test_data)
                test_cases.append(test_obj)
                logger.info(f"Structured test case: {test_obj.title}")
            
            return tasks, test_cases
        
        except ValidationError as e:
            logger.error(f"Task/Test validation failed: {e}")
            raise ValueError(f"Invalid task/test structure: {e}")
    
    @staticmethod
    def validate_consistency(epic: Epic, features: list[Feature], 
                           stories: list[UserStory]) -> bool:
        """Validate consistency across artifacts"""
        try:
            # Check that all features reference the epic
            for feature in features:
                if feature.epic_id != epic.id:
                    logger.warning(f"Feature {feature.id} references different epic")
            
            # Check that all stories reference existing features
            feature_ids = {f.id for f in features}
            for story in stories:
                if story.feature_id not in feature_ids:
                    logger.warning(f"Story {story.id} references non-existent feature")
            
            logger.info("Consistency validation passed")
            return True
        
        except Exception as e:
            logger.error(f"Consistency validation failed: {e}")
            return False
