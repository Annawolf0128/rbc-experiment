from os import environ

SESSION_CONFIGS = [
    dict(
        name='rbc_preview',
        display_name='RBC: solo design preview (n=1, walk through every page)',
        app_sequence=['rbc'],
        num_demo_participants=1,
        penalty=20,
    ),
    dict(
        name='rbc_small_low',
        display_name='RBC: small group (n=5), low penalty (L=20)',
        app_sequence=['rbc'],
        num_demo_participants=5,
        penalty=20,
    ),
    dict(
        name='rbc_small_high',
        display_name='RBC: small group (n=5), high penalty (L=40)',
        app_sequence=['rbc'],
        num_demo_participants=5,
        penalty=40,
    ),
    dict(
        name='rbc_large_low',
        display_name='RBC: large group (n=15), low penalty (L=20)',
        app_sequence=['rbc'],
        num_demo_participants=15,
        penalty=20,
    ),
    dict(
        name='rbc_large_high',
        display_name='RBC: large group (n=15), high penalty (L=40)',
        app_sequence=['rbc'],
        num_demo_participants=15,
        penalty=40,
    ),
]

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00,
    participation_fee=5.00,
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
