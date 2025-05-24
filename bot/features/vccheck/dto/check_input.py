from pydantic import BaseModel
from discord import Interaction
from typing import Optional


class VcCheckInput(BaseModel):
    channel_id: int
    message_id: int
    interaction: Optional[Interaction] = None

    model_config = {"arbitrary_types_allowed": True}

    @classmethod
    def from_interaction(cls, interaction: Interaction, raw: Optional[str]):
        from features.vccheck.internal.message_parser import parse_message

        if not raw:
            raise ValueError("메시지 링크 또는 ID를 입력하거나 답장을 지정해주세요.")
        channel_id, message_id = parse_message(interaction, raw)
        return cls(
            channel_id=channel_id, message_id=message_id, interaction=interaction
        )
