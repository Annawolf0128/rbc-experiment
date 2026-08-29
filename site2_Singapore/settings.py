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
        name='rbc_site2_small_low',
        display_name=f'SITE 2: 3 small groups (3 × {GROUP_SIZE_SMALL}), low penalty (L={PENALTY_LOW}), no belief — create 1 session',
        app_sequence=['rbc'],
        num_demo_participants=SESSION_SIZE,
        expected_session_size=SESSION_SIZE,
        group_size=GROUP_SIZE_SMALL,
        penalty=PENALTY_LOW,
        show_consent=False,
        show_welcome=True,
    ),
    dict(
        name='rbc_site2_small_high',
        display_name=f'SITE 2: 3 small groups (3 × {GROUP_SIZE_SMALL}), high penalty (L={PENALTY_HIGH}), no belief — create 1 session',
        app_sequence=['rbc'],
        num_demo_participants=SESSION_SIZE,
        expected_session_size=SESSION_SIZE,
        group_size=GROUP_SIZE_SMALL,
        penalty=PENALTY_HIGH,
        show_consent=False,
        show_welcome=True,
    ),
    dict(
        name='rbc_site2_large_low',
        display_name=f'SITE 2: 1 large group (1 × {GROUP_SIZE_LARGE}), low penalty (L={PENALTY_LOW}), no belief — create 3 sessions',
        app_sequence=['rbc'],
        num_demo_participants=SESSION_SIZE,
        expected_session_size=SESSION_SIZE,
        group_size=GROUP_SIZE_LARGE,
        penalty=PENALTY_LOW,
        show_consent=False,
        show_welcome=True,
    ),
    dict(
        name='rbc_site2_large_high',
        display_name=f'SITE 2: 1 large group (1 × {GROUP_SIZE_LARGE}), high penalty (L={PENALTY_HIGH}), no belief — create 3 sessions',
        app_sequence=['rbc'],
        num_demo_participants=SESSION_SIZE,
        expected_session_size=SESSION_SIZE,
        group_size=GROUP_SIZE_LARGE,
        penalty=PENALTY_HIGH,
        show_consent=False,
        show_welcome=True,
    ),
    dict(
        name='rbc_site2_small_low_belief',
        display_name=f'SITE 2: 3 small groups (3 × {GROUP_SIZE_SMALL}), low penalty (L={PENALTY_LOW}), belief elicitation — create 1 session',
        app_sequence=['rbc'],
        num_demo_participants=SESSION_SIZE,
        expected_session_size=SESSION_SIZE,
        group_size=GROUP_SIZE_SMALL,
        penalty=PENALTY_LOW,
        elicit_belief=True,
        show_consent=False,
        show_welcome=True,
    ),
    dict(
        name='rbc_site2_large_low_belief',
        display_name=f'SITE 2: 1 large group (1 × {GROUP_SIZE_LARGE}), low penalty (L={PENALTY_LOW}), belief elicitation — create 1 session',
        app_sequence=['rbc'],
        num_demo_participants=SESSION_SIZE,
        expected_session_size=SESSION_SIZE,
        group_size=GROUP_SIZE_LARGE,
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

ROOMS = [
    dict(
        name='sg_lab',
        display_name='Singapore Lab (15 seats)',
        # 固定候场室：实验室每台电脑书签设为
        #   http://<server>/room/sg_lab?participant_label=Seat01  （每台机器一个座位号）
        # 被试开机即候场；实验员人齐后在后台该 room 里 create session 即可开场。
        participant_label_file='_rooms/seats.txt',
        use_secure_urls=False,
    ),
]

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD', '')

DEMO_PAGE_INTRO_HTML = """
<p>Reversed Beauty Contest — Site 2. Each official session recruits exactly 15 participants and runs one treatment only: either three groups of 5 or one group of 15.</p>
"""

SECRET_KEY = environ.get('OTREE_SECRET_KEY', 'rbc-dev-only-do-not-use-in-prod')

INSTALLED_APPS = ['otree']
