from stravalib.client import Client
from config import *
import functions

#connection stuff
client = Client()
authorize_url = client.authorization_url(client_id = C_ID, redirect_uri='http://localhost:8282/authorized')
access_token = client.exchange_code_for_token(client_id=C_ID, client_secret=C_SECRET, code=CODE)
client.access_token = access_token

#getting activites
activities = client.get_club_activities(club_id = CLUB, limit = 200)

#getting activities already recorded
done = functions.get_array('done')

#going through activities
data = []
for run in activities:
    #using local activity start date as a metric since using IDs feels shady
    if(str(run.start_date) not in done):
        #taking only runs
        if(run.type == 'Run'):
            data.append(run.start_date_local)
            data.append(run.elapsed_time)
            data.append(run.distance)
            data.append(run.total_elevation_gain)
            data.append(run.pr_count)
            done.append(run.start_date)
            #keeping size of the arrays to handle small
            if(len(done) > 500):
                del done[0]

#writing data
functions.write_out('data',data)
functions.write_out('done',done)
