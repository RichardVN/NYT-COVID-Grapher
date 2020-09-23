""" Helper functions to make retrieve COVID-19 Data and to create PyGal Histograms """

import requests
import csv
from contextlib import closing

import pygal

from graph_settings import GraphSettings


def get_NYT_COVID_data(url, state=None):
    """API call to New York Times github using url.  Retrieves latest COVID data in U.S.

    :param url: the url needed to make API call to retrieve COVID data from gitihub repo
    :type url: str
    :param state: if provided, limits the retrieval of data by counties to the specified State (default is None)
    :type state: str
    :return: tuple of last update date, list of locations and corresponding lists of COVID cases and deaths
    :rtype: tuple(str, list[str], list[int], list[str], list[int], list[int])
    """
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
                location_dictionary = dict(zip(header_row, row))
                locations_data.append(location_dictionary)

        if locations_data:

            print(f"successful retrieval of data covid by {location_type}")
            print('\t', locations_data[0:4], '...')

            # fill data lists, sorted from highest cases to lowest
            locations_data = sorted(locations_data, key=lambda location: location.get('cases', 0), reverse=True)
            locations_list_by_cases, locations_cases = [], []
            for location_dic in locations_data:
                # load states/counties
                locations_list_by_cases.append(location_dic[location_type])
                # populate cases
                locations_cases.append(location_dic['cases'])

            # fill data lists, sorted from highest deaths to lowest
            locations_data = sorted(locations_data, key=lambda location: location.get('deaths', 0), reverse=True)
            locations_list_by_deaths, locations_deaths = [], []
            for location_dic in locations_data:
                # load states/counties
                locations_list_by_deaths.append(location_dic[location_type])
                # populate cases
                locations_deaths.append(location_dic['deaths'])

            last_updated = locations_data[0]['date']

            return last_updated, locations_list_by_cases, locations_cases, locations_list_by_deaths, locations_deaths
        else:
            print('Error in retrieving data')


def create_histogram(x_labels, y_label, y_values, title='', outfname='graph.svg', config=None, style=None):
    """ Uses PyGal to create histogram from lists of labels and values.  Outputs .svg file

    :param x_labels: A list of strings to label the x axis
    :type x_labels: list
    :param y_label: label the type of value plotted.
    :type y_label: str
    :param y_values: list contains values corresponding to a y_label
    :type y_values: list
    :param title: The title of the chart
    :type title: str
    :param outfname: name of the file that the graph will be saved as (preferably .svg)
    :type outfname: str
    :param config: pygal Config class for graph layout settings (default is None)
    :type config: pygal.Config()
    :param style: pygal Style class for custom visuals (default is None)
    :type style: pygal.style.Style
    :return: None
    :rtype: None
    """
    if config is None or style is None:
        default_settings = GraphSettings()
        config = default_settings.config
        style = default_settings.style
    else:
        config = config
        style = style

    config.title = title
    graph = pygal.Bar(config=config, style=style)
    graph.x_labels = x_labels
    # add y values
    graph.add(y_label, y_values)
    graph.render_to_file(outfname)
    print('Created histogram:', outfname)
