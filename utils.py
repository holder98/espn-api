import statsapi
import math

def get_SPs(team):
    pitchers = []
    for player in team.roster:
        if 'SP' in player.eligibleSlots:
            pitchers.append(player.name)
    return pitchers


def get_prob_pitchers_for_timeframe(pitchers, start_date,end_date): # start_date='07/01/2018',end_date='07/31/2018'
    prob_pitchers = {}
    for game in statsapi.schedule(start_date=start_date,end_date=end_date):

        if game['home_probable_pitcher'] in pitchers:
            if game['home_probable_pitcher'] not in prob_pitchers:
                prob_pitchers[game['home_probable_pitcher']] = []
            
            prob_pitchers[game['home_probable_pitcher']].append({
                'Opp team': game['away_name'],
                'Home team': game['home_name'],
                'Venue name': game['venue_name'],
                'Opp pitcher': game['away_probable_pitcher'],
                'Date': game['game_date']
            })

        if game['away_probable_pitcher'] in pitchers:
            if game['away_probable_pitcher'] not in prob_pitchers:
                prob_pitchers[game['away_probable_pitcher']] = []
            
            prob_pitchers[game['away_probable_pitcher']].append({
                'Opp team': game['home_name'],
                'Home team': game['home_name'],
                'Venue name': game['venue_name'],
                'Opp pitcher': game['home_probable_pitcher'],
                'Date': game['game_date']
            })

    return prob_pitchers


def add_in_opp_team_context(prob_starters, start_date, end_date):

    runs = {}

    for pitcher in prob_starters:
        for start in prob_starters[pitcher]:
            if start['Opp team'] not in runs:
                runs[start['Opp team']] = []
    
    for game in statsapi.schedule(start_date=start_date,end_date=end_date):
        if game['away_name'] in runs:
            runs[game['away_name']].append(int(game['away_score']))


        if game['home_name'] in runs:
            runs[game['home_name']].append(int(game['home_score']))

    for starter in prob_starters:
        for start in prob_starters[starter]:
            start['Opp team avg runs'] = round(sum(runs[start['Opp team']]) / len(runs[start['Opp team']]), 2)
    

    return prob_starters