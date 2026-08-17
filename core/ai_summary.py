import anthropic
from django.conf import settings
from django.utils import translation

from timeline.models import Education, Experience, Language

MODEL = "claude-opus-5"

# Internal lang codes used by this module ("en"/"pt_br", matching modeltranslation's
# field suffixes) vs. the Django locale identifiers translation.override() expects.
DJANGO_LOCALE = {"en": "en", "pt_br": "pt-br"}

SYSTEM_PROMPT = {
    "en": (
        "You are drafting a professional summary paragraph for a personal resume "
        "website, based ONLY on the structured career data provided below. Write "
        "1-2 short paragraphs (roughly 80-150 words), confident and natural "
        "professional tone. Do not invent any skill, employer, achievement, or "
        "metric that isn't present in the data. Some employers are marked as "
        "confidential -- for those, use the given substitute description instead "
        "of any real company name. Reply with the summary text only: no preamble, "
        "no headings, no quotes."
    ),
    "pt_br": (
        "Você está redigindo um parágrafo de resumo profissional para um site de "
        "currículo pessoal, baseado SOMENTE nos dados de carreira estruturados "
        "abaixo. Escreva 1-2 parágrafos curtos (aproximadamente 80-150 palavras), "
        "em português do Brasil natural e fluente, tom profissional e confiante. "
        "Não invente nenhuma habilidade, empregador, conquista ou número que não "
        "esteja presente nos dados. Alguns empregadores estão marcados como "
        "confidenciais -- para esses, use a descrição substituta fornecida em vez "
        "do nome real da empresa. Responda apenas com o texto do resumo: sem "
        "preâmbulo, sem títulos, sem aspas."
    ),
}


def _field(obj, name, lang):
    return getattr(obj, f"{name}_{lang}") or ""


def _build_context(lang):
    sections = []

    exp_lines = []
    for exp in Experience.objects.all().order_by("-start_date"):
        title = _field(exp, "title", lang)
        company_description = _field(exp, "company_description", lang)
        company = company_description if exp.redact_company_name else exp.company_name
        description = _field(exp, "description", lang)
        start = exp.start_date.strftime("%Y-%m")
        end = exp.end_date.strftime("%Y-%m") if exp.end_date else "present"
        exp_lines.append(f"- {title} @ {company} ({start} .. {end})\n  {description}")
    sections.append("EXPERIENCE:\n" + ("\n".join(exp_lines) if exp_lines else "(none)"))

    edu_lines = []
    for edu in Education.objects.all().order_by("-start_date"):
        degree = _field(edu, "degree", lang)
        field_of_study = _field(edu, "field_of_study", lang)
        institution = _field(edu, "institution", lang)
        edu_lines.append(f"- {degree}, {field_of_study} -- {institution}")
    sections.append("EDUCATION:\n" + ("\n".join(edu_lines) if edu_lines else "(none)"))

    lang_lines = []
    with translation.override(DJANGO_LOCALE[lang]):
        for item in Language.objects.all():
            name = _field(item, "name", lang)
            proficiency = item.get_proficiency_display()
            lang_lines.append(f"- {name}: {proficiency}")
    sections.append("LANGUAGES:\n" + ("\n".join(lang_lines) if lang_lines else "(none)"))

    return "\n\n".join(sections)


def generate_profile_summary():
    """Draft a fresh EN + PT-BR professional summary from real Experience,
    Education, and Language records. Each language is generated natively
    from that language's own stored content -- not a translation of the
    other -- so both read naturally.
    """
    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    result = {}
    for lang in ("en", "pt_br"):
        context = _build_context(lang)
        message = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT[lang],
            messages=[{"role": "user", "content": context}],
        )
        result[f"summary_{lang}"] = "".join(
            block.text for block in message.content if block.type == "text"
        ).strip()
    return result
