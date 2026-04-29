from os import environ

# All tunable parameters live in params.py — edit there, not here.
from params import (
    PENALTY_LOW,
    PENALTY_HIGH,
    GROUP_SIZE_SMALL,
    GROUP_SIZE_LARGE,
    SHOW_UP_FEE,
    CURRENCY_PER_POINT,
)

SESSION_CONFIGS = [
    dict(
        name='rbc_preview',
        display_name='RBC: solo design preview (n=1, walk through every page)',
        app_sequence=['rbc'],
        num_demo_participants=1,
        penalty=PENALTY_LOW,
    ),
    dict(
        name='rbc_small_low',
        display_name=f'RBC: small group (n={GROUP_SIZE_SMALL}), low penalty (L={PENALTY_LOW})',
        app_sequence=['rbc'],
        num_demo_participants=GROUP_SIZE_SMALL,
        penalty=PENALTY_LOW,
    ),
    dict(
        name='rbc_small_high',
        display_name=f'RBC: small group (n={GROUP_SIZE_SMALL}), high penalty (L={PENALTY_HIGH})',
        app_sequence=['rbc'],
        num_demo_participants=GROUP_SIZE_SMALL,
        penalty=PENALTY_HIGH,
    ),
    dict(
        name='rbc_large_low',
        display_name=f'RBC: large group (n={GROUP_SIZE_LARGE}), low penalty (L={PENALTY_LOW})',
        app_sequence=['rbc'],
        num_demo_participants=GROUP_SIZE_LARGE,
        penalty=PENALTY_LOW,
    ),
    dict(
        name='rbc_large_high',
        display_name=f'RBC: large group (n={GROUP_SIZE_LARGE}), high penalty (L={PENALTY_HIGH})',
        app_sequence=['rbc'],
        num_demo_participants=GROUP_SIZE_LARGE,
        penalty=PENALTY_HIGH,
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
<p>Reversed Beauty Contest experiment. Use the demo links below to preview each treatment.</p>
"""

SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'rbc-dev-only-do-not-use-in-prod')

INSTALLED_APPS = ['otree']
