from utils import get_SPs, get_prob_pitchers_for_timeframe, add_in_opp_team_context
from datetime import timedelta
from prettytable import PrettyTable

def check_for_injuries(team):

    max_IL_slots = 4

    curr_injured = 0

    curr_injured_on_IL = 0

    curr_injured_not_IL = 0

    curr_not_injured_on_IL = 0

    for player in team.roster:

        if player.injured:
            curr_injured += 1
            if player.lineupSlot == 'IL':
                curr_injured_on_IL += 1
            else:
                curr_injured_not_IL += 1
        else:
            if player.lineupSlot == 'IL':
                curr_not_injured_on_IL += 1
    
    if curr_injured_not_IL > 0: # if there are any IL-eligible players not on the IL
        if curr_injured_on_IL == max_IL_slots: # if already at max IL spots
            # nothing to do since the IL is full
            message = 'There are injured players on the bench, but no more IL spots to use. There are {curr_injured_not_IL} injured players on bench.'
            pass
        elif curr_not_injured_on_IL > 0 and curr_not_injured_on_IL == curr_injured_not_IL: # if there are IL slots being used up by non-injured players, swap them
            message = 'Swap {curr_not_injured_on_IL} injured player(s) on bench for non-injured player(s) on IL'
        elif curr_not_injured_on_IL > 0 and curr_not_injured_on_IL > curr_injured_not_IL:
            num_to_drop = curr_not_injured_on_IL-curr_injured_not_IL
            message = 'Swap {curr_injured_not_IL} injured player(s) on bench for non-injured player(s) on IL. Drop {num_to_drop} player(s) to activate {num_to_drop} player(s)'

        elif curr_not_injured_on_IL > 0 and curr_not_injured_on_IL < curr_injured_not_IL:
            net_add_to_IL = curr_injured_not_IL - curr_not_injured_on_IL
            if curr_injured_on_IL + net_add_to_IL > max_IL_slots:
                actual_add_to_IL = max_IL_slots - curr_injured_on_IL
                message = 'Swap {curr_injured_not_IL} injured player(s) on bench for non-injured player(s) on IL. Add {actual_add_to_IL} player(s) after IL\'ing {actual_add_to_IL} player(s)'
            else:
                message = 'Swap {curr_injured_not_IL} injured player(s) on bench for non-injured player(s) on IL. Add {net_add_to_IL} player(s) after IL\'ing {net_add_to_IL} player(s)'

        else:
            message = 'Unhandled situation'
    elif curr_not_injured_on_IL > 0:
        message = 'Activate {curr_not_injured_on_IL} player(s)'
    else:
        message = 'No necessary IL actions'
    

    return message


