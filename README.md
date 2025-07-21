# Projektstruktur

```
bewerbungsaufgabe/
├── backend/
│   ├── index.php           # Enthält handleAction() zum Verarbeiten von PHP-Requests
│   ├── phpunit.xml         # PHPUnit-Konfiguration
│   ├── tests/              # PHPUnit-Testcases
│   │   └── php_unit_Test.php
│   └── Dockerfile          # PHP-Image mit Apache & PHPUnit
├── falcon_framework/
│   ├── controller.py       # Falcon-API: mapped auf PHP-Routen
│   ├── index.html          # Frontend-Demo
│   ├── req.txt             # Python-Abhängigkeiten
│   ├── wsgi.py             # WSGI Entry Point
│   └── Dockerfile          # Python-Image mit Waitress
├── docker-compose.yml      # Multi-Container-Setup
└── README.md               # Diese Anleitung
```

---

## Setup

1. **Klonen oder Pullen**  
2. **Container starten & bauen:**

```bash
docker-compose up --build
```

3. **Frontend öffnen:**  
[http://localhost:8000/index.html](http://localhost:8000/index.html)

4. **Terminal beobachten:**  
    - Python → empfängt `/in`, `/hello`, `/whattimeisit` etc.  
    - PHP → verarbeitet die API-Logik über `index.php`

---

## Kommunikation

### Architekturüberblick:

```
Browser (index.html)
   ↓
Falcon (Python)
   ↓ REST API via HTTP
PHP (Apache)
```

- Die Falcon-Routen (`/in`, `/hello`, etc.) rufen intern `http://php/index.php?action=...` auf.
- PHP liefert JSON-Antworten zurück, z. B. `{"message": "It's half past 5 am"}`.

---

## PHPUnit-Tests (Unit)

```bash
docker-compose exec php phpunit
```

- Es werden **8 Tests** direkt gegen die PHP-Funktion `handleAction()` durchgeführt.

---

## Endpunkte

| Endpoint            | Methode | Beschreibung                                  |
|---------------------|---------|-----------------------------------------------|
| `/hello`            | GET     | Gibt „hello“ zurück                           |
| `/howareyou`        | GET     | Gibt „I'm fine“ zurück                        |
| `/whattimeisit`     | GET     | Ermittelt Zeitzone via IP → aktuelle Zeit     |
| `/in/{city}`        | GET     | Zeigt Zeit für die übergebene Stadt           |
| `/in`               | POST    | JSON `{"city": "Berlin"}` → Zeitantwort       |

---

## Abhängigkeiten

### Python

- Falcon, Waitress
- geopy, timezonefinder
- requests

### PHP

- PHP 8.4
- Apache
- PHPUnit 9.6

---

## Hinweis

- PHP läuft auf Port `8001`, Python (Falcon) auf `8000`
- Der Containername `php` wird von Falcon genutzt, um PHP via `http://php/` zu erreichen (siehe Docker-Netzwerk).

---

---

# Aufgabe:
Erstelle oder verwende einen existierenden Docker Container (Stack) der einen Webserver und PHP (oder eben anderweitiges Framework) bereitstellt und 
stelle damit eine kleine REST API bereit.

- freie Wahl des Frameworks oder Plain PHP
- Zeitangaben sind nicht statisch (hart codiert) sondern dynamisch 
- Zeitangabe im Format 10 to 3 pm statt hh:mm

- Endpunkte
/hello
{message:'hello'}
/howareyou
{message: 'I\'m fine'}
/whattimeisit

{message:'It\'s 10 to 4 pm'}

/in/
Variante 1 per GET timezone
london
Variante 2 per POST timezone
{city: 'london'}

{message:'It\'s 10 to 3 pm'} 


PHPUnit - Test
- wenn bekannt Test mit Codeception


Fleißaufgaben

- Authentifizeriung
- HTTP Basic Auth oder Token
