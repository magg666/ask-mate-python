from flask import Flask, render_template, redirect, request
from python import connection

import uuid
import csv
from python import data_manager

app = Flask(__name__)

headers = connection.QUESTION_HEADER

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
		return render_template('add_question.html') 
							
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 






if __name__ == "__main__":
	app.run(debug = True,
			host = '0.0.0.0',
			port = 8000)