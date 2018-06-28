from flask import Flask,render_template,url_for,request,flash,redirect,session,make_response
from pymongo import MongoClient
from werkzeug.security import generate_password_hash,check_password_hash
import datetime, pprint,array


app = Flask(__name__)
app.secret_key = str(generate_password_hash("9502276095"))

#Global Variables

det="hmm"
mail="nothing yet"
global details


@app.route('/')
def index():
	return render_template('homepage.html')
	
@app.route('/homepage')
def homepage():
	if 'logged_in' in session:
		return render_template("loginhome.html",det=det)
	else :
		return render_template("homepage.html")

@app.route('/stuReg',methods=['POST','GET'])
def stuReg():
	return render_template("regStudent.html")
	

	
@app.route('/newsFeed')
def newsFeed():
	if 'logged_in' in session:
		client = MongoClient('localhost')
		db = client.ASP
		announce = db.announcements
		posts= announce.find({})
		return render_template("newsfeed.html",det=det,posts=posts)
	
	else :
		return render_template("login.html")
	
@app.route('/login',methods=['POST','GET'])
def login():
	return render_template("login.html")

@app.route('/admReg',methods=['POST','GET'])
def admReg():
	return render_template("regAdmin.html")

@app.route('/recReg',methods=['POST','GET'])
def recReg():
	return render_template("regRecruiter.html")

@app.route('/forum',methods=['POST','GET'])
def forum():
	return render_template("forum.html",det=det)


@app.route('/dataStu',methods=['POST','GET'])
def dataStu():
	client = MongoClient('localhost')
	db = client.ASP
	User = db.userStudents

	firstname = request.form['uname']
	lastname = request.form['uname2']
	email = request.form['email']
	rollnumber=request.form['roll']
	branch = request.form['branchOption']
	gender = request.form['genderOption']
	password = request.form['pass']
	password2=request.form['pass2']

	noOfUsers = User.find({'$or': [{"rollnumber":rollnumber},{"email":email}]}).count()

	if noOfUsers >= 1 :
		error="A user with this Roll Number/Email already exists."
		return render_template("regStudent.html",error=error)
	else :
		if password == password2:
			hashpass=generate_password_hash(password)
			entry  =  {"firstname":firstname,"rollnumber": rollnumber,"lastname":lastname,"email":email,"branch":branch,"gender":gender,"password":hashpass,"aggregate":"Not Defined"}
			document = User.insert_one(entry)
			return render_template("login.html")
		else :
			error="Passwords do not match"
			return render_template("regStudent.html",error=error)
		
@app.route('/dataAdm',methods=['POST','GET'])
def dataAdm():
	client = MongoClient('localhost')
	db = client.ASP
	User = db.userAdmins

	firstname = request.form['uname']
	lastname = request.form['uname2']
	email = request.form['email']
	branch = request.form['branchOption']
	gender = request.form['genderOption']
	phno = request.form['phno']
	password = request.form['pass']
	password2=request.form['pass2']

	noOfUsers = User.find({"email":email}).count()

	if noOfUsers >= 1 :
		error="A user with this email already exists."
		return render_template("regAdmin.html",error=error)
	else :
		if password== password2 :
			hashpass=generate_password_hash(password)
			entry  =  {"firstname":firstname,"lastname":lastname,"phno": phno,"email":email,"branch":branch,"gender":gender,"password":hashpass}
			document = User.insert_one(entry)
			return render_template("login.html")
		else:
			error="Passwords do not match"
			return render_template("regAdmin.html",error=error)
		
	# code for REGISTRATION of users go here:

