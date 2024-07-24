import os


class Settings:
    ANTHROPIC_API_KEY: str = os.getenv(key="ANTHROPIC_API_KEY", default="")
    OPENAI_API_KEY: str = os.getenv(key="OPENAI_API_KEY", default="")
    OPENAI_ORG_ID: str = os.getenv(key="OPENAI_ORG_ID", default="")
