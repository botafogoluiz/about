import anthropic
from django.conf import settings

MODEL = "claude-haiku-4-5-20251001"

HTML_SYSTEM_PROMPT = (
    "Translate the following content from Brazilian Portuguese to English. "
    "The content is an HTML fragment. Preserve every HTML tag, attribute, and "
    "the overall structure exactly as-is -- translate only the human-readable "
    "text nodes. Do not add, remove, or reorder tags, and do not add any "
    "commentary. Reply with the translated HTML only, nothing else."
)

TEXT_SYSTEM_PROMPT = (
    "Translate the following content from Brazilian Portuguese to English. "
    "Preserve line breaks and whitespace exactly as given. Reply with the "
    "translated text only -- no preamble, no quotes, no explanation."
)


def translate_pt_to_en(text, is_html=False):
    """Translate a single field's value from pt-BR to English via Claude."""
    if not text or not text.strip():
        return ""

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    system_prompt = HTML_SYSTEM_PROMPT if is_html else TEXT_SYSTEM_PROMPT

    message = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": text}],
    )
    return "".join(block.text for block in message.content if block.type == "text").strip()