@app.route('/dataRec',methods=['POST','GET'])
def dataRec():
	client = MongoClient('localhost')
	db = client.ASP
	User = db.userRecruiters

	firstname = request.form['uname']
	lastname = request.form['uname2']
	email = request.form['email']
	NOOrganization = request.form['comName']
	designation = request.form['Desig']
	phno = request.form['phno']
	password = request.form['pass']
	password2=request.form['pass2']

	noOfUsers = User.find({"email":email}).count()

	if noOfUsers >= 1 :
		error="A user with this email already exists."
		return render_template("regRecruiter.html",error=error)
	else :
		if password== password2 :
			hashpass=generate_password_hash(password)
			entry  =  {"firstname":firstname,"lastname":lastname,"email":email,"designation": designation,"phno": phno,"NOOrganization": NOOrganization,"password":hashpass}
			document = User.insert_one(entry)
			return render_template("login.html")
		else:
			error="Passwords do not match"
			return render_template("regRecruiter.html",error=error)		
		
	# LOG IN SECTION STARTS HERE

@app.route('/loginInfo' , methods=['POST','GET'])
def loginInfo():
	client=MongoClient('localhost')
	db=client.ASP
	userType=request.form['userType']
	
	
	global det,mail
	mail=request.form['username']

	# if the user is a student, DO THIS:

	if userType == 'student': 
		det="student"
		User = db.userStudents
		current_user=request.form['username']
		existing_user = User.find_one({"email": current_user})
		if existing_user is None:
			error="Username is incorrect."
			return render_template("login.html",error=error)
		else:
			current_pass=request.form['password']
			existing_pass = existing_user['password']
			
			if check_password_hash(existing_pass, current_pass) :
				session['logged_in'] = True
				return render_template("loginhome.html",det=det)
			else :
				error="Password is incorrect."
				return render_template("login.html",error=error)

		# if the user is an administrator, DO THIS:

	elif userType=='administrator': 
		det="administrator"
		User=db.userAdmins
		current_user=request.form['username']
		existing_user = User.find_one({"email": current_user})
		if existing_user is None:
			error="Username is incorrect"
			return render_template("login.html",error=error)
		else:
			current_pass=request.form['password']
			existing_pass = existing_user['password']
			
			if check_password_hash(existing_pass, current_pass) :
				session['logged_in'] = True
				return render_template("loginhome.html",det=det)
			else :
				error="Password is incorrect."
				return render_template("login.html",error=error)

		# if the user is a recruiter, DO THIS:

	elif userType == 'recruiter': 
		det="recruiter"
		User=db.userRecruiters
		current_user=request.form['username']
		existing_user = User.find_one({"email": current_user})
		if existing_user is None:
			error="Username is incorrect."
			return render_template("login.html",error=error)
		else:
			current_pass=request.form['password']
			existing_pass = existing_user['password']
			
			if check_password_hash(existing_pass, current_pass):
				session['logged_in'] = True
				return render_template("loginhome.html",det=det)
			else :
				error="Password is incorrect."
				return render_template("login.html",error=error)
	
	# log out section :

@app.route('/logout')
def logout():
	session.clear()
	return render_template('/homepage.html')

@app.route('/notifications')
def notifications():
	if 'logged_in' in session:
		return render_template('/notificatins.html')
	else:
		error = 'login to continue'
		return render_template('login.html',error=error)

@app.route('/profile')
def profile():
	if 'logged_in' in session:
		if det == "student":
			stuMail=mail
			client=MongoClient('localhost')
			db=client.ASP
			global details
			
			current_user=db.userStudents.find_one({"email": stuMail})
			firstname=current_user['firstname']
			lastname=current_user['lastname']
			email=current_user['email']
			rlno=current_user['rollnumber']
			branch=current_user['branch']
			gender=current_user['gender']
			aggregate = current_user['aggregate']
			details  =  [firstname,lastname,email,rlno,branch,gender,aggregate]
			
			if db.resumes.find_one({"email" : mail}) :
				d=0
			else :
				d=1
			
			return render_template("studentProf.html",details=details,d=d)
			
		elif det == "administrator":
			return render_template('adminProf.html')
			
		elif det == "recruiter":
			recMail=mail
			client=MongoClient('localhost')
			db=client.ASP
			
			
			current_user=db.userRecruiters.find_one({"email": recMail})
			firstname=current_user['firstname']
			lastname=current_user['lastname']
			email=current_user['email']
			desig=current_user['designation']
			phno=current_user['phno']
			NOOrganization=current_user['NOOrganization']
			details = [firstname,lastname,email,NOOrganization,desig,phno]
			
			if db.resumes.find_one({"email" : mail}) :
				d=0
			else :
				d=1
			
			return render_template("recruiterProf.html",details=details,d=d)
			
	else:
		error = 'login to continue'
		return render_template('login.html',error=error)
		
