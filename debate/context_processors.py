from debate.models import Tournament, Round
from debate.models import Config

def debate_context(request):

    if hasattr(request, 'tournament'):
        d = {
            'tournament'              : request.tournament,
            'current_round'           : request.tournament.current_round,
            'show_emoji'              : request.tournament.config.get('show_emoji'),
            'show_institutions'       : request.tournament.config.get('show_institutions'),
            'public_team_standings'   : request.tournament.config.get('public_team_standings') \
                                           and request.tournament.current_round.prev is not None,
            'public_breaking_teams'   : request.tournament.config.get('public_breaking_teams'),
            'public_breaking_adjs'    : request.tournament.config.get('public_breaking_adjs'),
            'esl_break'               : request.tournament.config.get('esl_break_size') > 0,
            'public_participants'     : request.tournament.config.get('public_participants'),
            'public_side_allocations' : request.tournament.config.get('public_side_allocations') \
                                            and request.tournament.config.get('draw_side_allocations') == "preallocated",
            'public_draw'             : request.tournament.config.get('public_draw'),
            'public_motions'          : request.tournament.config.get('public_motions'),
            'public_results'          : request.tournament.config.get('public_results'),
            'public_ballots'          : request.tournament.config.get('public_ballots'),
            'public_feedback'         : request.tournament.config.get('public_feedback'),
            'feedback_progress'       : request.tournament.config.get('feedback_progress'),
            'tab_released'            : request.tournament.config.get('tab_released'),
            'motion_tab_released'     : request.tournament.config.get('motion_tab_released'),
            'side_allocations_enabled': request.tournament.config.get('draw_side_allocations') == "preallocated",
        }
        if hasattr(request, 'round'):
            d['round'] = request.round
        return d
    return {}

