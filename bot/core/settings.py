from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List
from pydantic import Field


class Settings(BaseSettings):
    discord_token: str = Field(..., alias="DISCORD_TOKEN")
    env: str = Field(..., alias="ENV")
    log_level: str = Field(..., alias="LOG_LEVEL")
    guild_ids: List[int] = Field([], alias="GUILD_IDS")

    @field_validator("guild_ids", mode="before")
    @classmethod
    def split_ids(cls, v):
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",")]
        return v

    model_config = {"env_file": ".env", "case_sensitive": False}


settings = Settings()
