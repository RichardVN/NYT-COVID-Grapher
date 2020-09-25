""" Helper functions to simplify NY_Times_Covid_Data.py

- Retrieve COVID data from New York Times API
- Populate data and create PyGal histograms
- cleanup of .svg graph files

"""

from contextlib import closing

import csv
import os
import pygal
import requests

from graph_settings import GraphSettings
from text_menu import num_menu


def get_NYT_COVID_data(location_type, state=None):
    """

    :param location_type: 'county' or 'state', determines URL for API call
    :type location_type: str
    :param state: state to retrieve county data from
    :type state: str or None
    :return: list of dictionaries. Each dict has COVID info of a single county/state
    :rtype: list[dict]
    """
    if location_type == 'state':
        url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv'
    elif location_type == 'county':
        url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'
    else:
        print('no NYT API for this location type')
    # store response of API call
    response = requests.get(url)
    if response.status_code != 200:
        print('Failed to retrieve data:', response.status_code)
        return None
    else:
        with closing(requests.get(url, stream=True)) as r:
            f = (line.decode('utf-8') for line in r.iter_lines())
            reader = csv.reader(f, delimiter=',', quotechar='"')  # csv row iterator
            # header columns
            header_row = next(reader)
            location_type = header_row[1]
            state_column = header_row.index('state')

            # list of state data, dictionary for each state/county
            locations_data = []

            for row in reader:
                if state:
                    if state.lower() != row[state_column].lower():
                        continue
                # convert numbers into ints if possible
                for idx, value in enumerate(row):
                    try:
                        row[idx] = int(value)
                    except ValueError:
                        if 'death' in header_row[idx] or 'case' in header_row[idx]:
                            row[idx] = 0
                        # other columns such as dates remain as strings
                        pass
                # dictionary of COVID data for state / county
                location_dictionary = dict(zip(header_row, row))
                # calculate death rate
                location_dictionary['death_rates'] = (location_dictionary['deaths'] / location_dictionary['cases']) * 100
                # list of data for all states OR all counties in a state
                locations_data.append(location_dictionary)

        if locations_data:
            if state:
                print(f"\tSuccessful retrieval of COVID-19 data by {location_type} in {state.title()}")
            else:
                print(f"\tSuccessful retrieval of COVID-19 data by {location_type}")
            return locations_data
        else:
            print('Error in retrieving data')
            return None


def graphs_options_menu(locations_data, location_type, state=None):
    """ Menu to produce graph of cases, deaths, or death rate """

    if state:
        menu_title = f'COUNTY data for {state.upper()} - Select a Graph'
    else:
        menu_title = 'STATE data for all U.S. states - Select a Graph'
    graph_choice = num_menu(menu_title, ('Graph of COVID cases', 'Graph of COVID deaths', 'Graph of COVID death rates'))
    if graph_choice == 1:
        cases_dict = populate_pygal_graph_data(locations_data, location_type, 'cases')
        create_histogram(cases_dict, state)
    elif graph_choice == 2:
        # graph deaths per state
        deaths_dict = populate_pygal_graph_data(locations_data, location_type, 'deaths')
        create_histogram(deaths_dict, state)
    elif graph_choice == 3:
        death_rates_dict = populate_pygal_graph_data(locations_data, location_type, 'death_rates')
        create_histogram(death_rates_dict, state)


def sorted_locations_data(locations_data, key):
    """ Helper function to sort multiple dictionaries in order of the values of a key"""
    return sorted(locations_data, key=lambda location: location.get(key, 0), reverse=True)


def populate_pygal_graph_data(locations_data, location_type, key):
    """ Extract dictionary containing values necessary for pygal.Bar()

    :param locations_data: list of dictionaries of COVID data
    :type locations_data: list of dicts
    :param location_type: 'state' or 'county'
    :type location_type: str
    :param key: the metric to sort by, ex. 'deaths' or 'cases'
    :type key: str
    :return: dictionary of key-value pairs to create pygal histogram
    :rtype: dict
    """
    sorted_data_dicts = sorted_locations_data(locations_data, key)
    data_dict = dict()
    data_dict['x_labels'] = [d[location_type] for d in sorted_data_dicts]
    data_dict['value_name'] = key
    data_dict['value_list'] = [d[key] for d in sorted_data_dicts]
    data_dict['last_updated'] = sorted_data_dicts[1]['date']
    return data_dict


def get_state_input():

    """ Prompts user to input the name of a state and validates input

    :return: name of US state
    :rtype: str
    """
    # validate state
    states_list = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware',
                   'district of columbia', 'florida', 'georgia', 'guam', 'hawaii', 'idaho', 'illinois', 'indiana',
                   'iowa',
                   'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota',
                   'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey',
                   'new mexico',
                   'new york', 'north carolina', 'north dakota', 'northern mariana islands', 'ohio', 'oklahoma',
                   'oregon',
                   'pennsylvania', 'puerto rico', 'rhode island', 'south carolina', 'south dakota', 'tennessee',
                   'texas',
                   'utah', 'vermont', 'virgin islands', 'virginia', 'washington', 'west virginia', 'wisconsin',
                   'wyoming']
    valid_state = False
    while not valid_state:
        state = input('What state would you like to retrieve county data for?: ')
        if state.lower() in states_list:
            valid_state = True
        else:
            print('That is not a valid U.S. State. Please try again.')
    return state


def create_histogram(data_dict, state=None):
    """

    :param data_dict: dictionary containing x_labels, value_name, value_list, last_updated
    :type data_dict: dict
    :param state: U.S. state if retrieving by county
    :type state: str or None
    :return: None
    :rtype: None
    """

    # retrieve data from dict
    x_labels = data_dict['x_labels']
    value_name = data_dict['value_name']
    value_list = data_dict['value_list']
    last_updated = data_dict['last_updated']

    # shorten lists if too many locations to graph
    if len(x_labels) > 50:
        x_labels = x_labels[0:50]
        value_list = value_list[0:50]
    # graph customization
    default_settings = GraphSettings()
    config = default_settings.config
    style = default_settings.style

    # configure title of graph
    if state:
        title = f'COVID-19 {value_name} in {state.title()} Counties, New York Times ({last_updated})'
    else:
        title = f'COVID-19 {value_name} in U.S. States, New York Times ({last_updated})'
    config.title = title

    # create graph
    graph = pygal.Bar(config=config, style=style)

    # add labels and data to graph
    graph.x_labels = x_labels
    graph.add('COVID' + value_name.title(), value_list)

    # output graph to .svg file in directory
    value_name = value_name.replace(' ', '_')
    if state:
        outfname = f'NYT_COVID_{state.title()}_Counties_{value_name.title()}.svg'
    else:
        outfname = f'NYT_COVID_States_{value_name.title()}.svg'
    graph.render_to_file(outfname)

    print('\tCreated histogram:', outfname)


def svg_cleanup():
    # Store path of directory containing file
    file_directory = os.path.dirname(__file__)

    for file in os.listdir(file_directory):
        if file.endswith('.svg'):
            print('- deleting', file)
            os.unlink(file_directory + '/' + file)
