from flask import Flask,render_template, request, jsonify, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'doctors'
app.secret_key = 'your secret key'

mysql = MySQL(app)

@app.route('/')
def index():
    return jsonify("Hello")

@app.route('/doclist',methods=['POST','GET'])
def doc_list():
    cur = mysql.connection.cursor()
    if request.method == "GET":
        cur.execute('''SELECT name,domain,qualification FROM doclist''')
        result = cur.fetchall()
        print (result)
        return jsonify(result)
    if request.method == "POST":
        new_id = request.form["id"]
        new_name = request.form["name"]
        new_mobile = request.form["domain"]
        new_email = request.form["qualification"]
        new_address = request.form["experience"]
        new_date = request.form["email"]
        new_time = request.form["specialities"]
        new_password = request.form["password"]
        sql = """INSERT INTO doclist (id, name, domain, qualification, experience, email, specialities, password)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor = cur.execute(sql, (new_id, new_name, new_mobile, new_email, new_address, new_date, new_time, new_password))
        mysql.connection.commit()
        session['name'] = new_name
        session['email'] = new_email
    return jsonify('Added')

@app.route("/doclist/<int:id>", methods=["GET", "PUT"])
def specific_doctor(id):
    cur = mysql.connection.cursor()
    doctor = None
    if request.method == "GET":
        cur.execute("SELECT name,domain,qualification, experience, specialities FROM doclist WHERE id=%s", (id,))
        rows = cur.fetchall()
        for r in rows:
            doctor = r
        if doctor is not None:
            return jsonify(doctor)
        else:
            return "Something wrong"

@app.route('/login', methods=['GET','POST'])
def login_doctor():
    if request.method == "POST":
        log = True
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM doclist WHERE email = %s AND password = %s', (email, password,))
        user = cur.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['email'] = user['email']
            return jsonify('Logged in successfully!')
        else:
            return jsonify('Incorrect username/password!')
    return "logged in successfully!"

@app.route("/logout")
def logout_doctor():
    session.clear()
    return jsonify("You're logged out!")



if __name__ == "__main__":
    app.run()