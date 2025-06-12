from pydantic_settings import BaseSettings

class CoreConfig(BaseSettings):
    ENVIRONMENT: str
    SERVICE_NAME: str = "PROFILE_SEARCH_SERVICE"
    GROQ_API_KEY: str
    TAVILY_API_KEY: str

    # Model configurations
    GROQ_MODERATION_MODEL: str = "groq/llama-3.3-70b-versatile"
    GROQ_QUERY_DECOMPOSITION_MODEL: str = "groq/llama-3.3-70b-versatile"
    GENERAL_RESPONSE_MODEL: str = "groq/meta-llama/llama-4-maverick-17b-128e-instruct"
    PROFILE_RESPONSE_MODEL: str = "groq/meta-llama/llama-4-maverick-17b-128e-instruct"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


core_config = CoreConfig()