@app.route('/updateResume')
def updateResume():
	
	if 'logged_in' in session:
		client = MongoClient('localhost',27017)
		db = client.ASP
		res = db.resumes
		resume = res.find_one({'email':mail})

		if resume:
			s1 = resume['CProfile']
			s2 = resume['PStrength'] 
			s3 = resume['TProficiency'] 
			s4 = resume['PExperience'] 
			s5 = resume['PAchievement'] 
			s6 = resume['ECActivities']
			s7 = resume['IAHobby'] 
			s8 = resume['ESummary']
			s9 = resume['PDetail']

			resume_data =[s1,s2,s3,s4,s5,s6,s7,s8,s9]
			return render_template("Resume.html",resume =resume,resume_data=resume_data)

		else:
			return render_template('Resume.html',resume=resume)

		
	else:
		return render_template('login.html')
		
@app.route('/deleteResume')
def deleteResume():
	if 'logged_in' in session:
		client = MongoClient('localhost',27017)
		db = client.ASP
		res = db.resumes
		resume = res.find_one({'email':mail})
		global d
		if resume :
			db.resumes.remove({'email' : mail})
			d=1
		else :
			d=0
			
		return redirect('/profile')
	
	else:
		return render_template('login.html')
			
		

@app.route('/resumeapplication',methods=['POST','GET'])
def resumeapplication():

	if request.method == 'POST':
		f1 = request.form['CProfile']
		f2 =request.form['PStrength']
		f3 =request.form['TProficiency']
		f4 =request.form['PExperience']
		f5 =request.form['PAchievement']
		f6 =request.form['ECActivities']
		f7 =request.form['IAHobby']
		f8 =request.form['ESummary']
		f9 =request.form['PDetail']
		
		client = MongoClient('localhost',27017)
		db = client.ASP
		res = db.resumes
		
		if res.find_one({'email':mail}) :
			db.resumes.remove({"email" : mail})
		

		document = res.insert_one({"email":mail,"CProfile":f1,"PStrength":f2,"TProficiency":f3,"PExperience":f4,"PAchievement":f5,"ECActivities":f6,"IAHobby":f7,"ESummary":f8,"PDetail":f9})
		return redirect('/profile')
		

@app.route('/changepassword',methods=['POST','GET'])
def changepassword():
	if request.method == 'POST':
		if 'logged_in' in session:		
			client = MongoClient('localhost')
			db = client.ASP
			if det=="student":
				User = db.userStudents
			if det=="administrator":
				User = db.userAdmins
			if det=="recruiter":
				User = db.userRecruiters
			
			founduser =  User.find_one({'email':mail})
			existing_pass =founduser['password']
			_id = founduser['_id']
			# collecting form data from studentProf/changepassword

			current_pass = request.form['Cpass']
			new_pass1 = generate_password_hash(request.form['pass'] ) 
			new_pass2 = request.form['pass2'] 
		
			if check_password_hash(existing_pass, current_pass) :
				if check_password_hash(new_pass1,new_pass2):
				
					User.update_one({'_id':_id},{"$set":{'password':new_pass1}})
					error = "password successfully changed"
					if det=="student":
						return render_template('studentProf.html',error=error,details=details)
					if det=="administrator":
						return render_template('adminProf.html',error=error,details=details)
					if det=="recruiter":
						return render_template('recruiterProf.html',error=error,details=details)
				else:
					error="Passwords do not match"
					if det=="student":
						return render_template('studentProf.html',error=error,details=details)
					if det=="administrator":
						return render_template('adminProf.html',error=error,details=details)
					if det=="recruiter":
						return render_template('recruiterProf.html',error=error,details=details)
		else:
			error = "login to change the password"
			return render_template('login.html',error = error)
	if request.method == 'GET':
		return redirect('/profile')
		
