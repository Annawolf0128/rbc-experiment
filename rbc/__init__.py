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


def session_num_rounds(obj):
    return obj.session.config.get('num_rounds', C.NUM_ROUNDS)


def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        paid_round_max = session_num_rounds(subsession)
        for p in subsession.get_players():
            p.participant.paid_round = random.randint(1, paid_round_max)


class Group(BaseGroup):
    median_x = models.FloatField()


class Player(BasePlayer):
    consent_given = models.BooleanField(
        label="I agree to participate.",
        blank=True,  # validated in Consent.error_message instead, so we get a friendlier message
    )

    x_choice = models.IntegerField(
        min=0, max=100,
        label='Choose a number between 0 and 100',
    )
    belief_median = models.IntegerField(
        min=0, max=100,
        label='What do you think the group median will be in this round?',
        blank=True,
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
    quiz_equal_earnings = models.StringField(
        choices=[
            ('no_penalty_formula', '100 − x²/200'),
            ('penalty_formula', '100 − x²/200 − 20'),
            ('linear_formula', '100 − x − 20'),
        ],
        label=(
            "Suppose your number is x, the group median is y, and penalty = 20, with x = y. "
            "What are your earnings for the round?"
        ),
        widget=widgets.RadioSelect,
    )
    quiz_below_earnings = models.StringField(
        choices=[
            ('no_penalty_formula', '100 − x²/200'),
            ('penalty_formula', '100 − x²/200 − 20'),
            ('linear_formula', '100 − x − 20'),
        ],
        label=(
            "Suppose your number is x, the group median is y, and penalty = 20, with x < y. "
            "What are your earnings for the round?"
        ),
        widget=widgets.RadioSelect,
    )
    quiz_fixed_penalty = models.StringField(
        choices=[
            ('fixed', 'The penalty is the same fixed amount L.'),
            ('distance', 'The penalty is larger when x is farther below y.'),
            ('half', 'The penalty is half of L.'),
        ],
        label="If x < y, does the penalty depend on how far x is below y?",
        widget=widgets.RadioSelect,
    )

    survey_risk = models.IntegerField(
        choices=[(i, str(i)) for i in range(11)],
        min=0, max=10,
        label=(
            "Q1. How would you rate your willingness to take risks in general? "
            "(0 = not at all willing, 10 = very willing)"
        ),
        widget=widgets.RadioSelectHorizontal,
        blank=True,
    )
    survey_strategy = models.LongStringField(
        label="Q2. How did you decide which number to choose each round?",
        blank=True,
    )
    survey_use_median = models.StringField(
        choices=[
            ('always', 'Always'),
            ('sometimes', 'Sometimes'),
            ('no_fixed', 'No fixed strategy'),
            ('ignored', "No, I ignored it"),
        ],
        label="Q3. Did you use the previous round's median to help you make your decisions?",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_median_importance = models.StringField(
        choices=[
            ('very', 'Very important'),
            ('somewhat', 'Somewhat important'),
            ('not_much', 'Not very important'),
            ('not_at_all', 'Not important at all'),
        ],
        label="Q4. How important was the previous round's median in your decision-making?",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_use_prior_medians = models.StringField(
        choices=[
            ('yes', 'Yes'),
            ('sometimes', 'Sometimes'),
            ('no', 'No'),
        ],
        label="Q5. Did you use the medians from the previous two or more rounds to help make your decisions?",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_prior_medians_importance = models.StringField(
        choices=[
            ('very', 'Very important'),
            ('somewhat', 'Somewhat important'),
            ('not_much', 'Not very important'),
            ('not_at_all', 'Not important at all'),
        ],
        label="Q6. How important were the medians from the previous two or more rounds in your decision-making?",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_best = models.StringField(
        choices=[
            ('all_zero', 'Everyone chooses 0'),
            ('all_high', 'Everyone chooses a high value'),
            ('mixed_low_high', 'Some choose low values, some choose high values'),
            ('other', 'Others'),
        ],
        label="Q7. What do you think was the best outcome for the group in each round?",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_best_other = models.StringField(
        label="If others, please specify:",
        blank=True,
    )
    survey_gender = models.StringField(
        choices=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('nonbinary', 'Non-binary'),
            ('prefer_not', 'Prefer not to say'),
        ],
        label="Q10. Gender",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_prior_bc = models.StringField(
        choices=[
            ('yes', 'Yes'),
            ('no', 'No'),
            ('unsure', 'Unsure'),
        ],
        label="Q8. Have you participated in a Beauty Contest experiment before?",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_game_theory = models.StringField(
        choices=[
            ('formal', 'Formal course'),
            ('self_study', 'Self-study'),
            ('no', 'No'),
        ],
        label="Q9. Have you studied game theory or experimental economics?",
        widget=widgets.RadioSelect,
        blank=True,
    )
    survey_age = models.StringField(
        choices=[(str(a), str(a)) for a in range(17, 30)] + [('30+', '30 or above')],
        label="Q11. Age",
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

class Welcome(Page):
    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number == 1
            and player.session.config.get('show_welcome', False)
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            n=player.session.num_participants,
            num_rounds=session_num_rounds(player),
        )


class Consent(Page):
    form_model = 'player'
    form_fields = ['consent_given']

    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number == 1
            and player.session.config.get('show_consent', True)
        )

    @staticmethod
    def error_message(player: Player, values):
        if not values.get('consent_given'):
            return "You must check the box to consent to participate."


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
            other_players=player.session.num_participants - 1,
            num_rounds=session_num_rounds(player),
            point_value=player.session.config.get('real_world_currency_per_point', 1),
        )


class Quiz(Page):
    form_model = 'player'
    form_fields = [
        'quiz_match_median',
        'quiz_equal_earnings',
        'quiz_below_earnings',
        'quiz_fixed_penalty',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def error_message(player: Player, values):
        correct = dict(
            quiz_match_median='no_penalty',
            quiz_equal_earnings='no_penalty_formula',
            quiz_below_earnings='penalty_formula',
            quiz_fixed_penalty='fixed',
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


class Belief(Page):
    form_model = 'player'
    form_fields = ['belief_median']

    @staticmethod
    def is_displayed(player: Player):
        return (
            player.round_number <= session_num_rounds(player)
            and player.session.config.get('elicit_belief', False)
        )

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            round_number=player.round_number,
            num_rounds=session_num_rounds(player),
        )


class Choice(Page):
    form_model = 'player'
    form_fields = ['x_choice']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= session_num_rounds(player)

    @staticmethod
    def error_message(player: Player, values):
        if values.get('x_choice') is None:
            return "Please choose a number and confirm your submission."

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            L=player.session.config.get('penalty', PENALTY_LOW),
            E=C.ENDOWMENT,
            K=C.K,
            round_number=player.round_number,
            num_rounds=session_num_rounds(player),
        )


class WaitForGroup(WaitPage):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= session_num_rounds(player)

    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number <= session_num_rounds(player)

    @staticmethod
    def vars_for_template(player: Player):
        median = player.group.median_x
        num_rounds = session_num_rounds(player)
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
            num_rounds=num_rounds,
            is_last_round=player.round_number == num_rounds,
        )


class Survey(Page):
    form_model = 'player'
    form_fields = [
        'survey_risk',
        'survey_strategy',
        'survey_use_median',
        'survey_median_importance',
        'survey_use_prior_medians',
        'survey_prior_medians_importance',
        'survey_best',
        'survey_best_other',
        'survey_prior_bc',
        'survey_game_theory',
        'survey_gender',
        'survey_age',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == session_num_rounds(player)


class Payment(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == session_num_rounds(player)

    @staticmethod
    def vars_for_template(player: Player):
        paid_round = player.participant.paid_round
        paid_player = player.in_round(paid_round)
        paid_amount = paid_player.round_payoff
        player.payoff = paid_amount
        fee = player.session.config.get('participation_fee', 0)
        point_value = player.session.config.get('real_world_currency_per_point', 1)
        bonus = paid_amount * point_value
        return dict(
            paid_round=paid_round,
            paid_amount=round(paid_amount, 2),
            point_value=point_value,
            bonus=round(bonus, 2),
            participation_fee=fee,
            total=round(bonus + fee, 2),
        )


page_sequence = [
    Welcome,
    Consent,
    Instructions,
    Quiz,
    Belief,
    Choice,
    WaitForGroup,
    Results,
    Survey,
    Payment,
]
