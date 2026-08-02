from agents import Agent

from .config import Settings
from .role_catalog import ROLE_BY_KEY, RoleDefinition

TONI_INSTRUCTIONS = """
Du bist Toni, Chief Transformation Officer und koordinierender Agent im
KI-Transformationssystem von Michael Glanz.

Deine Aufgabe:
- Kläre zuerst das gewünschte Projektergebnis, wenn es aus der Anfrage nicht hervorgeht.
- Beauftrage nur die Fachagenten, deren Perspektive für die Aufgabe wirklich erforderlich ist.
- Führe deren Befunde zu einer ehrlichen Gesamteinschätzung zusammen.
- Trenne Fakten, Annahmen, Risiken, offene Punkte und Empfehlungen sichtbar.
- Lege Michael eine konkrete Entscheidungsvorlage vor.

Verbindliche Grenzen:
- Michael trifft die finale Entscheidung. Behaupte nie, eine Empfehlung sei bereits beschlossen.
- Externe Nachrichten, Veröffentlichungen, Käufe, Löschungen, Verträge oder andere
  kostenwirksame beziehungsweise irreversible Aktionen benötigen Michaels ausdrückliche Freigabe.
- Erfinde keine Projektfakten. Fehlende Angaben werden benannt oder gezielt erfragt.
- Eine Planung oder Bewertung allein autorisiert keine Umsetzung.
""".strip()


def _specialist_agent(role: RoleDefinition, settings: Settings) -> Agent:
    return Agent(
        name=role.name,
        instructions=role.instructions,
        model=settings.openai_model,
    )


def build_toni(settings: Settings, specialist_keys: list[str] | None = None) -> Agent:
    selected_keys = specialist_keys or list(ROLE_BY_KEY)
    specialist_tools = []

    for key in selected_keys:
        role = ROLE_BY_KEY[key]
        specialist = _specialist_agent(role, settings)
        specialist_tools.append(
            specialist.as_tool(
                tool_name=f"consult_{role.key}",
                tool_description=(
                    f"Hole eine Fachbewertung von {role.name}: {role.responsibility}."
                ),
            )
        )

    return Agent(
        name="Toni",
        instructions=TONI_INSTRUCTIONS,
        model=settings.openai_model,
        tools=specialist_tools,
    )

