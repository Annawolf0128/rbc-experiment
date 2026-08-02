from os import environ

# All tunable parameters live in params.py — edit there, not here.
from params import (
    PENALTY_LOW,
    PENALTY_HIGH,
    SESSION_SIZE,
    GROUP_SIZE_SMALL,
    GROUP_SIZE_LARGE,
    SHOW_UP_FEE,
    CURRENCY_PER_POINT,
)

SESSION_CONFIGS = [
    dict(
        name='rbc_preview',
        display_name='TEST: 1 player, 2 rounds, no belief',
        app_sequence=['rbc'],
        num_demo_participants=1,
        penalty=PENALTY_LOW,
        num_rounds=2,
        show_consent=False,
        show_welcome=True,
    ),
    dict(
        name='rbc_test_2p_2r',
        display_name='TEST: 2 players, 2 rounds, no belief',
        app_sequence=['rbc'],
        num_demo_participants=2,
        penalty=PENALTY_LOW,
        num_rounds=2,
        show_consent=True,
        show_welcome=True,
    ),
    dict(
        name='rbc_test_2p_2r_belief',
        display_name='TEST: 2 players, 2 rounds, belief elicitation',
        app_sequence=['rbc'],
        num_demo_participants=2,
        penalty=PENALTY_LOW,
        num_rounds=2,
        elicit_belief=True,
        show_consent=True,
        show_welcome=True,
    ),
    dict(
        name='rbc_site2_low',
        display_name=f'SITE 2: 20 participants (1 × {GROUP_SIZE_LARGE} + 1 × {GROUP_SIZE_SMALL}), low penalty (L={PENALTY_LOW}), no belief',
        app_sequence=['rbc'],
        num_demo_participants=SESSION_SIZE,
        expected_session_size=SESSION_SIZE,
        group_sizes=[GROUP_SIZE_LARGE, GROUP_SIZE_SMALL],
        penalty=PENALTY_LOW,
        show_consent=False,
        show_welcome=True,
    ),
    dict(
        name='rbc_site2_high',
        display_name=f'SITE 2: 20 participants (1 × {GROUP_SIZE_LARGE} + 1 × {GROUP_SIZE_SMALL}), high penalty (L={PENALTY_HIGH}), no belief',
        app_sequence=['rbc'],
        num_demo_participants=SESSION_SIZE,
        expected_session_size=SESSION_SIZE,
        group_sizes=[GROUP_SIZE_LARGE, GROUP_SIZE_SMALL],
        penalty=PENALTY_HIGH,
        show_consent=False,
        show_welcome=True,
    ),
    dict(
        name='rbc_site2_low_belief',
        display_name=f'SITE 2: 20 participants (1 × {GROUP_SIZE_LARGE} + 1 × {GROUP_SIZE_SMALL}), low penalty (L={PENALTY_LOW}), belief elicitation',
        app_sequence=['rbc'],
        num_demo_participants=SESSION_SIZE,
        expected_session_size=SESSION_SIZE,
        group_sizes=[GROUP_SIZE_LARGE, GROUP_SIZE_SMALL],
        penalty=PENALTY_LOW,
        elicit_belief=True,
        show_consent=False,
        show_welcome=True,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=CURRENCY_PER_POINT,
    participation_fee=SHOW_UP_FEE,
    doc='',
)

PARTICIPANT_FIELDS = ['paid_round']
SESSION_FIELDS = []

LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', '')

DEMO_PAGE_INTRO_HTML = """
<p>Reversed Beauty Contest — Site 2. Each official session recruits exactly 20 participants and forms one group of 15 plus one group of 5.</p>
"""

SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'rbc-dev-only-do-not-use-in-prod')

INSTALLED_APPS = ['otree']
