

def convert_number_to_integer(all_questions):
    """
    Function converts data
    :param all_questions: - list of dict
    :return: all_questions - list of dict
    """
    for question in all_questions:
        question['submission_time'] = int(question['submission_time'])
        question['view_number'] = int(question['view_number'])
        question['vote_number'] = int(question['vote_number'])
    return all_questions


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
