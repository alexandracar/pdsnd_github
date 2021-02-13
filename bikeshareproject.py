import time
import pandas as pd
import numpy as np
from dateutil import parser

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_DATA = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}

DAY_DATA = {
    'monday': 0,
    'tuesday': 1,
    'wednesday': 2,
    'thursday': 3,
    'friday': 4,
    'saturday': 5,
    'sunday': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input('Choose a city: \n Chicago, New York City, or Washington\n').lower()

    while True:
        if city not in CITY_DATA:
            city = input('Incorrect city name! \n Please choose either Chicago, New York City, or Washington\n').lower()
        else:
            break

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Would you like to see data for all months? Yes or No\n').lower()
    if month == 'yes':
        month = 'all'
    else:
        month = input('\nWould you like to see data for a certain month? Choose from January to June\n').lower()
        while True:
            if month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                month = input('Incorrect entry.\n Please choose out of the first six months\n').lower()
            else:
                break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Would you like to see data for each weekday? Yes or No\n').lower()
    # Use all for all data for each weekday
    if day == 'yes':
        day = 'all'
    else:
        day= input('\nPlease enter Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday\n').lower()
        while True:
            if day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                day = input('Incorrect entry. \nPlease choose a correct weekday\n').lower()
            else:
                break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        dataframe - Pandas DataFrame containing city data filtered by month and day
    """
    dataframe = pd.read_csv(CITY_DATA[city])

    # Values for new rows
    months = []
    days_of_week = []
    hours = []
    start_times = dataframe['Start Time'].tolist()
    for start_time in start_times:
        time_parsed = parser.parse(start_time)
        months.append(time_parsed.month)
        hours.append(time_parsed.hour)
        days_of_week.append(time_parsed.weekday())

    # Input month column
    dataframe['month'] = months

    # Input days column
    dataframe['day_of_week'] = days_of_week

    # Input hour column
    dataframe['hour'] = hours

    if month != 'all':
        is_same_month = dataframe['month'] == MONTH_DATA[month]
        dataframe = dataframe.loc[is_same_month]

    if day != 'all':
        is_same_day = dataframe['day_of_week'] == DAY_DATA[day]
        dataframe = dataframe.loc[is_same_day]


    return dataframe


def time_stats(dataframe):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = dataframe['month'].mode()[0]
    print('The most common month', common_month)

    # TO DO: display the most common day of week
    common_day = dataframe['day_of_week'].mode()[0]
    print('The most common day is', common_day)

    # TO DO: display the most common start hour
    start_hour = dataframe['hour'].mode()[0]
    print('The most common start hour', start_hour)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(dataframe):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = dataframe['Start Station'].mode()[0]
    print('Commonly used start station:', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = dataframe['End Station'].mode()[0]
    print('Commonly used end station:', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    combination_trip = dataframe['Start Station'] + dataframe['End Station']
    print('Most common trip is', combination_trip.mode()[0])


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(dataframe):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time:', dataframe['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('Mean travel time:', dataframe['Trip Duration'].mean())

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(dataframe):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = dataframe['User Type'].count()
    print('Counts of user types:', user_types)

    # TO DO: Display counts of gender

    if 'Gender' in dataframe:
        gender_counts = dataframe['Gender'].value_counts()
        print('Counts of gender:', gender_counts)
    else:
        print('Unknown gender\n')

        # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in dataframe:
        earliest = dataframe['Birth Year'].min()
        print('Earliest year of birth:\n', earliest)
        most_recent = dataframe['Birth Year'].max()
        print('Most recent year of birth:\n', most_recent)
        common_year = dataframe['Birth Year'].mode()[0]
        print('Common year of birth:\n', common_year)
    else:
        print('Unknown birth\n')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def display_raw_data(dataframe):
    """ Displays raw data until user states no """
    i = 0
    raw = input('Want to see the first 5 lines of raw data?\n').lower() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns', 300)

    while True:
        if raw == 'no':
            break
        print(dataframe[i:i+5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
        raw = input('Want to see the last 5 rows of raw data?\n').lower() # TO DO: convert the user input to lower case using lower() function
        i += 5

def main():
    while True:
        city, month, day = get_filters()
        dataframe = load_data(city, month, day)

        time_stats(dataframe)
        station_stats(dataframe)
        trip_duration_stats(dataframe)
        user_stats(dataframe)
        display_raw_data(dataframe)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == '__main__':
    main()
