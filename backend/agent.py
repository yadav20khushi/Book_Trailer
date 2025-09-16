from letta_client import Letta, MessageCreate, TextContent
from config import settings
from urllib.parse import urlparse
import json

client = Letta(
    project=settings.LETTA_PROJECT,
    token=settings.LETTA_API_KEY,
)

def _is_http_url(s: str) -> bool:
    pr = urlparse(s)
    return pr.scheme in ("http", "https") and bool(pr.netloc)

def send_book_details_to_letta(desc: str) -> str:
    response = client.agents.messages.create(
        agent_id=settings.AGENT_ID,
        messages=[MessageCreate(role="user", content=[TextContent(text=desc)])],
        max_steps=1,
        include_return_message_types=["assistant_message"],
    )

    assistant_text = ""
    for m in getattr(response, "messages", []):
        if getattr(m, "role", "") == "assistant":
            # Collect text parts only
            content = getattr(m, "content", "")
            if isinstance(content, str):
                assistant_text = content.strip()
            elif isinstance(content, list):
                parts = []
                for c in content:
                    t = getattr(c, "text", None)
                    if t:
                        parts.append(t)
                if parts:
                    assistant_text = " ".join(parts).strip()

    if not assistant_text:
        return "error generating trailer"

    video_url = None
    try:
        data = json.loads(assistant_text)
        if isinstance(data, dict) and "video_url" in data and isinstance(data["video_url"], str):
            if _is_http_url(data["video_url"]):
                return data["video_url"]
    except json.JSONDecodeError:
        pass

    if _is_http_url(assistant_text):
        return assistant_text

    return "error generating trailer"
