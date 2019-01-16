# File to handling database as csv
import csv
import shutil


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


def get_question_by_id(filename, question_id):
	"""
	Based on given id looks for Q with matching id
	and returns it
	:param: filename, question_id:
	:return: question as a dict
	"""
	with open(filename) as file:
		reader = csv.DictReader(file)
		for question in reader:
			if question['id'] == question_id:
				return question


def get_answers_by_id(filename, question_id):
	"""
	Based on given id looks for A with matching id
	and returns it
	:param: filename, answer_id:
	:return: answers as a list of dicts
	"""
	with open(filename) as file:
		reader = csv.DictReader(file)
		all_answers = [answer for answer in reader if answer['question_id'] == question_id]
		return all_answers


def update_data_by_id(filename, headers, data_id, new_data):
	"""
	Function finds data (Q/A) by given id and changes it
	:param filename:
	:param headers:
	:param data_id:
	:param new_data:
	:return: None
	"""
	with open(filename, 'r') as csv_file, open('sample_data/output_file.csv', 'w') as output:
		reader = csv.DictReader(csv_file, fieldnames=headers)
		writer = csv.DictWriter(output, fieldnames=headers)
		for data in reader:
			if data['id'] == data_id:
				data = new_data
			writer.writerow(data)
	shutil.move('sample_data/output_file.csv', filename)


def delete_data_by_id(filename, headers, data_id):
	"""
	 Function finds data(Q/A) by given id and deletes it
	:param filename:
	:param headers:
	:param data_id:
	:return: list of dict without given data
	"""
	with open(filename, 'r') as csv_file, open('output_file.csv', 'w') as output:
		reader = csv.DictReader(csv_file, fieldnames=headers)
		writer = csv.DictWriter(output, fieldnames=headers)
		for data in reader:
			if data['id'] != data_id:
				writer.writerow(data)
	shutil.move('output_file.csv', filename)
