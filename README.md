# Reversed Beauty Contest — oTree repository (US site)

This repository contains the US-site oTree project for the Reversed Beauty Contest experiment.

| Project | Venue | Official session plan |
|---|---|---|
| [`site1_US/`](site1_US/) | Site 1 — US | Six arm-specific configs; target 15 per session |

The China deployment lives in its own repository:
[**Rat-Race_Site1_China**](https://github.com/Annawolf0128/Rat-Race_Site1_China)
(Chinese interface, RMB payment, deployment manual in Chinese).

## Treatment coverage

The project implements six arms:

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
