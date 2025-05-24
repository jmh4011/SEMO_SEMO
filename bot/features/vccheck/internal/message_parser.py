import re
from discord import Interaction

MESSAGE_URL_REGEX = re.compile(r"https://discord(?:app)?\.com/channels/\d+/(\d+)/(\d+)")


def parse_message(interaction: Interaction, raw: str) -> tuple[int, int]:

    try:
        if raw.startswith("https://"):
            parts = raw.strip("/").split("/")
            message_id = int(parts[-1])
            channel_id = int(parts[-2])
        elif "-" in raw:
            channel_id, message_id = map(int, raw.split("-"))
        else:
            message_id = int(raw)
            channel_id = interaction.channel.id
        return channel_id, message_id
    except Exception:
        raise ValueError("올바른 메시지 링크, ID 또는 채널ID-메시지ID 형식이 아닙니다.")
