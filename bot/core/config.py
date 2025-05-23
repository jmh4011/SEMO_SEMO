from pydantic import BaseSettings, Field
from typing import List

class Settings(BaseSettings):
    discord_token: str = Field(..., env="DISCORD_TOKEN")
    guild_ids: List[int] = Field(..., env="GUILD_IDS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# 전역 설정 인스턴스
settings = Settings()
