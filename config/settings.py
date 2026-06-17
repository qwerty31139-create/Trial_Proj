from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # Azure OpenAI
    azure_openai_api_key: str
    azure_openai_endpoint: str
    azure_openai_deployment_name: str = "gpt-4"
    
    # Azure DevOps
    ado_organization: str
    ado_project: str
    ado_pat: str
    
    # Database
    database_url: str
    
    # Cosmos DB (optional)
    cosmos_db_endpoint: Optional[str] = None
    cosmos_db_key: Optional[str] = None
    
    # Application
    environment: str = "development"
    log_level: str = "INFO"
    debug: bool = False
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    return Settings()
