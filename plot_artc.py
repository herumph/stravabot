import numpy as np
import matplotlib.pyplot as plt
import itertools
import functions

def main():
    #getting and cleaning data
    data = functions.get_array('data')
    data = [i.split('\t') for i in data]

    #date range if wanted
    #mm/dd/yy format
    user_in = input("Date range? ")
    if(len(user_in) > 0):
        user_in = user_in.split(' ')
        dates = [functions.strip_time(i) for i in user_in]

    #trimming data if date range if given
    if 'dates' in locals():
        data = functions.date_trim(data, dates)
        if(data == 0): 
            print("No data in that range")
            return

    #binning data
    print("Total number of runs in selection: ",len(data))
    sigma = 5.0 #sigma of data to trim
    bins = np.arange(45) #one bin for each km out to 45km
    data = functions.bin_data(data, bins, sigma)
    #splitting up data into variables and joining bins together
    start = list(itertools.chain.from_iterable(data[0]))
    time = list(itertools.chain.from_iterable(data[1]))
    distance = list(itertools.chain.from_iterable(data[2]))
    elevation = list(itertools.chain.from_iterable(data[3]))
    PRs = list(itertools.chain.from_iterable(data[4]))
    print("Number of data points being included: ",len(start))

    ##################
    #     plots      #
    ##################

    #time v distance
    functions.plot_data(time, distance, 1, "Time (minutes)", "Distance (km)", 211)
    #converting to miles
    miles = functions.convert_distance(distance,'miles')
    functions.plot_data(time, miles, 1, "Time (minutes)", "Distance (miles)", 212)

    #histogram of runs per distance
    bins = np.arange(45)
    functions.plot_hist(distance, bins, 2, "Distance (km)", "Number of runs", 211)
    bins = np.arange(28)
    functions.plot_hist(miles, bins, 2, "Distance (miles)", "Number of runs", 212)

    #distance v elevation
    #only plotting runs with >0 meters elevation
    index = [i for i in range(0,len(elevation)) if elevation[i] != 0]
    elevation1 = [elevation[i] for i in index]
    distance1 = [distance[i] for i in index]
    miles1 = [miles[i] for i in index]
    feet = functions.convert_distance(elevation1,'feet')
    functions.plot_data(distance1, elevation1, 3, "Distance (km)", "Elevation (m)", 211)
    functions.plot_data(miles1, feet, 3, "Distance (miles)", "Elevation (ft)", 212)

    #only plotting runs with >1 PR
    PR1 = [i for i in PRs if i != 0]
    bins = np.arange(25)
    functions.plot_hist(PR1, bins, 4, "PRs set in a single run", "Number of runs", 0)

    plt.show()
    return

main()