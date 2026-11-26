# Manufacturing-Order

## Funktionen

- Benutzer erstellen, anzeigen und löschen
- Aufträge erstellen und anzeigen
- Aufträge in eine Warteschlange aufnehmen
- Warteschlange anzeigen und der Reihe nach abarbeiten
- Zugehörige Aufträge werden beim Löschen eines Benutzers entfernt

Auftragsdauer: 1 bis 120 Sekunden  
Maximale Scannerlaufzeit: 5 Minuten

## Voraussetzungen

- Python 3.10 oder neuer
- Keine externen Pakete

## Start

Im Projektordner ausführen:

```powershell
python main.py
```

Anschließend erscheint das Menü für die Verwaltung der Benutzer und Aufträge.

## Projektstruktur

```text
main.py                 Startpunkt der Anwendung
Business_logic/         Benutzer- und Auftragslogik
Helpers/                Menü, Scanner und JSON-Datenzugriff
models/                 Datenmodelle für Benutzer und Aufträge
DB_files/               Lokale JSON-Datenbanken
```

## Datenspeicherung

Die Anwendung speichert Daten in:

- `DB_files/user_DB.json`
- `DB_files/order_DB.json`

Die Dateien werden bei der ersten Speicherung automatisch erstellt.

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE).