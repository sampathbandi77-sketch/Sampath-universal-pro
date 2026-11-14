from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SAMPATH UNIVERSAL PRO API"
    app_env: str = "development"
    database_url: str = ""
    trading_mode: str = "paper"
    live_trading_enabled: bool = False
    auto_execution_enabled: bool = False
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
