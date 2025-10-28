import time
import pandas as pd
import numpy as np

# Sources including stackoverflow, w3schools, and github were utilized in creating this project.
# Ideas from github were utilized to gain new prespectives on how to tackle the project.

## Filenames
chicago = 'chicago.csv'
new_york_city = 'new_york_city.csv'
washington = 'washington.csv'

def get_raw_city_data():
    '''Asks the user for a city, get the corresponding bikeshare data as Pandas
        dataframe, perform basic data processing, and 
        and returns the processed data and selected city name.
    Args:
        none.
    Returns:
        (obj) basic processed data
        (str) Name of the selected city.
    '''

# TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        get_city = input('\nHello! Let\'s explore some US bikeshare data!\n'
                 'Would you like to see data for Chicago, New York, or Washington?\n')
        if get_city.lower() in ('chicago', 'new york', 'washington'):
            if get_city.lower() == 'chicago':
                city_filename = chicago
            elif get_city.lower() == 'new york':
                city_filename = new_york_city
            elif get_city.lower() == 'washington':
                city_filename = washington
            break
        print('Please enter one of the three valid city names provided.')

    raw_city_data = pd.read_csv(city_filename)
    # parse datetime and column names
    raw_city_data['Start Time'] = pd.to_datetime(raw_city_data['Start Time'])
    raw_city_data['End Time'] = pd.to_datetime(raw_city_data['End Time'])
    #replace white spaces with underscores   
    raw_city_data.columns = [x.strip().replace(' ', '_') for x in raw_city_data.columns]
    city_file = get_city.lower()
    return raw_city_data, city_file

def filter_time_period(raw_city_data):
    '''Asks the user for a time period and returns the filtered data.
    Args:
        (obj) basic processed data
    Returns:
        (obj) filtered data
        (str) Name of the filter(none, name of month, or name of the weekday).
    '''

# TO DO: get user input for month (all, january, february, ... , june)

    while True: 
        time_period = input('\nWould you like to filter the data by month, day, or not at'
                        ' all? Type "none" for no time filter.\n')
        if time_period in ('month', 'day', 'none'):
            break
        print('Please enter one of the three valid inputs provided.')
    if time_period == 'month':
        month_tuple = ('january', 'february', 'march', 'april', 'may', 'june')
        while True:
            get_month = input('\nWhich month? January, February, March, April,' 
                              ' May, or June?\n')
            if get_month.lower() in month_tuple:
                month_ind = month_tuple.index(get_month.lower()) + 1
                filtered_city_data = raw_city_data[raw_city_data['Start_Time'].dt.month == month_ind]
                time_period = get_month.lower()
                break
            print('Please enter one of the valid months provided.')

# TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    elif time_period == 'day':
        list_weekdays = ('monday','tuesday','wednesday','thursday','friday','saturday','sunday')
        while True:
            get_day = int(input('\nWhich day? Please type your response as an integer.' 
                                'E.g. Monday:0, Tuesday:1...\n'))
            if get_day in np.arange(0, 6, 1, 'int'):
                filtered_city_data = raw_city_data[raw_city_data['Start_Time'].dt.dayofweek == get_day]
                time_period=list_weekdays[get_day]
                break
            print('Please enter a valid integer.')

    else:
        filtered_city_data = raw_city_data 

    return filtered_city_data, time_period

# TO DO: display the most common month

def pop_month(city_file, time_period, filtered_city_data):
    '''Finds the most popular month for start time.
    Args:
        (str) Name of the city.
        (str) Name of the filter.
        (obj) filtered data.
    Returns:
        none.
        '''

    month_tuple = ('January', 'February', 'March', 'April', 'May', 'June')
    grouped_data = filtered_city_data['Start_Time'].groupby([filtered_city_data.Start_Time.dt.month]).agg('count')

    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The most popular month for start time is {} with {} total transactions.".format(month_tuple[grouped_data.argmax() - 1], grouped_data[grouped_data.argmax()]))
    print("It's total number of transactions is {} times greater than the total transactions for the least popular month {}.".format(format(grouped_data[grouped_data.argmax()]/grouped_data[grouped_data.argmin()],'.2f'),month_tuple[grouped_data.argmin()-1]))

# TO DO: display the most common day of week

