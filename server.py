from flask import Flask, render_template, request, redirect
from python import connection

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
	single_question = connection.get_question_by_id(connection.QUESTION_FILE_PATH, question_id)
	all_answers = connection.get_answers_by_id(connection.ANSWER_FILE_PATH, question_id)
	view_counter = int(single_question['view_number'])
	vote_counter = int(single_question['vote_number'])
	if request.method == 'GET':
		view_counter += 1
		single_question['view_number'] = str(view_counter)
		connection.update_data_by_id(connection.QUESTION_FILE_PATH, connection.QUESTION_HEADER, question_id,
									 single_question)
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
	connection.delete_record_by_id(connection.QUESTION_FILE_PATH, connection.QUESTION_HEADER, question_id)
	return redirect('/')


@app.route('/answer/<answer_id>/delete')
def route_delete_answer(answer_id):
	connection.delete_record_by_id(connection.ANSWER_FILE_PATH, connection.ANSWER_HEADER, answer_id)
	return redirect('/')  # rozwiązać przekierowanie na stronę pytania


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def route_post_answer(question_id):
	given_question = connection.get_question_by_id(connection.QUESTION_FILE_PATH, question_id)
	if request.method == 'GET':
		return render_template('add_answer.html', given_question=given_question, question_id=question_id)
	else:
		message = request.form['message']
		image = request.form['image']
		answer = {"id": 15, "submission_time": 1236547891, "vote_number": 0, "question_id": question_id,
				  "message": message, "image": image}
		connection.append_data_in_file(connection.ANSWER_FILE_PATH, answer, connection.ANSWER_HEADER)
		return redirect('/')  # rozwiązać przekierowanie na stronę pytania


if __name__ == "__main__":
	app.run(debug=True,
			host='0.0.0.0',
			port=8000)
