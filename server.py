from flask import Flask, render_template
from python import connection

app = Flask(__name__)

@app.route('/')
@app.route('/list')
def route_list():
	all_data = connection.get_all_data(connection.QUESTION_FILE_PATH)
	headers = connection.QUESTION_HEADER
	return render_template('questions_list.html',
						   all_data = all_data,
						   headers = headers)







if __name__ == "__main__":
	app.run(debug = True,
			host = '0.0.0.0',
			port = 8000)