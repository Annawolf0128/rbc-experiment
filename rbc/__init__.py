from otree.api import *
import random

# All tunable parameters live in params.py — edit there, not here.
from params import ENDOWMENT, COST_DIVISOR, NUM_ROUNDS, PENALTY_LOW


doc = """
Reversed Beauty Contest. Each round players choose a number x in [0, 100]; cost is
x^2/k; a fixed penalty L is paid by anyone whose x is strictly below the group median.
2x2 treatment design (group size x penalty) selected via session config. Comprehension
quiz at start; SOEP risk Likert in exit survey; payment is the show-up fee plus the
earnings of one randomly selected round.
"""


class C(BaseConstants):
    NAME_IN_URL = 'rbc'
    PLAYERS_PER_GROUP = None  # all participants in one group; size = num_participants
    NUM_ROUNDS = NUM_ROUNDS
    ENDOWMENT = ENDOWMENT
    K = COST_DIVISOR


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            p.participant.paid_round = random.randint(1, C.NUM_ROUNDS)


class Group(BaseGroup):
    median_x = models.FloatField()


class Player(BasePlayer):
    x_choice = models.IntegerField(
        min=0, max=100,
        label='Choose a number between 0 and 100',
    )
    cost = models.FloatField(initial=0)
    penalty_paid = models.FloatField(initial=0)
    round_payoff = models.FloatField(initial=0)

    quiz_below_median = models.StringField(
        choices=[
            ('yes', 'Yes — you pay a penalty.'),
            ('no', 'No — you pay no penalty.'),
        ],
        label="If your number is strictly below the group median, do you pay a penalty?",
        widget=widgets.RadioSelect,
    )
    quiz_match_median = models.StringField(
        choices=[
            ('penalty', 'Yes — you pay the penalty.'),
            ('no_penalty', 'No — you pay no penalty.'),
            ('half', 'You pay half the penalty.'),
        ],
        label="If your number equals the group median exactly, do you pay a penalty?",
        widget=widgets.RadioSelect,
    )
    quiz_cost = models.StringField(
        choices=[
            ('higher', 'A higher number costs more.'),
            ('lower', 'A lower number costs more.'),
            ('same', 'All numbers have the same cost.'),
        ],
        label="How does the number you choose affect your cost?",
        widget=widgets.RadioSelect,
    )

    survey_risk = models.IntegerField(
        min=0, max=10,
        label=(
            "Q1. How would you rate your willingness to take risks in general? "
            "(0 = completely unwilling, 10 = fully prepared to take risks)"
        ),
        blank=True,
    )
    survey_strategy = models.LongStringField(
        label="Q2. What was your main reasoning when choosing a number each round?",
        blank=True,
    )
    survey_use_median = models.StringField(
        choices=[
            ('always', 'Always'),
            ('sometimes', 'Sometimes'),
            ('no_fixed', 'No fixed strategy'),
            ('ignored', "No, I ignored it"),
        ],
        label="Q3. Did you use the previous round's median as a reference?",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_best = models.StringField(
        choices=[
            ('all_zero', 'Everyone chooses 0'),
            ('middle', 'Middle values (~50)'),
            ('high', 'High values'),
            ('unsure', 'Unsure'),
        ],
        label="Q4. What do you think was the best outcome for the group?",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_gender = models.StringField(
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('nonbinary', 'Non-binary'),
            ('prefer_not', 'Prefer not to say'),
        ],
        label="Q5. Gender",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_prior_bc = models.StringField(
        choices=[
            ('yes', 'Yes'),
            ('no', 'No'),
            ('unsure', 'Unsure'),
        ],
        label="Q6. Have you participated in a Beauty Contest experiment before?",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_game_theory = models.StringField(
        choices=[
            ('formal', 'Formal course'),
            ('self_study', 'Self-study'),
            ('no', 'No'),
        ],
        label="Q7. Have you studied game theory or experimental economics?",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_age = models.StringField(
        choices=[(str(a), str(a)) for a in range(17, 30)] + [('30+', '30 or above')],
        label="Q8. Age",
        blank=True,
    )


def set_payoffs(group: Group):
    L = group.session.config.get('penalty', PENALTY_LOW)
    players = group.get_players()
    sorted_choices = sorted([p.x_choice for p in players])
    n = len(sorted_choices)
    if n % 2 == 1:
        median = float(sorted_choices[n // 2])
    else:
        median = (sorted_choices[n // 2 - 1] + sorted_choices[n // 2]) / 2.0
    group.median_x = median
    for p in players:
        p.cost = (p.x_choice ** 2) / C.K
        p.penalty_paid = float(L) if p.x_choice < median else 0.0
        p.round_payoff = C.ENDOWMENT - p.cost - p.penalty_paid


# ============ Pages ============

class Consent(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            L=player.session.config.get('penalty', PENALTY_LOW),
            E=C.ENDOWMENT,
            K=C.K,
            n=player.session.num_participants,
            num_rounds=C.NUM_ROUNDS,
        )


class Quiz(Page):
    form_model = 'player'
    form_fields = ['quiz_below_median', 'quiz_match_median', 'quiz_cost']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        correct = dict(
            quiz_below_median='yes',
            quiz_match_median='no_penalty',
            quiz_cost='higher',
        )
        wrong = [k for k, v in correct.items() if values.get(k) != v]
        if wrong:
            return f"You got {len(wrong)} answer(s) wrong. Please re-read the rules and try again."

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            L=player.session.config.get('penalty', PENALTY_LOW),
            E=C.ENDOWMENT,
            K=C.K,
        )


class Choice(Page):
    form_model = 'player'
    form_fields = ['x_choice']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            L=player.session.config.get('penalty', PENALTY_LOW),
            E=C.ENDOWMENT,
            K=C.K,
            round_number=player.round_number,
            num_rounds=C.NUM_ROUNDS,
        )


class WaitForGroup(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        median = player.group.median_x
        return dict(
            x=player.x_choice,
            cost=round(player.cost, 2),
            median=int(median) if median == int(median) else round(median, 1),
            below_median=player.x_choice < median,
            penalty=int(player.penalty_paid),
            round_payoff=round(player.round_payoff, 2),
            E=C.ENDOWMENT,
            K=C.K,
            L=player.session.config.get('penalty', PENALTY_LOW),
            round_number=player.round_number,
            num_rounds=C.NUM_ROUNDS,
            is_last_round=player.round_number == C.NUM_ROUNDS,
        )


class Survey(Page):
    form_model = 'player'
    form_fields = [
        'survey_risk',
        'survey_strategy',
        'survey_use_median',
        'survey_best',
        'survey_gender',
        'survey_prior_bc',
        'survey_game_theory',
        'survey_age',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS


class Payment(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        paid_round = player.participant.paid_round
        paid_player = player.in_round(paid_round)
        paid_amount = paid_player.round_payoff
        player.payoff = paid_amount
        fee = player.session.config.get('participation_fee', 0)
        return dict(
            paid_round=paid_round,
            paid_amount=round(paid_amount, 2),
            participation_fee=fee,
            total=round(paid_amount + fee, 2),
        )


page_sequence = [
    Consent,
    Instructions,
    Quiz,
    Choice,
    WaitForGroup,
    Results,
    Survey,
    Payment,
]
