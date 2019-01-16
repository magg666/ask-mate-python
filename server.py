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
						   all_data = all_data,
						   headers = headers)


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
		question_id = str(uuid.uuid1(clock_seq = question_actual_time))

		# SAVE TO CSV FILE 
		# IT NEEDS TO BE CHANGED TO MAGDA'S FUNCTIONS (I DIDN'T KNOW HOW TO TRANSLATE CONTENT OF THE CSV FILE TO A DICT)	
		with open('sample_data/question.csv', 'a', newline='') as csvfile:
			headers_of_the_csv_table = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
			writer = csv.DictWriter(csvfile, fieldnames = headers_of_the_csv_table)
			writer.writerow({'id': question_id,
							'submission_time': question_actual_time, 
							'view_number': 1, #IT NEEDS TO BE CHANGED
							'vote_number': 2, #IT NEEDS TO BE CHANGED
							'title': question_title, 
							'message': question_message, 
							'image': question_url})
			return redirect('/question/' + question_id)

	# ELSE (IF METHOD IS GET) -> SHOW THE FORM TO FILL
	else:
		return render_template('add_question.html',
							   form_url = url_for('add_question')) 


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# EDIT QUESTION
@app.route('/question/<question_id>/edit', methods=['POST','GET'])
def edit_question(question_id):

	if request.method == 'GET':
		record = connection.get_data_by_id("sample_data/question.csv", question_id)
		return render_template('add_question.html',
								record = record,
								form_url = url_for('edit_question', question_id = record['id']))
	
	else:
		founded_row_as_dict = change_founded_row_by_id_into_dict(question_id)
		headers_of_the_csv_table = ['id','submission_time','view_number','vote_number','title','message','image']
		
		with open('sample_data/question.csv', 'r') as csv_file, open('output_file.csv', 'w') as output:
			reader = csv.DictReader(csv_file, fieldnames = headers_of_the_csv_table)
			writer = csv.DictWriter(output, fieldnames = headers_of_the_csv_table)
			for story in reader:
				if story['id'] == question_id:
					story = {k: founded_row_as_dict[k] for k in story}
				writer.writerow(story)
			shutil.move('output_file.csv', 'sample_data/question.csv')

########################################################################################################################################
# CHANGE THE ROW WITH GIVEN ID INTO DICTIONARY


def change_founded_row_by_id_into_dict(id):

    # VARIABLES FROM UPDATED FORM
    question_title_from_form = request.form['question_title']
    question_content_from_form = request.form['question_message']
    question_url_img = request.form['url_address']

    founded_row_transformed_into_dict = {'title': question_title_from_form, 
                                         'message': question_content_from_form, 
                                         'image': question_url_img}

    return founded_row_transformed_into_dict

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 






if __name__ == "__main__":
	app.run(debug = True,
			host = '0.0.0.0',
			port = 8000)