def get_current_matchup_info(league, team):
    curr_matchup_num = league.currentMatchupPeriod
    curr_matchup = team.schedule[curr_matchup_num-1]
    if curr_matchup.away_team.team_name == team.team_name:
        team_pts = curr_matchup.away_final_score
        opp_pts = curr_matchup.home_final_score
        opp_name = curr_matchup.home_team.team_name
        team_image = curr_matchup.away_team.logo_url
        opp_image = curr_matchup.home_team.logo_url
    else:
        team_pts = curr_matchup.home_final_score
        opp_pts = curr_matchup.away_final_score
        opp_name = curr_matchup.away_team.team_name
        team_image = curr_matchup.home_team.logo_url
        opp_image = curr_matchup.away_team.logo_url
    if team_pts > opp_pts:
        score_message = f"<p>You are currently beating {opp_name}, {team_pts} to {opp_pts}</p>"
    elif team_pts < opp_pts:
        score_message = f"<p>You are currently losing to {opp_name}, {team_pts} to {opp_pts}</p>"
    else:
        score_message = f"<p>You are currently tied with {opp_name}, {team_pts} to {opp_pts}</p>"

    if team_pts > 0: # if not the first day
        all_pts = []
        teams = []
        for loop_team in league.teams:
            if loop_team.team_name not in teams:
                curr_matchup = loop_team.schedule[curr_matchup_num-1]
                all_pts.append(curr_matchup.away_final_score)
                all_pts.append(curr_matchup.home_final_score)
                teams.append(curr_matchup.away_team.team_name)
                teams.append(curr_matchup.home_team.team_name)
        average_pts = sum(all_pts) / len(teams)
        sorted_least_to_most = [x for _, x in sorted(zip(all_pts, teams))]

        map_numbers = {
            1: '1st',
            2: '2nd',
            3: '3rd',
            4: '4th',
            5: '5th',
            6: '6th',
            7: '7th',
            8: '8th',
            9: '9th',
            10: '10th'
        }

        team_place = 10 - sorted_least_to_most.index(team.team_name)
        opp_place = 10 - sorted_least_to_most.index(opp_name)
        team_place_super = map_numbers[team_place]
        opp_place_super = map_numbers[opp_place]

        relative_pts_message = f'''\
            <p>You and your opponent have scored the {team_place_super} and {opp_place_super} most points this week, respectively.</p>
            <p>The average points so far this week is {average_pts}.</p>
            '''
    else:
        relative_pts_message = "<p>Good luck this week</p>"
    
    #TODO get all-time (and current-year) record against opponent

    return score_message + relative_pts_message, [team_image, opp_image]


def check_probable_starters(team, d1, d2):
    # check for probable starters between d1 and d2

    pitchers = get_SPs(team)


    prob_starters = get_prob_pitchers_for_timeframe(pitchers, d1.strftime("%m/%d/%Y"), d2.strftime("%m/%d/%Y"))


    # TODO: decide what these dates should be. How far back? Properly format
    context_start = d1 - timedelta(days=30)
    context_end = d1 - timedelta(days=1)
    prob_starters = add_in_opp_team_context(prob_starters, context_start.strftime("%m/%d/%Y"), context_end.strftime("%m/%d/%Y"))

    t = PrettyTable(['Date', 'Pitcher', 'Opp Team', 'Opp Avg. RS', 'Venue', 'Opp Pitcher'])

    for pitcher in prob_starters:
        for i in range(len(prob_starters[pitcher])):
            t.add_row([prob_starters[pitcher][i]['Date'], pitcher, prob_starters[pitcher][i]['Opp team'], prob_starters[pitcher][i]['Opp team avg runs'], prob_starters[pitcher][i]['Venue name'], prob_starters[pitcher][i]['Opp pitcher']])

    table_html = '''\
    <table>
    <tr>
        <th>Date</th>
        <th>Pitcher</th>
        <th>Opp Team</th>
        <th>Opp Avg. RS</th>
        <th>Venue</th>
        <th>Opp Pitcher</th>
    </tr>
    '''

    for pitcher in prob_starters:
        for i in range(len(prob_starters[pitcher])):
            new_row = '''\
            <tr>
                <td>{date}</td>
                <td>{pitcher}</td>
                <td>{opp_team}</td>
                <td>{opp_runs}</td>
                <td>{venue}</td>
                <td>{opp_pitcher}</td>
            </tr>
                '''.format(date=prob_starters[pitcher][i]['Date'], pitcher=pitcher, opp_team=prob_starters[pitcher][i]['Opp team'], 
                opp_runs=prob_starters[pitcher][i]['Opp team avg runs'], venue=prob_starters[pitcher][i]['Venue name'], 
                opp_pitcher=prob_starters[pitcher][i]['Opp pitcher'])
            table_html = table_html + new_row
    table_html = table_html + '''
    </table>
    '''
    
    #message_array = [f"{pitcher} starts against the {prob_starters[pitcher][i]['Opp team']} (30-day RS={prob_starters[pitcher][i]['Opp team avg runs']}) and {prob_starters[pitcher][i]['Opp pitcher']} on {prob_starters[pitcher][i]['Date']}\n" for pitcher in prob_starters for i in range(len(prob_starters[pitcher]))]
    return table_html