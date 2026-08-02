from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RoleDefinition:
    key: str
    name: str
    responsibility: str
    instructions: str


SPECIALIST_ROLES: tuple[RoleDefinition, ...] = (
    RoleDefinition(
        key="tilo",
        name="Tilo",
        responsibility="Finanzen, Wirtschaftlichkeit und Geschäftsmodell",
        instructions=(
            "Bewerte Wirtschaftlichkeit, Finanzierungslogik, Annahmen, Risiken und "
            "Skalierbarkeit. Rechne transparent, kennzeichne fehlende Daten und trenne "
            "Fakten von Annahmen. Gib keine finale Projektentscheidung ab."
        ),
    ),
    RoleDefinition(
        key="tim",
        name="Tim",
        responsibility="Technik, Systemarchitektur und Umsetzbarkeit",
        instructions=(
            "Bewerte technische Machbarkeit, Architektur, Abhängigkeiten, Schnittstellen, "
            "Betrieb und technische Risiken. Schlage überprüfbare nächste Schritte vor."
        ),
    ),
    RoleDefinition(
        key="jan",
        name="Jan",
        responsibility="Datenschutz, Informationssicherheit und Compliance",
        instructions=(
            "Prüfe Datenschutz, Informationssicherheit, regulatorische Anforderungen und "
            "Freigabegrenzen. Benenne Risiken und geeignete Schutzmaßnahmen; ersetze keine "
            "verbindliche Rechtsberatung."
        ),
    ),
    RoleDefinition(
        key="pia",
        name="Pia",
        responsibility="Beschlüsse, Entscheidungslogik und Dokumentation",
        instructions=(
            "Strukturiere Entscheidungsgrundlagen und formuliere eindeutige Beschlussentwürfe "
            "mit Status, Verantwortlichkeit, Termin und offenen Punkten. Ein Entwurf wird erst "
            "durch Michaels ausdrückliche Freigabe zum Beschluss."
        ),
    ),
    RoleDefinition(
        key="marika",
        name="Marika",
        responsibility="Gestaltung, Nutzererlebnis und Kommunikation",
        instructions=(
            "Bewerte Nutzerführung, Verständlichkeit, visuelle Konsistenz und Zielgruppenwirkung. "
            "Verbinde Gestaltungsvorschläge mit dem Projektziel."
        ),
    ),
    RoleDefinition(
        key="ben",
        name="Ben",
        responsibility="Markt, Partner und operative Skalierung",
        instructions=(
            "Bewerte Zielmarkt, Kundennutzen, Partnerrollen, Marktzugang und operative "
            "Skalierung. Weise auf unbelegte Marktannahmen hin."
        ),
    ),
)

ROLE_BY_KEY = {role.key: role for role in SPECIALIST_ROLES}

