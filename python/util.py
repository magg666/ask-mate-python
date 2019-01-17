import data_manager
import connection

def convert_number_to_integer(all_stories):
    """
    Function converts data for business value and estimation into integers
    :param all_stories:all_stories - list of dict
    :return: all_stories - list of dict
    """
    for user_story in all_stories:
        user_story['business_value'] = int(user_story['business_value'])
        user_story['estimation'] = int(user_story['estimation'])
    return all_stories


def sort_by_attributes(all_data, attribute, order):
    """
    Function sorts data based on given parameters
    :param all_data: List of dict
    :param attribute: string
    :param order:
    :return: new_all_data - list of dict
    """
    sort_order = None
    if order == 'desc':
        sort_order = True
    elif order == 'asc':
        sort_order = False
    new_all_data = sorted(all_data, key=lambda k: k[attribute], reverse=sort_order)
    return new_all_data

# pobieranie z formularzy od użytkownika mamy w nastepujących miejscach:
# 1. dodawanie pytania
# 2. edytowanie pytania
# 3. dodawanie odpowiedzi


# 1. dodawanie pytania to
# a) tytuł
# b) treść
# c) ewentualnie obrazek

# def check_title(title):



# 2. edytowanie pytania to
# a) tytuł
# b) treść
# c) ewentualnie obrazek

# 3. dodawanie odpowiedzi to
# a) treść
# b) ewentualnie obrazek