@app.route('/changecontact',methods=['POST','GET'])
def changecontact():
	if request.method == 'POST':
		if 'logged_in' in session:		
			client = MongoClient('localhost')
			db = client.ASP
			User=db.userRecruiters
			founduser =  User.find_one({'email':mail})
			existing_pass =founduser['password']
			_id = founduser['_id']
			
			# collecting form data from recruiterProf/changecontact
			
			current_pass = request.form['Cpass']
			if check_password_hash(existing_pass, current_pass) :
				new_contact=request.form['NCNum']
				User.update_one({'_id':_id},{"$set":{'phno':new_contact}})
				error="Contact Number successfully changed"
				return redirect('/profile')
			else :
				error="Password is incorrect"
				return render_template('recruiterProf.html',error=error,details=details)
		else:
			error = "login to change the password"
			return render_template('login.html',error = error)
			
@app.route('/makeAnnouncement',methods=['POST','GET'])
def makeAnnouncement():
	if request.method == 'POST':
		if 'logged_in' in session:		
			client = MongoClient('localhost')
			
			#Getting author's name
			founduser =  client.ASP.userRecruiters.find_one({'email':mail})
			author= founduser['firstname']
			
			db = client.ASP
			User=db.announcements
			
			#Collecting announcement details from the form.
			
			jobtitle=request.form['job_name']
			jobspecs=request.form['job_specification']
			jobdesc=request.form['job_description']
			salary=request.form['salary']
			aggregate=request.form['Baggregate']
			lastdate=request.form['last_date']
			
			#Determining the id of the post
			
			post_id = User.find({}).count() + 1
			
			#Inserting the announcement into a collection called announcements
			
			entry={"post_id":post_id,"email":mail,"author":author,"jobtitle":jobtitle,"jobspecs":jobspecs,"jobdesc":jobdesc,"salary":salary,"aggregate":aggregate,"lastdate":lastdate}
			document = User.insert_one(entry)
			return redirect('/profile')
			
		
		else:
			error = "login to make an announcement"
			return render_template('login.html',error = error)
			
@app.route('/changeagg', methods = ['POST','GET'])
def changeagg():
	global _id,details
	if 'logged_in' in session:
		if request.method == 'POST':
			client = MongoClient('localhost')
			db = client.ASP
			User = db.userStudents
			aggregate = request.form['Agg']
			founduser =  User.find_one({'email':mail})
			existing_pass = founduser['password']	
			if check_password_hash(existing_pass,request.form['Cpass'])	:
				_id = founduser['_id']
				if User.update({'_id':_id},{"$set":{'aggregate':aggregate}}):
					return redirect('/profile')

		if request.method == 'GET' :
			return render_template('studentProf.html',details = details)
	else:
		error = "login to change the aggregate"
		return render_template('login.html',error = error)
		
@app.route("/newsFeed/<int:post_id>")
def post(post_id):
	if 'logged_in' in session:
		client = MongoClient('localhost')
		db = client.ASP
		Post = db.announcements
		post=Post.find_one({"post_id": post_id})
		author_email=post['email']
		author=client.ASP.userRecruiters.find_one({"email":author_email})
		return render_template("post.html",post=post,author=author,det=det)
	else:
		return redirect('/login')
		

