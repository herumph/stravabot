from stravalib.client import Client
from config import *

def get_array(input_string):
    with open("textfiles/"+input_string+".txt","r") as f:
        input_array = f.readlines()
    input_array = [x.strip("\n") for x in input_array]
    return(input_array)

def write_out(input_string, input_array):
    if(input_string == 'done'):
        with open("textfiles/"+input_string+".txt","w") as f:
            for i in input_array:
                f.write(str(i)+"\n")
    else:
        with open("textfiles/"+input_string+".txt","a") as f:
            for i in range(0,len(input_array),1):
                f.write(str(input_array[i])+"\t") 
                if(int(i+1) % 4 == 0):
                    f.write("\n") 
    return

#connection stuff
client = Client()
authorize_url = client.authorization_url(client_id = C_ID, redirect_uri='http://localhost:8282/authorized')
access_token = client.exchange_code_for_token(client_id=C_ID, client_secret=C_SECRET, code=CODE)
client.access_token = access_token

#getting activites
activities = client.get_club_activities(club_id = CLUB, limit = 200)

#getting last updated activity
done = get_array('done')

#going through activities
data = []
for run in activities:
    #taking only runs
    if(str(run.start_date) not in done):
        if(run.type == 'Run' and run.id not in done):
            data.append(run.elapsed_time)
            data.append(run.distance)
            data.append(run.total_elevation_gain)
            data.append(run.pr_count)
            if(len(done) > 200):
                del done[-1]
            done.append(run.start_date)

#writing data
write_out('data',data)
write_out('done',done)
