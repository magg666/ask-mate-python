from flask import Flask, render_template, redirect, request, url_for
import uuid
import os
from python import data_manager, connection, util

QUESTION_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/question.csv'
ANSWER_FILE_PATH = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data/answer.csv'
QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']

app = Flask(__name__)


# add sorting
@app.route('/')
@app.route('/list')
def route_questions_list():
    """
    Function supports main and /list page
    :return questions list on page /list:
    """
    all_questions = data_manager.sort_questions()
    for question in all_questions:
        question['submission_time'] = data_manager.convert_timestamp_to_date(int(question['submission_time']))
    return render_template('questions_list.html',
                           all_questions=all_questions)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question_view(question_id):
    """
    Function supports displaying page of given question and all answers for it
    Function generates effects of voting for question and counts views of question
    :param question_id:
    :return: page of given question
    """
    all_answers = connection.get_answers_by_id(ANSWER_FILE_PATH, question_id)
    for answer in all_answers:
        answer['submission_time'] = data_manager.convert_timestamp_to_date(int(answer['submission_time']))
    if request.method == 'GET':
        question = data_manager.change_view_counter(QUESTION_FILE_PATH, QUESTION_HEADER, question_id)
        question['submission_time'] = data_manager.convert_timestamp_to_date(int(question['submission_time']))
        return render_template('question_page.html',
                               question=question,
                               all_answers=all_answers)
    elif request.method == 'POST':
        data_manager.vote_question(QUESTION_FILE_PATH, QUESTION_HEADER, question_id)
        return redirect('/question/' + question_id)


@app.route('/question/<question_id>/<answer_id>', methods=['POST'])
def route_answer_vote(question_id, answer_id):
    """
    Function supports voting for answers
    :param question_id:
    :param answer_id:
    :return: page of given question
    """
    data_manager.vote_answer(ANSWER_FILE_PATH, ANSWER_HEADER, question_id, answer_id)
    return redirect('/question/' + question_id)


@app.route('/question/<question_id>/delete')
def route_delete_question(question_id):
    """
    Function supports deleting questions
    :param question_id:
    :return /list page:
    """
    connection.delete_data_by_id(QUESTION_FILE_PATH, QUESTION_HEADER, question_id)
    return redirect('/list')


@app.route('/answer/<answer_id>/delete')
def route_delete_answer(answer_id):
    """
    Function supports deleting answers
    :param answer_id:
    :return /question page:
    """
    answer = connection.get_question_by_id(ANSWER_FILE_PATH, answer_id)
    question_id = answer["question_id"]
    connection.delete_data_by_id(ANSWER_FILE_PATH, ANSWER_HEADER, answer_id)
    return redirect('/question/' + question_id)


@app.route('/add-question', methods=['POST', 'GET'])
def route_add_question():
    """
    Function supports adding questions to database
    :return: depends of used method
    """
    if request.method == 'POST':
        question_submission_time = data_manager.generate_timestamp()
        question_id = str(uuid.uuid1(clock_seq=question_submission_time))
        question_view = 0
        question_vote = 0
        question = data_manager.create_question(question_submission_time, question_id, question_view, question_vote)
        connection.append_data_in_file(QUESTION_FILE_PATH, question, QUESTION_HEADER)
        return redirect('/question/' + question_id)
    else:
        return render_template('add_question.html',
                               form_url=url_for('route_add_question'))


@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def route_edit_question(question_id):
    """
    Function supports updating question's data
    :param question_id:
    :return: depends of used method
    """
    question = connection.get_question_by_id(QUESTION_FILE_PATH, question_id)
    if request.method == 'GET':
        return render_template('add_question.html',
                               question=question,
                               form_url=url_for('route_edit_question', question_id=question['id']))
    else:
        question_id = question['id']
        question_submission_time = question['submission_time']
        question_view = question['view_number']
        question_vote = question['vote_number']
        update_question = data_manager.create_question(question_submission_time,
                                                       question_id,
                                                       question_view,
                                                       question_vote)
        connection.update_data_by_id(QUESTION_FILE_PATH,
                                     QUESTION_HEADER,
                                     question_id,
                                     update_question)
        return redirect('/')


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_post_answer(question_id):
    """
    Function supports adding answer to question
    :param question_id:
    :return: depends of used method
    """
    given_question = connection.get_question_by_id(QUESTION_FILE_PATH, question_id)
    if request.method == 'GET':
        return render_template('add_answer.html', given_question=given_question, question_id=question_id)
    else:
        answer = data_manager.create_answer(question_id)
        connection.append_data_in_file(ANSWER_FILE_PATH, answer, ANSWER_HEADER)
        return redirect('/question/' + question_id)


@app.route('/list/sorted')
def route_list_sorted():
    all_data = connection.get_all_data(QUESTION_FILE_PATH)
    attribute = request.args.get('attribute')
    order = request.args.get('order')
    sorted_all_data = util.sort_by_attributes(all_data, attribute, order)
    return render_template('questions_list.html',
                           all_questions=sorted_all_data)

    # for question in all_data:
    #     question['submission_time'] = data_manager.convert_timestamp_to_date(int(question['submission_time']))


@app.errorhandler(404)
def route_not_found_error(error):
    return 'Page not found', 404


@app.errorhandler(400)
def route_bad_request_error(error):
    return 'Bad request', 400


if __name__ == "__main__":
    app.run(debug=True,
            host='0.0.0.0',
            port=8000)
