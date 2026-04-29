"""
Central parameter file for the Reversed Beauty Contest experiment.

EDIT VALUES HERE — settings.py and rbc/__init__.py both import from this file.
Restart `otree devserver` after editing for changes to take effect.
"""

# ============================================================
# Game parameters (shared across all treatments)
# ============================================================
ENDOWMENT     = 100      # E   each round starts with this many points
COST_DIVISOR  = 200      # k   cost = x^2 / k  (so x=100 costs 50, x=10 costs 0.5)
NUM_ROUNDS    = 12       # T   how many rounds per session

# ============================================================
# Treatment parameters
# ============================================================
PENALTY_LOW   = 20       # L   penalty for the "low penalty" treatments    -> xbar = sqrt(L*k) ~ 63.2
PENALTY_HIGH  = 40       # L   penalty for the "high penalty" treatments   -> xbar = sqrt(L*k) ~ 89.4

GROUP_SIZE_SMALL = 5     # n   participants per session in "small group" treatments (also used as num_demo_participants)
GROUP_SIZE_LARGE = 15    # n   participants per session in "large group" treatments

# ============================================================
# Payment parameters
# ============================================================
SHOW_UP_FEE         = 5.00    # USD paid to every participant who completes (regardless of choices)
CURRENCY_PER_POINT  = 1.00    # USD per 1 oTree point (so 1 point = $1.00)
