"""This programm creates the histogram from Closure_record.xlsx"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Read Stations_data.xlsx drop fist column and first row


# Plot histogram for all station times
def histogram_task2():
    labels = []
    stn_data = []

    # getting data from Excel file
    histogram_df = pd.read_excel('Closure_record.xlsx')
    histogram_df = histogram_df.drop(columns=histogram_df.columns[-1:-1])

    # running loop to get data
    for data in range(0, len(histogram_df)):
        line = histogram_df.loc[data, 'Lines']
        station_a = histogram_df.loc[data, 'Station A']
        station_b = histogram_df.loc[data, 'Station B']
        a = station_a, station_b
        stn_data.append([line, a])

    for i in range(len(stn_data)):
        labels.append(stn_data[i])

    time_before = histogram_df['Time_before']
    time_after = histogram_df['Time_after']

    x = np.arange(len(labels))  # the label locations
    width = 0.40  # the width of the bars
    plt.rcParams['font.size'] = 6

    # creating plot
    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width / 2, time_before, width, label='Before')
    rects2 = ax.bar(x + width / 2, time_after, width, label='After')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    # display the data
    ax.set_ylabel('Time(m)')
    ax.set_title("Journey Time between immediate neighbour station per line before and after closing stations. ")
    ax.set_xticks(x, labels, rotation=30, ha='right')
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    fig.tight_layout()
    plt.show()


histogram_task2()

"""Reference:: Metapolib :: https://matplotlib.org/stable/gallery/index.html"""
