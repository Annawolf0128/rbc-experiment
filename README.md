# Reversed Beauty Contest — two-site oTree repository

This repository contains two independent oTree projects for the same Reversed Beauty Contest experiment. Participant-facing pages, experimental rules, payoff calculations, survey questions, payment parameters, and the 20-round structure are identical across sites. Only the official-session recruitment and group-assignment plan differs.

| Project | Venue | Official session plan | Participants covering all six arms |
|---|---|---|---:|
| [`site1_US/`](site1_US/) | Site 1 — US | Six arm-specific configs; target 15 per session, with small groups formed flexibly in blocks of 5 | 90 planned |
| [`site2_Singapore/`](site2_Singapore/) | Site 2 — Singapore | Six arm-specific configs; 10 planned 15-person sessions, with three groups in each main no-belief block | 150 planned |

## Treatment coverage

Both projects implement the same six arms:

1. Small–Low: group size 5, penalty 20, no belief elicitation
2. Small–High: group size 5, penalty 40, no belief elicitation
3. Large–Low: group size 15, penalty 20, no belief elicitation
4. Large–High: group size 15, penalty 40, no belief elicitation
5. Small–Low–Belief: group size 5, penalty 20, belief elicitation
6. Large–Low–Belief: group size 15, penalty 20, belief elicitation

Both sites run the six arms as separate session configurations. In Singapore, each official session recruits exactly 15 participants: a small-arm session forms three groups of 5, while a large-arm session forms one group of 15. The two no-belief large-group configurations are each run three times so that all four main no-belief blocks contain three groups; each belief configuration is run once.

## Running a project

Run commands from the site directory you intend to use. Each folder contains its own `settings.py`, `params.py`, `requirements.txt`, templates, and app code.

```bash
cd site1_US                 # or: cd site2_Singapore
python3.9 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
otree prodserver
```

Do not combine databases or participant links between the two site directories.
