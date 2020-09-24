""" Retrieves latest COVID-19 data from The New York Times and creates corresponding Histogram graphs.

Data courtesy of The New York Times for non-commercial use.
"""

from graph_settings import GraphSettings
from helper_functions import get_NYT_COVID_data, create_histogram

from text_menu import num_menu

us_covid_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us.csv'
us_states_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv'
us_counties_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'

states_list = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut', 'delaware',
               'district of columbia', 'florida', 'georgia', 'guam', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa',
               'kansas', 'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota',
               'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico',
               'new york', 'north carolina', 'north dakota', 'northern mariana islands', 'ohio', 'oklahoma', 'oregon',
               'pennsylvania', 'puerto rico', 'rhode island', 'south carolina', 'south dakota', 'tennessee', 'texas',
               'utah', 'vermont', 'virgin islands', 'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming']

options_menu = (
    'Create/Update COVID-19 Cases and Deaths by State',
    'Create/Update COVID-19 Cases and Deaths by County',
    'Exit Program')

while True:
    menu_choice = num_menu(options_menu)

    if menu_choice == 1:
        # retrieve data for States
        states_last_updated, states_list_by_cases, states_cases, states_list_by_deaths, states_deaths = \
            get_NYT_COVID_data(us_states_url)

        custom_settings = GraphSettings()
        # graphs cases per state
        create_histogram(
            x_labels=states_list_by_cases,
            y_label='COVID Cases',
            y_values=states_cases,
            title=f'COVID-19 Cases in U.S. States, New York Times ({states_last_updated})',
            outfname='NYT_COVID_all_states_cases.svg'
        )
        # graph deaths per state
        create_histogram(
            x_labels=states_list_by_deaths,
            y_label='COVID Deaths',
            y_values=states_deaths,
            title=f'COVID-19 Deaths in U.S. States, New York Times ({states_last_updated})',
            outfname='NYT_COVID_all_states_deaths.svg'
        )

    if menu_choice == 2:
        # retrieve data for counties
        valid_state = False
        while not valid_state:
            state = input('What state would you like to retrieve county data for?: ')
            if state.lower() in states_list:
                valid_state = True
            else:
                print('That is not a valid U.S. State. Please try again.')

        counties_last_updated, counties_list_by_cases, counties_cases, counties_list_by_deaths, counties_deaths = \
            get_NYT_COVID_data(us_counties_url, state=state)
        # graph cases per county
        create_histogram(
            x_labels=counties_list_by_cases[0:50],
            y_label='COVID Cases',
            y_values=counties_cases[0:50],
            title=f'COVID-19 Cases in {state.title()} Counties, New York Times ({counties_last_updated})',
            outfname=f'NYT_COVID_{state}_county_cases.svg'
        )
        # graph deaths per county
        create_histogram(
            x_labels=counties_list_by_deaths[0:50],
            y_label='COVID Deaths',
            y_values=counties_deaths[0:50],
            title=f'COVID-19 Deaths {state.title()} Counties, New York Times ({counties_last_updated})',
            outfname=f'NYT_COVID_{state}_county_deaths.svg'
        )

    if menu_choice == 3:
        print('Exiting Program. Thank you! ')
        quit()
