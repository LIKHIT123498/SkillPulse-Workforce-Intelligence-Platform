from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME:str="SkillPulse- Workforce Intelligence Platform"
    API_V1_STR:str="/api/v1"

    DATABASE_URL: str="sqlite:///./skillpulse.db"
    model_config=SettingsConfigDict(env_file=".env",case_sensitive=True)

settings=Settings()
