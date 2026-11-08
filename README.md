# Personal Digital Footprint Report

A passive OSINT project that helps a person find what is publicly visible about them online,
score the privacy and security risk, and track the improvement after fixing it.

> **Ethics:** use it only on yourself or someone who gave written consent. It uses public
> information only, never accesses private accounts, and makes no network requests.
> The sample data is fictional.

## What is included

| Part | Folder | Description |
|---|---|---|
| Web app | `web/` | Browser tool: consent, findings log, risk scoring, username links, redactor, dashboard, report |
| CLI tool | `cli/` | Python script to score, report, redact, list profile links and compare before/after |
| Sample data | `data/` | Fictional before and after findings |
| Tests | `tests/` | Unit tests for scoring and redaction |
| Docs | `docs/` | Methodology |

## Run the web app

Open `web/index.html` in Chrome. No install or sign-in is needed. Data stays in your browser.

## Run the CLI (Python 3.8+, no extra packages)

```bash
python cli/footprint.py score data/sample_before.json
python cli/footprint.py report data/sample_before.json -o report.md
python cli/footprint.py compare data/sample_before.json data/sample_after.json
python cli/footprint.py usernames krishna_sec22
echo "Mail a@b.com or call +91 98765 43210" | python cli/footprint.py redact
python -m unittest discover tests
```

## Scoring

Risk = Sensitivity x Discoverability x Exploitability, each scored 1 to 5.

| Rating | Score |
|---|---|
| Critical | 60+ |
| High | 30-59 |
| Medium | 12-29 |
| Low | under 12 |

Sample result: exposure fell from **37/100** to **12/100** after fixes.

## Data file format

```json
{ "subject": "Subject A", "consent": true,
  "findings": [{ "category": "Breach", "description": "Test email found in a data breach",
                 "source_url": "https://breachcheck.example/result",
                 "sensitivity": 4, "discoverability": 5, "exploitability": 5, "date": "2026-11-01" }] }
```

## Screenshots


### Screenshot 1
![Screenshot 1](docs/Screenshot%202026-11-06%20185315.png)

### Screenshot 2
![Screenshot 2](docs/Screenshot%202026-11-06%20185543.png)

### Screenshot 3 – Updated Report
![Screenshot 3](docs/FIRST_NEW_FILENAME.png)

### Screenshot 4 – Final Report
![Screenshot 4](docs/SECOND_NEW_FILENAME.png)

### Screenshot 5
![Screenshot 5](docs/Screenshot%202026-11-06%20185735.png)

### Screenshot 6
![Screenshot 6](docs/Screenshot%202026-11-06%20185805.png)

### Screenshot 7
![Screenshot 7](docs/Screenshot%202026-11-06%20185849.png)

## Author

BCA student, Internship project, 2026

## License

MIT
