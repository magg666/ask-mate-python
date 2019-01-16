from flask import Flask, render_template, redirect, request, url_for
from python import connection

import uuid
import csv
import shutil
from python import data_manager, connection

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    all_data = connection.get_all_data(connection.QUESTION_FILE_PATH)
    headers = connection.QUESTION_HEADER
    return render_template('questions_list.html',
                           all_data=all_data,
                           headers=headers)


@app.route('/question/<question_id>', methods=['GET', 'POST'])
def route_question_view(question_id):
    single_question = connection.get_question_by_id(
        connection.QUESTION_FILE_PATH, question_id)
    all_answers = connection.get_answers_by_id(
        connection.ANSWER_FILE_PATH, question_id)
    view_counter = int(single_question['view_number'])
    vote_counter = int(single_question['vote_number'])
    if request.method == 'GET':
        view_counter += 1
        single_question['view_number'] = str(view_counter)
        connection.update_data_by_id(
            connection.QUESTION_FILE_PATH, connection.QUESTION_HEADER, question_id, single_question)
        return render_template('question_page.html',
                               single_question=single_question,
                               all_answers=all_answers)
    elif request.method == 'POST':
        if request.form['vote_button'] == 'plus':
            vote_counter += 1
        elif request.form['vote_button'] == 'minus':
            vote_counter -= 1
        single_question['vote_number'] = str(vote_counter)
        connection.update_data_by_id(connection.QUESTION_FILE_PATH, connection.QUESTION_HEADER, question_id,
                                     single_question)
        return render_template('question_page.html',
                               single_question=single_question,
                               all_answers=all_answers)


@app.route('/question/<question_id>/delete')
def route_delete_question(question_id):
    connection.delete_record_by_id(
        connection.QUESTION_FILE_PATH, connection.QUESTION_HEADER, question_id)
    return redirect('/')


@app.route('/answer/<answer_id>/delete')
def route_delete_answer(answer_id):
    connection.delete_record_by_id(
        connection.ANSWER_FILE_PATH, connection.ANSWER_HEADER, answer_id)
    return redirect('/')  # rozwiązać przekierowanie na stronę pytania
    all_data = connection.get_all_data(connection.QUESTION_FILE_PATH)
    headers = connection.QUESTION_HEADER
    return render_template('questions_list.html',
                           all_data=all_data,
                           headers=headers)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# KACPER'S FUNCTIONS

# ADD QUESTION
@app.route('/add-question', methods=['POST', 'GET'])
def add_question():

        # IF METHOD IS POST (IF FORM IS SUBMITTED) -> THEN APPEND DATA IN CSV FILE
    if request.method == 'POST':

        question_title = request.form['question_title']
        question_message = request.form['question_message']
        question_url = request.form['url_address']

        question_actual_time = data_manager.generate_timestamp()
        question_id = str(uuid.uuid1(clock_seq=question_actual_time))

        # SAVE TO CSV FILE
        # IT NEEDS TO BE CHANGED TO MAGDA'S FUNCTIONS (I DIDN'T KNOW HOW TO TRANSLATE CONTENT OF THE CSV FILE TO A DICT)
        with open('sample_data/question.csv', 'a', newline='') as csvfile:
            headers_of_the_csv_table = [
                'id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
            writer = csv.DictWriter(
                csvfile, fieldnames=headers_of_the_csv_table)
            writer.writerow({'id': question_id,
                             'submission_time': question_actual_time,
                             'view_number': 1,  # IT NEEDS TO BE CHANGED
                             'vote_number': 2,  # IT NEEDS TO BE CHANGED
                             'title': question_title,
                             'message': question_message,
                             'image': question_url})
            return redirect('/question/' + question_id)

    # ELSE (IF METHOD IS GET) -> SHOW THE FORM TO FILL
    else:
        return render_template('add_question.html',
                               form_url=url_for('add_question'))


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# EDIT QUESTION
@app.route('/question/<question_id>/edit', methods=['POST', 'GET'])
def edit_question(question_id):
    record = connection.get_question_by_id("sample_data/question.csv", question_id)
    if request.method == 'GET':

        return render_template('add_question.html',
                               record=record,
                               form_url=url_for('edit_question', question_id=record['id']))

    else:
        id = record['id']
        submission_time = record['submission_time']
        view_number = record['view_number']
        vote_number = record['vote_number']
        title = request.form['question_title']
        message = request.form['question_message']
        image = request.form['url_address']

        update_question = {'id' : id,
                           'submission_time': submission_time,
                           'view_number': view_number,
                           'vote_number': vote_number,
                           'title': title,
                           'message': message,
                           'image': image}

        connection.update_data_by_id(connection.QUESTION_FILE_PATH, connection.QUESTION_HEADER, question_id, update_question)
        return redirect('/')

########################################################################################################################################
# CHANGE THE ROW WITH GIVEN ID INTO DICTIONARY


# def change_founded_row_by_id_into_dict(question_id):

#     # VARIABLES FROM UPDATED FORM
#     question_title_from_form = request.form['question_title']
#     question_content_from_form = request.form['question_message']
#     question_url_img = request.form['url_address']

#     founded_row_transformed_into_dict = {'id': question_id,
#                                          'submission_time': 
#                                          id,submission_time,view_number,vote_number,title,message,image}

#     return founded_row_transformed_into_dict

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


if __name__ == "__main__":
    app.run(debug=True,
            host='0.0.0.0',
            port=8000)
