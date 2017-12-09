import matplotlib.pyplot as plt
import numpy as np
import statistics as stats
import itertools
from datetime import datetime
from datetime import timedelta

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
                if(int(i+1) % 5 == 0):
                    f.write("\n") 
    return

def get_time(time):
    time = time.split(':')
    if(len(time) < 3):
        return float(time[0])+float(time[1])/60.0
    elif(len(time) == 3):
        return float(time[0])*60.0+float(time[1])+float(time[2])/60.0

def split_dis(input):
    input = input.split(' ')
    return input[0]

def convert_distance(input_array,input_string):
    if(input_string == 'miles'):
        conversion = [round(i/1.60934,1) for i in input_array]
        return conversion
    elif(input_string == 'feet'):
        conversion = [round(i*3.28084,1) for i in input_array]
        return conversion

def plot_data(x, y, fignum, x_lab, y_lab, subfig):
    plt.figure(fignum)
    if(subfig != 0): plt.subplot(subfig)
    axes = plt.gca()
    #fitting data
    best_fit = np.polyfit(x, y, 1)
    fit = [best_fit[0]*i+best_fit[1] for i in x]
    axes.set_xlim([0.0,max(x)])
    axes.set_ylim([0.0,max(y)])
    axes.set_xlabel(x_lab)
    axes.set_ylabel(y_lab)
    plt.scatter(x, y, color='black')
    plt.plot(x, fit, color='red')
    return

def plot_hist(x, bins, fignum, x_lab, y_lab, subfig):
    plt.figure(fignum)
    if(subfig != 0): plt.subplot(subfig)
    axes = plt.gca()
    axes.set_xlabel(x_lab)
    axes.set_ylabel(y_lab)
    plt.hist(x, bins=bins)
    return

def bin_data(input_array, bins, sigma):
    start = [[] for i in range(0,len(bins))]
    time = [[] for i in range(0,len(bins))]
    distance = [[] for i in range(0,len(bins))]
    elevation = [[] for i in range(0,len(bins))]
    PRs = [[] for i in range(0,len(bins))]
    #heavy loop all other loops are just over the bins, i.e. small
    #binning data into smaller subsets 
    for i in input_array:
        for j in range(0,len(bins)-1):
            if(float(split_dis(i[2]))/1000.0 < float(bins[j+1])):
                start[j+1].append(i[0])
                time[j+1].append(get_time(i[1]))
                distance[j+1].append(float(split_dis(i[2]))/1000.0)
                elevation[j+1].append(float(split_dis(i[3])))
                PRs[j+1].append(float(split_dis(i[4])))
                break;
    #getting rid of bins with small amounts data
    start = [i for i in start if len(i) > 1]
    time = [i for i in time if len(i) > 1]
    distance = [i for i in distance if len(i) > 1]
    elevation = [i for i in elevation if len(i) > 1]
    PRs = [i for i in PRs if len(i) > 1]
    data = [start, time, distance, elevation, PRs]

    #getting averages and standard deviations for each bin
    time_stats = get_stats(time)
    elevation_stats = get_stats(elevation)

    #trimming data outside input limit
    index = trim(time, time_stats[0], time_stats[1], sigma)
    index.extend(trim(elevation, elevation_stats[0], elevation_stats[1], sigma))
    #removing duplicates from the indices
    index = get_dups(index)

    #deleting all data from the trim
    #setting a variable to keep track of how many elements in a sub list have been deleted
    #because when an item is deleted the index of other items change
    shift = 0
    for i in data:
        for j in range(0,len(index)):
            if(j != 0):
                if(index[j][0] == index[j-1][0]): shift += 1
                else: shift = 0
            del i[index[j][0]][index[j][1]-shift]
    return data

def get_stats(input_array):
    mean_array = [stats.mean(i) for i in input_array]
    dev_array = [stats.stdev(i) for i in input_array]
    return [mean_array, dev_array]

def trim(input_array, mean_array, dev_array, sigma):
    output = []
    #another heavy loop but not on all the data
    #finding data that is over a given sigma away from the mean of each bin
    for i in range(0,len(input_array)):
        for j in range(0,len(input_array[i])):
            if(input_array[i][j] > (mean_array[i]+(sigma*dev_array[i]))):
                output.append([i,j])
    return output

def get_dups(index):
    index.sort()
    index = list(i for i,_ in itertools.groupby(index))
    return index

def strip_time(date):
    date = datetime.strptime(date, "%m/%d/%y")
    return date

def date_trim(input_array, dates):
    data = []
    for i in input_array:
        if(strava_time(i[0]) >= dates[0] and strava_time(i[0]) <= dates[1]):
            data.append(i)
    if(data != []): return data
    else: return 0

def strava_time(date):
    date = datetime.strptime(date[0:10], "%Y-%m-%d")
    return date