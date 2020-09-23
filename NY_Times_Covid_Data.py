""" Retrieves latest COVID-19 data from The New York Times and creates corresponding Histogram graphs.

Data courtesy of The New York Times for non-commercial use.
"""

from graph_settings import GraphSettings
from helper_functions import get_NYT_COVID_data, create_histogram

us_covid_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us.csv'
us_states_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv'
us_counties_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'

# retrieve data for States
states_last_updated, states_list_by_cases, states_cases, states_list_by_deaths, states_deaths = \
    get_NYT_COVID_data(us_states_url)

custom_settings = GraphSettings()
# graphs cases per state
create_histogram(
    x_labels=states_list_by_cases,
    y_label='COVID Cases',
    y_values=states_cases,
    title=f'COVID-19 Cases in US States, New York Times ({states_last_updated})',
    outfname='NYT_COVID_state_cases.svg'
)
# graph deaths per state
create_histogram(
    x_labels=states_list_by_deaths,
    y_label='COVID Deaths',
    y_values=states_deaths,
    title=f'COVID-19 Deaths in US States, New York Times ({states_last_updated})',
    outfname='NYT_COVID_state_deaths.svg'
)


# retrieve data for counties
state = 'california'
counties_last_updated, counties_list_by_cases, counties_cases, counties_list_by_deaths, counties_deaths =\
    get_NYT_COVID_data(us_counties_url, state=state)
# graph cases per county
create_histogram(
    x_labels=counties_list_by_cases,
    y_label='COVID Cases',
    y_values=counties_cases,
    title=f'COVID-19 Cases {state.title()} Counties, New York Times ({states_last_updated})',
    outfname='NYT_COVID_county_cases.svg'
)
# graph deaths per county
create_histogram(
    x_labels=counties_list_by_deaths,
    y_label='COVID Deaths',
    y_values=counties_deaths,
    title=f'COVID-19 Deaths {state.title()} Counties, New York Times ({states_last_updated})',
    outfname='NYT_COVID_county_deaths.svg'
)