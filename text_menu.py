""" Text based menu for user to navigate through features via Command Line """


def num_menu(option_list):
    """ Prompts user with a text-based menu of options. User must enter an integer value

    :param option_list: list of strings representing program options
    :type option_list: list
    :return: the number representing the user choice
    :rtype: int
    """
    valid_choice = False
    user_choice = None
    while not valid_choice:
        # show Menu prompt
        print('-' * 30, 'MENU - Pick one of the following options', '-' * 25, sep='\n')

        for idx, choice in enumerate(option_list, start=1):
            print(f"{idx}: {choice}")

        user_choice = input('Enter your choice: ')

        try:
            # convert choice to integer
            user_choice = int(user_choice)
        except ValueError:
            print('ERROR: Please enter an integer value.')
        else:
            # check if choice is within bounds of choices
            if user_choice in range(1, len(option_list)+1):
                valid_choice = True
            else:
                print('ERROR: That is not one of the options.')

    return user_choice
