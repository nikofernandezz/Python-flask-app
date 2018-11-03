# Import flask
from flask import Flask, render_template, request, redirect, url_for, flash
# Import flask-mysql library
from flaskext.mysql import MySQL

app = Flask(__name__)

# Secret key for flash message
app.secret_key = "flash message"

# Configuration and Initialization of MySQL
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 8889
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'flask_crud_app'

# Initialize the extension
mysql = MySQL()
mysql.init_app(app)



#Returns the homepage 'index.html'
@app.route('/')
def index():

	#Getting all student data from the database
	# btain cursor
	cursor = mysql.get_db().cursor()
	# Select all data of each students Query
	cursor.execute("SELECT * FROM students")
	# Initialize all selected students into the variable data
	data = cursor.fetchall()
	# Close the opened file
	cursor.close()
	# Redirect to the index.html page
	return render_template('index.html', students = data)





#Inserting data (Add Student) to the database
@app.route('/insert', methods = ['POST'])
def insert():

	# Checks if the method from the form is POST
	if request.method == 'POST':
		# Flash notification when you Added a student
		flash('Data Inserted Successfully')

		# Get the name, email and contact_number on the html form and initialize into a variable
		name = request.form['name']
		email = request.form['email']
		contact_number = request.form['contact_number']

		# Obtain a cursor
		cursor = mysql.get_db().cursor()
		# Insert data Query
		cursor.execute("INSERT INTO students (name, email, contact_number) VALUES (%s,%s,%s)", (name, email, contact_number))
		# Commit the Query
		mysql.get_db().commit()
		# Redirect to the index.html page
		return redirect(url_for('index'))




#Updating data from the database
@app.route('/update', methods = ['POST', 'GET'])
def update():

	# Checks if the method from the form is POST
	if request.method == 'POST':
		# Flash notification when you Updated a student
		flash('Data Updated Successfully')
		# Get the id_data, name, email and contact_number on the html form and initialize into a variable
		id_data = request.form['id']
		name = request.form['name']
		email = request.form['email']
		contact_number = request.form['contact_number']

		# Obtain a cursor
		cursor = mysql.get_db().cursor()
		# Update data Query
		cursor.execute(""" 
		UPDATE students
		SET name=%s, email=%s, contact_number=%s
		WHERE id=%s

		""", (name, email, contact_number, id_data))
		flash("Data Updated Successfully")
		# Commit the Query
		mysql.get_db().commit()
		# Redirect to the index.html page
		return redirect(url_for('index'))




# Deleting data from the database
@app.route('/delete/<string:id_data>', methods = ['POST', 'GET'])
def delete(id_data):
		# Flash notification when you Deleted a student
		flash('Data Deleted Successfully')
		# Obtain a cursor
		cursor = mysql.get_db().cursor()
		# Delete data Query
		cursor.execute("DELETE FROM students WHERE id = %s", (id_data))
		# Commit the Query
		mysql.get_db().commit()
		# Redirect to the index.html page
		return redirect(url_for('index'))





# Server Configurations
if __name__ == "__main__":
	# Reloads the template without restarting the server
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run()

