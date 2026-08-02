# RBC experiment — Site 1 (US)

Site 1 (US) oTree implementation of the Reversed Beauty Contest (RBC) experiment. This version runs the six treatment arms in separate sessions, with a recruitment target of 15 participants per session.

Each round, participants choose an integer in `[0, 100]`. Higher numbers cost more (cost = x²/k). A fixed penalty `L` is paid by anyone whose choice is **strictly below the group median**. The combination of cost and below-median penalty creates a "match-or-quit" best response and a continuum of symmetric equilibria.

## Quick start

Python 3.9 is required. Run the commands for your operating system one at a time so that, if cloning or installation fails, later commands do not run in the wrong directory.

### macOS / Linux

```bash
git clone https://github.com/Annawolf0128/rbc-experiment.git
cd rbc-experiment/site1_US
python3.9 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
otree devserver
```

### Windows PowerShell

```powershell
git clone https://github.com/Annawolf0128/rbc-experiment.git
Set-Location rbc-experiment/site1_US
py -3.9 -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
otree devserver
```

If PowerShell blocks `Activate.ps1`, open Command Prompt in the repository and activate with `venv\Scripts\activate.bat` instead.

Open http://localhost:8000/demo/ after the server starts.

### Clone troubleshooting

If `git clone` reports an HTTP/2 framing error, retry it with HTTP/1.1:

```bash
git -c http.version=HTTP/1.1 clone https://github.com/Annawolf0128/rbc-experiment.git
```

If it still cannot connect to `github.com:443`, check the computer's VPN, firewall, or proxy settings. Proxy addresses are machine- and network-specific, so do not copy another user's localhost proxy address.

## Treatment configurations

| Config | Session grouping | L | Rounds | x̄ = √(Lk) | Purpose |
|---|---|---|---|---|---|
| `rbc_preview` | 1 | 20 | 2 | 63.2 | Solo quick test, no belief elicitation |
| `rbc_test_2p_2r` | 2 | 20 | 2 | 63.2 | 2-player quick test |
| `rbc_test_2p_2r_belief` | 2 | 20 | 2 | 63.2 | 2-player quick test with belief elicitation |
| `rbc_small_low` | 3 × 5 (15 total) | 20 | 20 | 63.2 | Three small groups, low penalty |
| `rbc_small_high` | 3 × 5 (15 total) | 40 | 20 | 89.4 | Three small groups, high penalty |
| `rbc_large_low` | 1 × 15 | 20 | 20 | 63.2 | One large group, low penalty |
| `rbc_large_high` | 1 × 15 | 40 | 20 | 89.4 | One large group, high penalty |
| `rbc_small_low_belief` | 3 × 5 (15 total) | 20 | 20 | 63.2 | Three small groups, low penalty, with belief elicitation |
| `rbc_large_low_belief` | 1 × 15 | 20 | 20 | 63.2 | One large group, low penalty, with belief elicitation |

Shared parameters: endowment `E = 100`, cost denominator `k = 200`, `T = 20` rounds by default.

## Page flow

```
Group formation wait page → Welcome → Consent → Instructions → Quiz
       → 20 × ([Belief, if enabled] → Choice → WaitForGroup → Results)
       → Survey (risk, strategy, median-use, and demographics items)
       → Payment (show-up fee + one randomly selected round's earnings)
```

## Project layout

```
site1_US/
├── settings.py          # SESSION_CONFIGS, participation fee, currency
├── requirements.txt     # otree>=5.10,<6
├── _static/             # Required by oTree (empty placeholder)
├── _templates/          # Required by oTree (empty placeholder)
└── rbc/
    ├── __init__.py      # Constants C, Subsession, Group, Player, page_sequence
    ├── Welcome.html     # Welcome / waiting screen
    ├── Consent.html     # Placeholder consent screen
    ├── Instructions.html
    ├── Quiz.html        # Comprehension check (must answer correctly to proceed)
    ├── Belief.html      # Optional belief elicitation page
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

- Site 1 targets 15 recruits per official session. A small-group treatment forms complete groups in blocks of 5 under the same treatment. With 15 participants it forms three groups; if only 12 attend, two groups of 5 can proceed and the remaining 2 do not participate. The experimenter should not send those 2 beyond the initial group-formation wait page and should handle any show-up compensation outside oTree. Large-group treatments still require exactly 15 participants. Once formed, group membership stays unchanged across rounds.
- Running all six Site 1 configurations at their 15-person recruitment targets uses 90 participants. Actual participation in a small-group session may be lower when attendance is not divisible by 5.
- The randomly paid round is drawn once in `creating_session()` and stored on `participant.paid_round`, independent of in-session behaviour.
- The consent page body is intentionally a placeholder. Replace the text in `rbc/Consent.html` with the institution-specific consent statement (purpose, voluntary participation, data use, contact, ethics ID) before any real run.
