""" Retrieves latest COVID-19 data from The New York Times and creates corresponding Histogram graphs.

Data courtesy of The New York Times for non-commercial use. See LICENSE for mor information.
Author: Richard Nguyen
"""

from helper_functions import get_NYT_COVID_data, graphs_options_menu, get_state_input, svg_cleanup

from text_menu import num_menu

options_menu = (
    'COVID-19 data across all U.S. states',
    'COVID-19 data for counties in a single state',
    'Remove .svg graphs from directory',
    'Exit Program')

while True:
    menu_choice = num_menu('MAIN MENU - Select an Option', options_menu)
    # Choose get data for States
    if menu_choice == 1:
        location_type = 'state'
        # retrieve data for States
        states_data = get_NYT_COVID_data(location_type)
        # graph data by state
        graphs_options_menu(states_data, location_type)
    # Choose get data for counties in a state
    if menu_choice == 2:
        location_type = 'county'
        state = get_state_input()
        # retrieve data for counties
        counties_data = get_NYT_COVID_data(location_type, state=state)
        # graph data by county
        graphs_options_menu(counties_data, location_type, state)
    if menu_choice == 3:
        svg_cleanup()
    if menu_choice == 4:
        print('Exiting Program. Thank you! ')
        quit()
