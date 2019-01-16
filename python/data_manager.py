import time
import uuid
from flask import request
from python import connection
import server


def generate_timestamp():
    """
    Function generates timestamp in epoch format
    :return: timestamp (10 numbers)
    """
    timestamp = int(time.time())
    return timestamp


def convert_timestamp_to_date(timestamp):
    """
    Function converts 10-digit timestamp into normal format date
    :param timestamp:
    :return: date
    """
    return time.strftime("%a, %d %b %Y %H:%M:%S", (time.gmtime(timestamp)))


def create_question(question_submission_time, question_id, question_view, question_vote):
    """
    Function gets data from page-form and merge them into question
    :param question_submission_time:
    :param question_id:
    :param question_view:
    :param question_vote:
    :return: question - dictionary
    """
    question_title = request.form['title']
    question_message = request.form['message']
    question_image = request.form['image']
    question = {"id": question_id,
                "submission_time": question_submission_time,
                "view_number": question_view,
                "vote_number": question_vote,
                "title": question_title,
                "message": question_message,
                "image": question_image}
    return question


def create_answer(question_id):
    """
    Function gets data from page_form and merges it into answer
    :param question_id:
    :return: answer - dictionary
    """
    answer_submission_time = generate_timestamp()
    answer_id = str(uuid.uuid1(clock_seq=answer_submission_time))
    answer_vote = 0
    answer_message = request.form['message']
    answer_image = request.form['image']
    answer = {"id": answer_id,
              "submission_time": answer_submission_time,
              "vote_number": answer_vote,
              "question_id": question_id,
              "message": answer_message,
              "image": answer_image}
    return answer


def find_one_answer_from_all_for_one_question(question_id, answer_id):
    """
    Function choose one answer from list of all answers
    :param question_id:
    :param answer_id:
    :return: answer - dictionary
    """
    all_answers = connection.get_answers_by_id(server.ANSWER_FILE_PATH, question_id)
    for answer in all_answers:
        if question_id == answer['question_id'] and answer_id == answer['id']:
            return answer


def vote_question(filename, headers, question_id):
    """
    Function counts voting for question
    :param filename:
    :param headers:
    :param question_id:
    :return: none, only writes into database
    """
    question = connection.get_question_by_id(filename, question_id)
    vote_counter = int(question['vote_number'])
    if request.form['vote_button'] == 'plus':
        vote_counter += 1
    elif request.form['vote_button'] == 'minus':
        vote_counter -= 1
    question['vote_number'] = str(vote_counter)
    connection.update_data_by_id(filename, headers, question_id, question)


def vote_answer(filename, headers, question_id, answer_id):
    """
    Function counts voting for question
    :param filename:
    :param headers:
    :param question_id:
    :param answer_id:
    :return: none, only writes into database
    """
    answer = find_one_answer_from_all_for_one_question(question_id, answer_id)
    vote_counter = int(answer['vote_number'])
    if request.form['vote_button'] == 'plus':
        vote_counter += 1
    elif request.form['vote_button'] == 'minus':
        vote_counter -= 1
    answer['vote_number'] = str(vote_counter)
    connection.update_data_by_id(filename, headers, answer_id, answer)


def change_view_counter(filename, headers, question_id):
    """
    Function counts how many time was question viewed in single question page view
    :param filename:
    :param headers:
    :param question_id:
    :return: returns question with updated view counts (dictionary)
    """
    question = connection.get_question_by_id(filename, question_id)
    view_counter = int(question['view_number'])
    view_counter += 1
    question['view_number'] = view_counter
    connection.update_data_by_id(filename, headers, question_id, question)
    return question


def sort_questions():
    """
    Function sorts data by time
    :return: list of dictionary
    """
    all_data = connection.get_all_data(server.QUESTION_FILE_PATH)
    sorted_all_data = sorted(all_data, key=lambda k: k["submission_time"], reverse=True)
    return sorted_all_data
