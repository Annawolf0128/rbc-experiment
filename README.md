# Reversed Beauty Contest — two-site oTree repository

This repository contains two independent oTree projects for the same Reversed Beauty Contest experiment. Participant-facing pages, experimental rules, payoff calculations, survey questions, payment parameters, and the 20-round structure are identical across sites. Only the official-session recruitment and group-assignment plan differs.

| Project | Venue | Official session plan | Participants covering all six arms |
|---|---|---|---:|
| [`site1_US/`](site1_US/) | Site 1 — US | Six arm-specific configs: three 5-person sessions and three 15-person sessions | 60 |
| [`site2_Singapore/`](site2_Singapore/) | Site 2 — Singapore | Three 20-person configs; each forms one group of 15 and one group of 5 | 60 |

## Treatment coverage

Both projects implement the same six arms:

1. Small–Low: group size 5, penalty 20, no belief elicitation
2. Small–High: group size 5, penalty 40, no belief elicitation
3. Large–Low: group size 15, penalty 20, no belief elicitation
4. Large–High: group size 15, penalty 40, no belief elicitation
5. Small–Low–Belief: group size 5, penalty 20, belief elicitation
6. Large–Low–Belief: group size 15, penalty 20, belief elicitation

Site 1 runs these as six separate configurations. Site 2 pairs the small and large groups within the same penalty/belief condition, so three sessions cover all six arms.

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
