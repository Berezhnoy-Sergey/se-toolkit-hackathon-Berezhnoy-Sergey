from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App settings
    app_name: str = "TaskFlow"
    debug: bool = False
    
    # Server settings
    address: str = "0.0.0.0"
    port: int = 8000
    
    # CORS
    cors_origins: list[str] = ["*"]
    
    # JWT Secret (change in production!)
    jwt_secret_key: str = "your-secret-key-change-in-production"
    
    # Database
    db_url: str = Field(
        default="postgresql://taskflow:taskflow_password@localhost:5432/taskflow",
        alias="DATABASE_URL"
    )


settings = Settings.model_validate({})