def pop_day(city_file, time_period, filtered_city_data):
    '''Finds the most popular day of week.
    Args:
        (str) Name of the city.
        (str) Name of the filter.
        (obj) filtered data.
    Returns:
        none.
    '''
    list_weekdays = ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')

    temp1 = filtered_city_data.loc[:,['Start_Time','End_Time']]
    temp1['weekday'] = temp1['Start_Time'].dt.dayofweek
    temp2 = temp1.groupby(['weekday']).size().reset_index(name='counts')
    final_pop_day = temp2.loc[temp2['counts'].idxmax()]
    first_pop_day = temp2.loc[temp2['counts'].idxmin()]
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The most popular day of the week is {} with total transactions of {}.".format(list_weekdays[final_pop_day['weekday']], final_pop_day['counts']))
    print("{} has {} times more transaction than {} which is the least popular day.".format(list_weekdays[final_pop_day['weekday']], format(final_pop_day['counts']/first_pop_day['counts'],'.2f'), list_weekdays[first_pop_day['weekday']]))

# TO DO: display the most common start hour

def pop_hour(city_file, time_period, filtered_city_data):
    '''Finds the most popular hour of day.
    Args:
        (str) Name of the city.
        (str) Name of the filter.
        (obj) filtered data.
    Returns:
        none.
    '''
    grouped_data = filtered_city_data['Start_Time'].groupby([filtered_city_data.Start_Time.dt.hour]).agg('count')
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The most popular hour of the day for start time is {}:00 with {} total transactions.".format(grouped_data.argmax(), grouped_data[grouped_data.argmax()]))
    print("It's total transactions are {} times greater than the total transactions of {}:00 which is the least popular hour.".format(format(grouped_data[grouped_data.argmax()]/grouped_data[grouped_data.argmin()],'.2f'),grouped_data.argmin()))

# TO DO: display total travel time
# TO DO: display mean travel time

def trip_duration(city_file, time_period, filtered_city_data):
    '''Finds the total trip duration and average trip duration.
    Args:
        (str) Name of the city.
        (str) Name of the filter.
        (obj) filtered data.
    Returns:
        none.
    '''
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The total trip duration and average trip duration are {} seconds and {} seconds".format(format(filtered_city_data['Trip_Duration'].max(),'.2f'), format(filtered_city_data['Trip_Duration'].mean(),'.2f')))

# TO DO: display most commonly used start station
# TO DO: display most commonly used end station

def pop_stations(city_file, time_period, filtered_city_data):
    '''Finds the most popular used start station and most popular used end station.
    Args:
        (str) Name of the city.
        (str) Name of the filter.
        (obj) filtered data.
    Returns:
        none.
    '''
    group_pop_start = filtered_city_data.groupby(['Start_Station']).size().reset_index(name = 'counts')
    pop_start_station=group_pop_start.loc[group_pop_start['counts'].idxmax()]
    first_pop_start=group_pop_start.loc[group_pop_start['counts'].idxmin()]
    group_pop_end = filtered_city_data.groupby(['End_Station']).size().reset_index(name = 'counts')
    pop_end_station=group_pop_end.loc[group_pop_end['counts'].idxmax()]
    first_pop_end=group_pop_end.loc[group_pop_end['counts'].idxmin()]
    
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The most popular start station is '{}' with {} total transactions.".format(pop_start_station['Start_Station'], pop_start_station['counts']))
    print("'{}' has {} times more transactions than the '{}' which is least popular start station.".format(pop_start_station['Start_Station'], format(pop_start_station['counts']/first_pop_start['counts'],'.2f'), first_pop_start['Start_Station']))
    print("The most popular end station is '{}' with {} total transactions.".format(pop_end_station['End_Station'], pop_end_station['counts']))
    print("'{}' has {} times more transactions than the '{}' which is least popular end station.".format(pop_end_station['End_Station'], format(pop_end_station['counts']/first_pop_end['counts'],'.2f'), first_pop_end['End_Station']))


# TO DO: display most frequent combination of start station and end station trip

def pop_trip(city_file, time_period, filtered_city_data):
    '''Finds the most popular trip.
    Args:
        (str) Name of the city.
        (str) Name of the filter.
        (obj) filtered data.
    Returns:
        none.
    '''
    group_pop_trip = filtered_city_data.groupby(['Start_Station', 'End_Station']).size().reset_index(name = 'counts')
    re_pop_trip = group_pop_trip.loc[group_pop_trip['counts'].idxmax()]
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The most popular trip starts from station '{}' and ends at '{}' with {} total transactions.".format(re_pop_trip['Start_Station'], re_pop_trip['End_Station'], re_pop_trip['counts']))

# TO DO: Display counts of user types

def users(city_file, time_period, filtered_city_data):
    '''Finds the counts of each user type.
    Args:
        (str) Name of the city.
        (str) Name of the filter.
        (obj) filtered data.
    Returns:
        none.
    '''
    group_user = filtered_city_data.groupby(['User_Type']).size().reset_index(name = 'counts')
    print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
    print("The total counts of each user type are:")
    print(group_user)


