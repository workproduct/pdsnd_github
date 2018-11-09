"""
TITLE: Udacity - Explore US Bikeshare Data
DESCRIPTION: From the project brief: In this project, you will make use of Python to explore
data related to bike share systems for three major cities in the United
States—Chicago, New York City, and Washington. You will write code to import the
data and answer interesting questions about it by computing descriptive
statistics. You will also write a script that takes in raw input to create an
interactive experience in the terminal to present these statistics.
"""

import time
import datetime
import pandas as pd
import numpy as np
import calendar
from datetime import datetime, timedelta

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january',
      'february',
      'march',
      'april',
      'may',
      'june',
      'july',
      'august',
      'september',
      'october',
      'november',
      'december',
      'all']

days = ['sun',
      'mon',
      'tues',
      'wed',
      'thurs',
      'fri',
      'sat',
      'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Please choose a city to explore- \n')

    city_list=list(CITY_DATA.keys())
    print(str(city_list) + "\n")

    city = input("Enter a city name: ").lower()
    while city not in city_list:
        print("Invalid City.\n")
        city = input("Enter a city name: ").lower()
        continue
    else:
        print("\n" + city + " selected.\n")


    # get user input for month (all, january, february, ... , june)



    month = input("Enter a month, or all (ex. february): ").lower()
    while month not in months:
        print("Invalid Month.\n")
        month = input("Enter a month, or all (ex. february): ").lower()
        continue
    else:
        print("\n" + month + " selected.\n")

    # get user input for day of week (all, monday, tuesday, ... sunday)



    day = input("Enter a day of week, or all (ex. wed): ").lower()
    while day not in days:
        print("Invalid day.\n")
        day = input("Enter a day of week, or all (ex. wed): ").lower()
        continue
    else:
        print("\n" + day + " selected.\n")

    output = input('Output raw data? Enter yes or no: ')
    if output.lower() != 'yes':
        output='no'
    #for debug
    #city = "chicago"
    #month = "all"
    #day = "1"

    print('-'*40)
    return city, month, day, output


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #this is only loading 10 rows
    #df = pd.read_csv(CITY_DATA[city], nrows=10)

    df = pd.read_csv(CITY_DATA[city])
    df = df.fillna(method='bfill')

    #conver to datetime from str
    df['time'] = pd.to_datetime(df['Start Time'])

    #just month
    df['month'] = df['time'].dt.month

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    #just day
    df['day'] = df['time'].dt.day

    #find the day of the week
    df['day of week'] = df['time'].dt.dayofweek

    # filter by day of week if applicable

    if day != 'all':
        # filter by day of week to create the new dataframe
        day = day.index(day)
        df = df[df['day of week'] == day]

    #hour

    df['hour'] = df['time'].dt.hour


    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        print('\nMost Common Month for Travel\n')
        month=df['month'].mode()[0]
        print(calendar.month_name[month])
    # display the most common day of week
    if day == 'all':
        print('\nMost Common Day of Week for Travel\n')
        dow=df['day of week'].mode()[0]
        print(calendar.day_name[dow])
    # display the most common start hour
    print('\nMost Common Start Hour for Travel\n')
    hour=df['hour'].mode()[0]
    #convert to 12 hour
    h = time.strptime(str(hour), "%H")
    h12 = time.strftime( "%I %p", h )
    print(h12)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #not sure if these are right, might need to double check

    # display most commonly used start station
    mss = df['Start Station'].value_counts().idxmax()
    print('\nMost Common Start Station\n')
    print(mss)
    # display most commonly used end station
    mes = df['End Station'].value_counts().idxmax()
    print('\nMost Common End Station\n')
    print(mes)

    # display most frequent combination of start station and end station trip
    df["trip combine"] = df["Start Station"].map(str) + " to " + df["End Station"].map(str)
    mcs = df['trip combine'].value_counts().idxmax()
    print('\nMost Common Trip\n')
    print(mcs)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('\nTotal Trip Duration\n')
    TS = df['Trip Duration'].sum()
    #double check this math
    TSN= str(timedelta(seconds=float(TS)))
    print(TSN)
    # display mean travel time
    print('\nAvg Trip Duration\n')
    MS = df['Trip Duration'].mean()
    MSN= str(timedelta(seconds=float(MS)))
    print(MSN)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    ut = df['User Type'].value_counts()
    print('\nUsers by Type\n')
    print(ut)

    # Display counts of gender
    #Gender missing from washington, check if Gender exists
    if 'Gender' in df.columns:
        gt = df['Gender'].value_counts()
        print('\nUsers by Gender\n')
        print(gt)

    # Display earliest, most rece.nt, and most common year of birth
    #Birth Year missing from washington, check if Birth Year exists
    if 'Birth Year' in df.columns:
        eby = df['Birth Year'].min()
        print('\nEarliest Birth Year\n')
        print(int(eby))

        rby = df['Birth Year'].max()
        print('\nMost Recent Birth Year\n')
        print(int(rby))

        cby = df['Birth Year'].mode()
        print('\nMost Common Birth Year\n')
        print(int(cby))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def output_raw(df, output):
    #set panda print options
    pd.set_option('display.max_rows', 10)  # or 1000
    pd.set_option('display.max_columns', None)  # or 1000
    if output.lower() == 'yes':
        print(df)

def main():
    while True:
        city, month, day, output = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        output_raw(df, output)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
