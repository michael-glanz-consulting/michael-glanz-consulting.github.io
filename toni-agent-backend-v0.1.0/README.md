# Toni Agent Backend

Technisches Grundsystem für **Toni**, den koordinierenden KI-Transformationsagenten,
und seine Fachagenten. Das Projekt stellt eine HTTP-API bereit und enthält zunächst
keine Benutzeroberfläche.

## Was die erste Version kann

- Toni nimmt eine Projektfrage über `POST /v1/runs` entgegen.
- Toni kann ausgewählte Fachagenten als Werkzeuge beauftragen.
- Fachbewertungen werden von Toni zu einer Gesamteinschätzung zusammengeführt.
- Michael bleibt die letzte Entscheidungsinstanz.
- Externe, destruktive oder kostenwirksame Aktionen benötigen eine ausdrückliche Freigabe.
- `GET /v1/agents` liefert das aktuelle Rollenverzeichnis.
- `GET /health` dient der Betriebsprüfung.

## Enthaltene Rollen

| Agent | Verantwortung |
| --- | --- |
| Toni | Koordination, Synthese und Entscheidungsvorlage |
| Tilo | Finanzen, Wirtschaftlichkeit und Geschäftsmodell |
| Tim | Technik, Systemarchitektur und Umsetzbarkeit |
| Jan | Datenschutz, Informationssicherheit und Compliance |
| Pia | Beschlüsse, Entscheidungslogik und Dokumentation |
| Marika | Gestaltung, Nutzererlebnis und Kommunikation |
| Ben | Markt, Partner und operative Skalierung |

Die Rollen sind in `src/toni_backend/role_catalog.py` zentral beschrieben und können
ohne Änderung der API erweitert werden.

## Lokaler Start

Voraussetzungen: Python 3.11 oder neuer und ein eigener OpenAI-API-Schlüssel.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Danach `OPENAI_API_KEY` in `.env` eintragen und starten:

```bash
uvicorn toni_backend.main:app --reload
```

API-Dokumentation: `http://127.0.0.1:8000/docs`

## Beispielaufruf

```bash
curl -X POST http://127.0.0.1:8000/v1/runs \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bewerte ein KI-Erlebnisraum-Konzept für Handwerksbetriebe.",
    "project_context": {
      "zielgruppe": "Jugendliche der Klassen 7 bis 10",
      "region": "NRW"
    },
    "requested_specialists": ["tim", "jan", "ben"]
  }'
```

Wird `requested_specialists` weggelassen, stehen Toni alle Fachagenten zur Verfügung.

## Tests

```bash
pytest
ruff check .
```

Die mitgelieferten Tests benötigen keinen API-Schlüssel. Ein echter Modellaufruf wird
bewusst erst ausgeführt, wenn lokal ein Schlüssel hinterlegt ist.

## Docker

```bash
docker build -t toni-agent-backend .
docker run --rm -p 8000:8000 --env-file .env toni-agent-backend
```

## Sicherheitsregeln

- `.env` ist von Git ausgeschlossen.
- API-Schlüssel niemals per Chat, E-Mail oder Commit weitergeben.
- Das Backend führt in dieser Version keine externen Schreibaktionen aus.
- Vor einer öffentlichen Bereitstellung müssen Authentifizierung, Rate Limits,
  Protokollierungs- und Löschkonzept ergänzt werden.

## Nächste sinnvolle Ausbaustufen

1. Organisations- und Unternehmensverfassung als versionierte Wissensbasis einbinden.
2. Projektzustand und Beschlüsse in einer Datenbank speichern.
3. Freigabeprozess für Michael technisch erzwingen.
4. Authentifizierung und rollenbasierte Rechte ergänzen.
5. Evaluationsfälle für Qualität, Kosten und Laufzeit aufbauen.

