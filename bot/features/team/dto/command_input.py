from pydantic import BaseModel, Field, field_validator


class TeamCommandInput(BaseModel):
    user_id: int
    guild_id: int
    team_count: int = Field(gt=0, le=10, description="최소 1팀, 최대 10팀")

    @field_validator("team_count")
    @classmethod
    def validate_team_count(cls, v: int) -> int:
        if v < 1:
            raise ValueError("팀 수는 1 이상이어야 합니다.")
        return v
