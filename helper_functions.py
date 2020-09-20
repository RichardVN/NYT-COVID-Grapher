import requests
import csv
from contextlib import closing
import pygal
from graph_settings import GraphSettings


def get_NYT_COVID_data(url: str, state=None):
    """
    API call to New York Times github, retrieves COVID-19 data
    :param url: str
    :param state: str specifies to retrieve counties data from single state
    :return: (last_updated:str, locations_list: List[str], locations_cases: List[int], locations_deaths: List[int])
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
            locations_data = sorted(locations_data, key=lambda location: location.get('cases', 0), reverse=True)
            print(f"successful retrieval of data covid by {location_type}")
            print('\t', locations_data[0:4], '...')

            # fill data lists
            locations_list, locations_cases, locations_deaths = [], [], []
            for location_dic in locations_data:
                # load states/counties
                locations_list.append(location_dic[location_type])
                # populate cases
                locations_cases.append(location_dic['cases'])
                # populate deaths
                locations_deaths.append(location_dic['deaths'])

            last_updated = locations_data[0]['date']

            return last_updated, locations_list, locations_cases, locations_deaths
        else:
            print('Error in retrieving data')


def create_histogram(x_labels, y_labels, y_values, title='', outfname='graph.svg', config=None, style=None):
    """

    :param title:
    :param x_labels:
    :param y_labels: Tuple(str)
    :param y_values: Tuple(List[int])
    :param config:
    :param style:
    :return: output .svg file
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
    if len(y_labels) == len(y_values):
        for label, value_list in zip(y_labels, y_values):
            graph.add(label, value_list)
        graph.render_to_file(outfname)
        print('Created histogram:', outfname)
    else:
        print("arguments must be in tuples or lists")


