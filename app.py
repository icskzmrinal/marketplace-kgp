from flask import Flask,request,redirect,url_for,session
from flask import render_template
import pymysql
import pymysql.cursors
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SECRET_KEY']='Thisissecret'

conn = pymysql.connect(host="localhost",user="narainmrinal00",password="30042000",db="marketplace",cursorclass=pymysql.cursors.DictCursor)

@app.route('/')
def index():
	return render_template('login.html')

@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/signup')
def signup():
	return render_template('signup.html')

@app.route('/sign_up',methods=["POST"])
def sign_up():
	name=str(request.form['name'])
	email=str(request.form['email'])
	username=str(request.form['username'])
	password=str(request.form['pass'])
	confirmpass=str(request.form['passrepeat'])
	if confirmpass != password:
		return 'password mismatch'
	else:
		password=sha256_crypt.encrypt(str(password))
		cursor=conn.cursor()
		cursor.execute("INSERT INTO userdata (name,email,username,password) VALUES(%s,%s,%s,%s)",(name,email,username,password))
		conn.commit()
		cursor.close()
		return redirect(url_for("login"))

@app.route('/log_in',methods=["GET","POST"])
def log_in():

	username=str(request.form['username'])
	password_candidate=str(request.form['pass'])

	cursor=conn.cursor()

	result=cursor.execute("SELECT*FROM userdata WHERE username=%s",[username])
	
	if result > 0:
		user=cursor.fetchone()
		passwordreal=str(user['password'])
		if sha256_crypt.verify(password_candidate,passwordreal):
			session['logged_in']=True
			session['username']=username
			
			return redirect(url_for('home'))
		else:
			return "invalid username or password"
		cursor.close()
	else:
		app.logger.info('NO USER')
		return "invalid username or password"

@app.route('/home')
def home():
	if session['logged_in']==True:
		return render_template('home.html')
	else:
		return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session.clear()
	session['logged_in']=False
	return redirect(url_for('login'))


if __name__ == '__main__': 
	app.run(debug=True)

	