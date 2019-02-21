import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }
valid_time_filters = ['none', 'day', 'month', 'both']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']
cities = ['Chicago', 'New York', 'Washington', 'All']

def prompt_for_raw_data(city):
    while True:
        response = input('Would you like to see the first 5 rows of raw data (Y/N)?\n').title()
        if response != 'Y' and response != 'N':
            print("Oops! {} is not a valid answer. Please type 'Y' or 'N'.\n".format(response))
        else:
            break
            
    if response == 'Y':
        file = open(CITY_DATA[city])
        for i in range(0, 5):
            print(file.readline())

        while True:
            response = input('Would you like to see 5 more rows of raw data (Y/N)?\n').title()
            if response != 'Y' and response != 'N':
                print("Oops! {} is not a valid answer. Please type 'Y' or 'N'.\n".format(response))
            if response == 'Y':
                for i in range(0, 5):
                    print(file.readline())
            else:
                file.close()
                break
                        

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user inxput for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, New York, or Washington?\n').title()
        if city in cities:
            prompt_for_raw_data(city)
            break
        else:
            print("Oops! {} is not a valid answer. Please type Chicago, New York, or Washington.\n".format(city))

    # We want to avoid an UnboundLocalError so we assign 'month' and 'day' an empty value
    # in case we're not filtering by either or both.
    month = ""
    day = ""
    while True:
        response = input('Would you like to filter the data by month, day, both, or not at all (type "none" for not at all)?\n')
        if response in valid_time_filters:
            if response == 'none':
                break
            
            if response == 'month' or response == 'both':
                # TO DO: get user input for month (all, january, february, ... , june)
                while True:
                    month = input('Which month? January, February, March, April, May, June, or All? Please type out the full month name.\n').title()
                    if month in months:
                        break
                    else:
                        print("Oops! {} is not a valid answer. Please type out the month name.\n".format(month))
            if response == 'day' or response == 'both':
                # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
                while True:
                    day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or All?\n').title()
                    if day in days:
                        break
                    else:
                        print("Oops! {} is not a valid answer. Please type out the wanted day of the week.\n".format(day))
            break
        else:
            print("Oops! {} is not a valid answer. Please type 'day', 'month', 'both' or 'none'.\n".format(response))

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
    
 # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month and month != 'All':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day and day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('\nMost common month:', months[popular_month - 1])

    # TO DO: display the most common day of week
    popular_day_of_week = df['day_of_week'].mode()[0]
    print('\nMost common day of week:', popular_day_of_week)

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('\nMost common start hour (0:00-23:00): {}:00'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('\nMost commonnly used start station:', popular_start_station)

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('\nMost commonnly used end station:', popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip
    df['start_end_station_combination'] = df['Start Station'] + ' and ' + df['End Station']
    popular_station_combination = df['start_end_station_combination'].mode()[0]
    print('\nMost frequent combination of start station and end station trip:', popular_station_combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal travel time: ', total_travel_time)

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nMean travel time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types_counts = df['User Type'].value_counts()
    print('\nCounts of user types: \n{}'.format(user_types_counts))

    # TO DO: Display counts of gender
    if 'Gender' in df: 
        gender_counts = df['Gender'].value_counts()
        print('\nCounts of gender: \n{}'.format(gender_counts))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df: 
        earliest_birth_year = df['Birth Year'].min()
        print('\nEarliest year of birth: ', earliest_birth_year)
   
        recent_birth_year = df['Birth Year'].max()
        print('\nMost recent year of birth: ', recent_birth_year)

        popular_birth_year = df['Birth Year'].mode()[0]
        print('\nMost common year of birth: ', popular_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
