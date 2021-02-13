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
        month = input('\nWould you like to see data for a specific month? Choose from January to June\n').lower()
        while True:
            if month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                month = input('Incorrect entry.\n Please choose out of the first six months\n').lower()
            else:
                break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Would you like to see data for all days of the week? Yes or No\n').lower()
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
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    # Values for new rows
    months = []
    days_of_week = []
    hours = []
    start_times = df['Start Time'].tolist()
    for start_time in start_times:
        t = parser.parse(start_time)
        months.append(t.month)
        hours.append(t.hour)
        days_of_week.append(t.weekday())

    # Input month column
    df['month'] = months

    # Input days column
    df['day_of_week'] = days_of_week

    # Input hour column
    df['hour'] = hours

    if month != 'all':
        is_same_month = df['month'] == MONTH_DATA[month]
        df = df.loc[is_same_month]

    if day != 'all':
        is_same_day = df['day_of_week'] == DAY_DATA[day]
        df = df.loc[is_same_day]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month', common_month)

    # TO DO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print('The most common day is', common_day)

    # TO DO: display the most common start hour
    start_hour = df['hour'].mode()[0]
    print('The most common start hour', start_hour)

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('Commonly used start station:', common_start_station)

    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('Commonly used end station:', common_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    combination_trip = df['Start Station'] + df['End Station']
    print('Most common trip is', combination_trip.mode()[0])


    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total travel time:', df['Trip Duration'].sum())

    # TO DO: display mean travel time
    print('Mean travel time:', df['Trip Duration'].mean())

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].count()
    print('Counts of user types:', user_types)

    # TO DO: Display counts of gender

    if 'Gender' in df:
        gender_counts = df['Gender'].value_counts()
        print('Counts of gender:', gender_counts)
    else:
        print('Unknown gender\n')

        # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest = df['Birth Year'].min()
        print('Earliest year of birth:\n', earliest)
        most_recent = df['Birth Year'].max()
        print('Most recent year of birth:\n', most_recent)
        common_year = df['Birth Year'].mode()[0]
        print('Common year of birth:\n', common_year)
    else:
        print('Unknown birth\n')

    print('\nThis took %s seconds.' % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Displays raw data until user states no """
    i = 0
    raw = input('Want to see the first 5 lines of raw data?\n').lower() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns', 300)

    while True:
        if raw == 'no':
            break
        print(df[i:i+5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
        raw = input('Want to see the last 5 rows of raw data?\n').lower() # TO DO: convert the user input to lower case using lower() function
        i += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == '__main__':
    main()
