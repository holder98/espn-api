# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 23:42:10 2022

@author: gjh56
"""

from espn_api.baseball import League

import daily_checks 
from Gmail_Email import gmail_email
from datetime import date, timedelta

            

league = League(league_id=44195, year=2022, swid='6F2708E3-72BB-4FD7-BE07-D5AC1D8846D8', espn_s2='AECaeSP0dKyhunWGtQDcFc2b4l0q0%2FX17da2nCwmxWC06HjOdy8rwLOsYJhMrxbAvd7iuyFasC69EntcPXxLJIGZ85M1U8BxSDXx8%2Bi0q7cSffL1HH09cJ6hbnq9OpgdyClRmsTA0atFl1AuahpD0eyHTG5iPtTJEuyJ04r26eReCOakSwTEHt%2FcgdFMH9R5Bqy0WAAbWQzEKNlJ%2F3K4H%2FfpkQgmzdhREPbh6j3t4Li9gPcb7ggl9vnR6HM9XYmYJX0s6v2jzV50mx44rN44qQlO')

my_team = league.teams[8]

daily_check = True
weekly_check = False

if daily_check:
    today = date.today()
    tomorrow = today + timedelta(days=1)
    header = f"Weekly Check for {today}"
    injury_check_message = daily_checks.check_for_injuries(my_team)
    current_matchup_status, logo_images = daily_checks.get_current_matchup_info(league, my_team)
    prob_starters_today_tomorrow = daily_checks.check_probable_starters(my_team, today, tomorrow)

elif weekly_check:
    # preview message -- my record against that team
    # review message?
    first_day_of_matchup = '7/17/2022'
    last_day_of_matchup = '7/24/2022'
    header = f"Weekly Check for {first_day_of_matchup}"
    curr_matchup_period = league.currentMatchupPeriod
    prob_starters_week = daily_checks.check_probable_starters(my_team, first_day_of_matchup, last_day_of_matchup)



final_message = '''\
Injury check: {injury_check_message}
Current matchup status:  {current_matchup_status}
Probable starters in the next few days:
{prob_starters_today_tomorrow}
'''.format(injury_check_message=injury_check_message, current_matchup_status=current_matchup_status, prob_starters_today_tomorrow=prob_starters_today_tomorrow)



html_message = '''\
<!DOCTYPE html>
<html>
    <body>
        <div style="background-color:#eee;padding:10px 20px;">
            <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">{header}</h2>
        </div>
        <div style="padding:20px 0px">
            <div style="height: 500px;width:400px">
                <div style="text-align:center;">
                    <h3>Current Matchup Status</h3>
                    {current_matchup_status}
                    <h3>Injury Check</h3>
                    <p>{injury_check_message}</p>
                    <h3>Probable starters today and tomorrow</h3>
                    {prob_starters_today_tomorrow}
                </div>
            </div>
        </div>
    </body>
</html>
'''.format(header=header, team_logo=logo_images[0], opp_logo=logo_images[1], injury_check_message=injury_check_message, current_matchup_status=current_matchup_status, prob_starters_today_tomorrow=prob_starters_today_tomorrow)

# <img src="https://media.istockphoto.com/vectors/baseball-player-in-flat-design-isolated-on-white-background-vector-id1040284348?k=20&m=1040284348&s=612x612&w=0&h=gtYi02-HaspjWJGfkc2GOC_-CkWms0owQwgPmxeO1vo=" style="height: 25px; width: 25px;">
# <img src="https://hdclipartall.com/images/ambulance-clipart-ambulance-car-clipart-ambulance-clipart-emt-clipart-cartoon-vector-silhouette-340.jpg" style="height: 25px;">
                    # <table>
                    #     <tr>
                    #     <td>
                    #         <img style="width:100px;" src="{team_logo}">
                    #     </td>
                    #     <td>
                    #         <img style="width:100px;" src="{opp_logo}">
                    #     </td>
                    #     </tr>
                    # </table>           

receiving_email = ['holdergabe@comcast.net']
subject = 'Daily Fantasy Baseball Check'

#gmail_email(receiving_email, subject, final_message)
print(final_message)