def gender(city_file, time_period, filtered_city_data):
    '''Finds the counts of gender.
    Args:
        (str) Name of the city.
        (str) Name of the filter.
        (obj) filtered data.
    Returns:
        none.
    '''
    if city_file.lower() == 'washington':
        print('Sorry, Data related to gender is not present for Washingtion.')
    else:
        group_gender = filtered_city_data.groupby(['Gender']).size().reset_index(name = 'counts')
        print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
        print("The total counts of each gender type are as follows:")
        print(group_gender)

# TO DO: Display earliest, most recent, and most common year of birth

def birth_years(city_file, time_period, filtered_city_data):
    '''Finds the earliest (i.e. oldest user), most recent (i.e. 
       youngest user), and most popular birth years.
    Args:
        (str) Name of the city.
        (str) Name of the filter.
        (obj) filtered data.
    Returns:
        none.
    '''
    if city_file.lower() == 'washington':
        print('Sorry, Data related to birth year is not present for Washingtion.')
    else:
        group_birth_year = filtered_city_data.groupby(['Birth_Year']).size().reset_index(name = 'counts')
        print('STATISTICS FOR "{}" CITY AND "{}" FILTER'.format(city_file.upper(),time_period.upper()))
        print("The the earliest (i.e. oldest user) and the most recent (i.e. youngest user) birth years are {} and {}.".format(int(group_birth_year['Birth_Year'].min()), int(group_birth_year['Birth_Year'].max())))
        print("The most popular birth year is {} with total {} counts.".format(int(group_birth_year.loc[group_birth_year['counts'].idxmax()]['Birth_Year']),int(group_birth_year.loc[group_birth_year['counts'].idxmax()]['counts'])))

def display_data(city_file,time_period, filtered_city_data):
    '''Displays five lines of data if the user specifies that they would like to.
    After displaying five lines, ask the user if they would like to see five more,
    continuing asking until they say stop.
    Args:
        (str) Name of the city.
        (str) Name of the filter.
        (obj) filtered data.
    Returns:
        none.
    '''

    count = 0;
    while True:
        display = input('\nWould you like to view individual trip data?' 
                        ' Type \'yes\' or \'no\'.\n')
        if display.lower() in ('yes', 'no'):
            if display.lower() == 'yes':
                print("This individual trip data is filtered by '{}' and belongs to {} city.".format(time_period, city_file))
                print(filtered_city_data[count:count + 5])
                count += 5
            else:
                print('Display of data ends')
                break
        print('Please enter one of the valid options provided.')

def statistics():
    '''Calculates and prints out the descriptive statistics about a city and time period
    specified by the user via raw input.
    Args:
        none.
    Returns:
        none.
    '''
    # Filter by city 
    raw_data, city_name = get_raw_city_data()

    # Filter by time period
    filtered_data, filter_system = filter_time_period(raw_data)

    # Most popular month
    if filter_system == 'none':
        start_time = time.time()

        pop_month(city_name, filter_system, filtered_data)
        print("That took %s seconds.\n" % (time.time() - start_time))

    # Most popular day
    month_tuple = ('january', 'february', 'march', 'april', 'may', 'june')
    if filter_system == 'none' or filter_system in month_tuple:
        start_time = time.time()

        pop_day(city_name, filter_system, filtered_data)
        print("That took %s seconds.\n" % (time.time() - start_time))

    start_time = time.time()

    # Most popular hour
    pop_hour(city_name, filter_system, filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    start_time = time.time()

    # Total and average trip duration
    trip_duration(city_name, filter_system, filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    start_time = time.time()

    # Most popular start and end stations
    pop_stations(city_name, filter_system, filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    start_time = time.time()

    # Most popular trip
    pop_trip(city_name,filter_system,filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    start_time = time.time()

    # Counts of each user type
    users(city_name,filter_system,filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    start_time = time.time()

    # Counts of gender
    gender(city_name,filter_system,filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))
    start_time = time.time()

    # Oldest and younges users and most popular birth years
    birth_years(city_name,filter_system,filtered_data)
    print("That took %s seconds.\n" % (time.time() - start_time))

    # Display five lines of data at a time if user specifies that they would like to
    display_data(city_name,filter_system,filtered_data)
    
    # Restart?
    while True:
        restart = input('\nWould you like to restart? Type \'yes\' or \'no\'.\n')
        if restart.lower() in ('yes', 'no'):
            if restart.lower() == 'yes':
                statistics()
            else:
                print('Thank you for using this application.')
            break
        print('Enter one of the valid options provided.')


if __name__ == "__main__":
	statistics()