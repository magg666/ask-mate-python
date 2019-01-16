import time
import uuid
from flask import request
from python import connection
import server


def generate_timestamp():
	current_time = int(time.time())
	return current_time


def create_question(question_submission_time, question_id, question_view, question_vote):
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

def sort_questions():
	all_data = connection.get_all_data(server.QUESTION_FILE_PATH)
	sorted_all_data = sorted(all_data, key=lambda k: k["submission_time"], reverse = True)
	return sorted_all_data

