# COVID data courtesy of New York Times

import requests
import csv
from contextlib import closing
import pygal
from graph_settings import GraphSettings
from helper_functions import get_NYT_COVID_data, create_histogram

us_covid_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us.csv'
us_states_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv'
us_counties_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'

# populate lists with data from API call
states_last_updated, states_list, states_cases, states_deaths = get_NYT_COVID_data(us_states_url)

custom_settings = GraphSettings()
create_histogram(
    x_labels=states_list,
    y_labels=('COVID Cases', 'COVID Deaths'),
    y_values=(states_cases, states_deaths),
    title=f'COVID-19 Cases/Deaths in US States, New York Times ({states_last_updated})',
    outfname='NYT_covid_by_state.svg'
)


# retrieve data for counties
state = 'california'
counties_last_updated, counties_list, counties_cases, counties_deaths = get_NYT_COVID_data(us_counties_url, state=state)


create_histogram(
    x_labels=counties_list,
    y_labels=('COVID Cases', 'COVID Deaths'),
    y_values=(counties_cases, counties_deaths),
    title=f'COVID-19 Cases/Deaths {state.title()} Counties, New York Times ({states_last_updated})',
    outfname='NYT_covid_by_county.svg'
)