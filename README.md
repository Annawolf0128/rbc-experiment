# rbc-experiment

oTree implementation of the Reversed Beauty Contest (RBC) experiment.

Each round, participants choose an integer in `[0, 100]`. Higher numbers cost more (cost = x²/k). A fixed penalty `L` is paid by anyone whose choice is **strictly below the group median**. The combination of cost and below-median penalty creates a "match-or-quit" best response and a continuum of symmetric equilibria.

## Quick start

```bash
git clone https://github.com/Annawolf0128/rbc-experiment.git
cd rbc-experiment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
otree devserver
```

Open http://localhost:8000/demo/ in a browser. For multi-player testing, open additional incognito windows to the same demo URL.

> Requires Python 3.9 (use a 3.9 venv specifically; oTree 5.x is not compatible with 3.10+ until you upgrade to oTree 6.x).

## Treatment configurations

| Config | n | L | x̄ = √(Lk) | Purpose |
|---|---|---|---|---|
| `rbc_preview`    |  1 | 20 | 63.2 | Solo design preview, walks every page |
| `rbc_small_low`  |  5 | 20 | 63.2 | Small group, low penalty |
| `rbc_small_high` |  5 | 40 | 89.4 | Small group, high penalty |
| `rbc_large_low`  | 15 | 20 | 63.2 | Large group, low penalty |
| `rbc_large_high` | 15 | 40 | 89.4 | Large group, high penalty |

Shared parameters: endowment `E = 100`, cost denominator `k = 200`, `T = 12` rounds.

## Page flow

```
Consent → Instructions → Quiz (3-question comprehension check)
       → 12 × (Choice → WaitForGroup → Results)
       → Survey (SOEP risk Likert + 7 strategy / demographics items)
       → Payment (show-up fee + one randomly selected round's earnings)
```

## Project layout

```
rbc-experiment/
├── settings.py          # SESSION_CONFIGS, participation fee, currency
├── requirements.txt     # otree>=5.10,<6
├── _static/             # Required by oTree (empty placeholder)
├── _templates/          # Required by oTree (empty placeholder)
└── rbc/
    ├── __init__.py      # Constants C, Subsession, Group, Player, page_sequence
    ├── Consent.html     # Placeholder consent screen
    ├── Instructions.html
    ├── Quiz.html        # Comprehension check (must answer correctly to proceed)
    ├── Choice.html      # Slider 0–100 with live cost panel
    ├── Results.html     # Round-end feedback
    ├── Survey.html      # Post-experiment survey
    └── Payment.html     # Final payment summary
```

## Launching

### Development

```
otree devserver
```

The dev server includes a debug panel and auto-reloads on code changes. Not for real participants.

### Production / real sessions

```
otree prodserver
```

Then log in at http://localhost:8000/sessions, create a session, and distribute the unique `SessionStartLink` URLs to the participants. After the session ends, export data from http://localhost:8000/export.

For a public URL (so remote participants can join), deploy via [oTree Hub](https://www.otreehub.com), Heroku, Render, or an equivalent platform — `localhost` is only reachable from the host machine.

## Implementation notes

- `C.PLAYERS_PER_GROUP = None`, so every participant in a session is placed in a single group; group size is controlled by `num_participants` per session.
- The randomly paid round is drawn once in `creating_session()` and stored on `participant.paid_round`, independent of in-session behaviour.
- The consent page body is intentionally a placeholder. Replace the text in `rbc/Consent.html` with the institution-specific consent statement (purpose, voluntary participation, data use, contact, ethics ID) before any real run.
