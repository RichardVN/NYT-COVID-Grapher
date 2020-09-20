# COVID data courtesy of New York Times

import requests
import csv
from contextlib import closing
import pygal

us_covid_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us.csv'
us_states_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-states.csv'
us_counties_url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/live/us-counties.csv'

response = requests.get(us_states_url)
if response.status_code != 200:
    print('Failed to retrieve data:', response.status_code)
else:
    with closing(requests.get(us_states_url, stream=True)) as r:
        f = (line.decode('utf-8') for line in r.iter_lines())
        reader = csv.reader(f, delimiter=',', quotechar='"')  # csv row iterator
        # header columns
        header_row = next(reader)

        # list of state data, dictionary for each state
        states_data = []
        for row in reader:
            # convert numbers into ints if possible
            for idx, value in enumerate(row):
                try:
                    row[idx] = int(value)
                except:
                    print('cannot convert to int')
                    pass
            state_dictionary = dict(zip(header_row, row))
            states_data.append(state_dictionary)
            print(row)

    states_data = sorted(states_data, key=lambda state: state.get('cases', 0))
    print(states_data)
    last_updated = states_data[0].get('date', 'No Date')
    states_list = [state['state'] for state in states_data]
    states_cases = [int(state.get('cases', 0)) for state in states_data]
    states_deaths = [int(state.get('deaths', 0)) for state in states_data]

    # graph config settings
    graph_config = pygal.Config(
        show_legend=True,
        x_label_rotation=45,
        title=f"COVID Cases and Deaths in US States ({last_updated}) - NY Times"
    )
    # graph styling
    graph_style = pygal.style.Style(label_font_size=8)

    # pygal histogram - graph COVID data
    states_covid_graph = pygal.Bar(config=graph_config, style=graph_style)
    states_covid_graph.x_labels = states_list
    states_covid_graph.add('Cases', states_cases)
    states_covid_graph.add('Deaths', states_deaths)
    states_covid_graph.render_to_file('NYT_states_covid' + last_updated + '.svg')