@app.route('/deactivate')
def deactivate():
	global mail
	if 'logged_in' in session:
		client = MongoClient('localhost')
		db = client.ASP

		if det == "student":
			User = db.userStudents
			if User.remove({'email' : mail}):
				session.clear()
				return redirect('/homepage')
			else:
				return redirect('/profile')

		if det == "administrator":
			User = db.userAdmins
			if User.remove({'email' : mail}):
				session.clear()
				return redirect('/homepage')
			else:
				return redirect('/profile')
		if det == "recruiter":
			User = db.userRecruiters
			if User.remove({'email' : mail}):
				session.clear()
				return redirect('/homepage')
			else:
				return redirect('/profile')
	else:
		return redirect('/login')

@app.route('/apply',methods=['POST','GET'])
def apply():
	if request.method == 'POST':
		post_id = request.form['post_id']
		if 'logged_in' in session:
			global mail
			client = MongoClient()
			db = client.ASP
			col = db.verified_resumes
			col2 = db.applications

			# checking whether the resume of the user is verifid

			is_verified = col.find_one({'email':mail})

			if is_verified:
				f1 = is_verified['CProfile']
				f2 = is_verified['PStrength']
				f3 = is_verified['TProficiency']
				f4 = is_verified['PExperience']
				f5 = is_verified['PAchievement']
				f6 = is_verified['ECActivities']
				f7 = is_verified['IAHobby']
				f8 = is_verified['ESummary']
				f9 = is_verified['PDetail']
	
			#checking whether the applications has be already submitted to recruiter collection named "applications"

				already_applied = col2.find_one({'email':mail})

			# if already applied , then we should be updating the details of the resume.if not , we should insert the resume as new document in "applications" colleciton

				if already_applied:
					_id = already_applied['_id']
					applications.update({'_id':_id},
						{"$set":{'CProfile':f1,'PStrength':f2,'TProficiency':f3,'PExperience':f4,'PAchievement':f5,'ECActivities':f6,'IAHobby':f7,'ESummary':f8,'PDetail':f9}} )
					return redirect(url_for(post,post_id))
				else:
					applications.insert_one({'mail':mail,'CProfile':f1,'PStrength':f2,'TProficiency':f3,'PExperience':f4,'PAchievement':f5,'ECActivities':f6,'IAHobby':f7,'ESummary':f8,'PDetail':f9})
					return redirect(url_for(post,post_id))
			else:
				error = "your resume is not verified.contact your admin for verification"
				return redirect('/newsFeed')
		else:
			error = "log in to continue"
			return render_template("login.html",error = error)

# @app.route('/unverified')
# def unverified():
# 	client = MongoClient()
# 	db = client.ASP
# 	unverified = db.unverified_resumes

# 	unverified_applications = unverified.find()
# 	return render_template('unverified.html',unverified = unverified_applications)

@app.route('/verify')
def verify():
	if request.method == 'POST':
		client = MongoClient()
		db = client.ASP
		unverified = db.unverified_resumes
		verified = db.verified_resumes
		# if you use post method to send the mail id of the resume that the admin is currently seeing then,
		applicant_mail = request.form['mail']

		my_resume = unverified.find_one({'mail':applicant_mail})
		if my_resume:
			f1 = my_resume['CProfile']
			f2 = my_resume['PStrength']
			f3 = my_resume['TProficiency']
			f4 = my_resume['PExperience']
			f5 = my_resume['PAchievement']
			f6 = my_resume['ECActivities']
			f7 = my_resume['IAHobby']
			f8 = my_resume['ESummary']
			f9 = my_resume['PDetail']
			verified.insert_one({'mail':mail,'CProfile':f1,'PStrength':f2,'TProficiency':f3,'PExperience':f4,'PAchievement':f5,'ECActivities':f6,'IAHobby':f7,'ESummary':f8,'PDetail':f9})
			return redirect('/unverified')
		else:
			return redirect('/unverified')


	
if __name__=='__main__':
	app.run(debug=True)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	