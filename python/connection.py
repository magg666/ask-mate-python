# File to handling database as csv
import csv
import os
import shutil

QUESTION_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWER_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def get_all_data(filename):
    """
    Takes all data from database
    and return them
    :param: filename
    return: List of ordered dicts
    """

    with open(filename) as file:
        reader = csv.DictReader(file)
        all_data = [record for record in reader]
        return all_data


def append_data_in_file(filename, data, headers):
    """
    Takes data as arg. and convert it into dictionary using headers as keys.
    And appends dict into database
    param story: filename, data (Q or A), headers
    return: None
    """
    with open(filename, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writerow(data)


def get_question_by_id(filename, data_id):
    """
    Based on given id looks for Q with matching id
    and returns it
    :param: filename, data_id:
    :return: question as a dict
    """
    with open(filename) as file:
        reader = csv.DictReader(file)
        for record in reader:
            if record['id'] == data_id:
                return record


def get_answers_by_id(filename, data_id):
    """
    Based on given id looks for Q/A with matching id
    and returns it
    :param: filename, data_id:
    :return: story as a dict
    """
    with open(filename) as file:
        reader = csv.DictReader(file)
        all_answers = [record for record in reader if record['question_id'] == data_id]
        return all_answers


# rozwiązanie skompilowałam z:
# https://stackoverflow.com/questions/16020858/inline-csv-file-editing-with-python/16020923#16020923
# https://stackoverflow.com/questions/41574037/updating-a-specific-row-in-csv-file
# https://stackoverflow.com/questions/46126082/how-to-update-rows-in-a-csv-file
# polecana metoda aktualizowania - praca na pliku tymczasowym a nie źródłowym
# stąd moduł shutil, który pozwala zamykać, otwierać i kopiować pliki
def update_data_by_id(filename, headers, data_id, new_record):
    """
    Function finds record by given id and changes its data
    :param filename:
    :param headers:
    :param data_id:
    :param new_record:
    :return:
    """
    with open(filename, 'r') as csv_file, open('sample_data/output_file.csv', 'w') as output:
        reader = csv.DictReader(csv_file, fieldnames=headers)
        writer = csv.DictWriter(output, fieldnames=headers)
        for record in reader:
            if record['id'] == data_id:
                record = new_record
            writer.writerow(record)
    shutil.move('sample_data/output_file.csv', filename)


def delete_record_by_id(filename, headers, data_id):
    """
     Function finds data(Q/A) by given id and deletes its
    :param filename:
    :param headers:
    :param data_id:
    :return: list of dict without given record
    """
    with open(filename, 'r') as csv_file, open('output_file.csv', 'w') as output:
        reader = csv.DictReader(csv_file, fieldnames=headers)
        writer = csv.DictWriter(output, fieldnames=headers)
        for record in reader:
            if record['id'] != data_id:
                writer.writerow(record)
    shutil.move('output_file.csv', filename)
