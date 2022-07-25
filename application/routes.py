#region Import
from application import app, api, db
from flask import Response, jsonify, render_template, request, json, redirect, flash, url_for, session
from application.forms import LoginForm, RegisterForm
from application.models import Enrollment, User, Course
from flask_restx import Resource
#endregion

#region Route /
@app.route("/")
@app.route("/index")
@app.route("/home")
# all stacked paths above load index fuction below
def index():
    # renders index.html file inside app/templates
    return render_template("index.html", index=True)
#endregion

#region Route /login
@app.route("/login", methods=['GET', 'POST'])
def login():
    # if user already logged in redirect him to the index page
    if session.get("username"):
        return redirect(url_for("index"))


    # instantiating LoginForm to form variable
    # and passing the instance to the template (html) on return line
    form = LoginForm()
    
    # when the form is submitted it loads itself again.
    # and enters this if below, gives a message and redirects
    if form.validate_on_submit():
        # getting data from submitted form
        email = form.email.data
        password = form.password.data        

        #gets first occurence where email from object matches email from form
        user = User.objects(email=email).first()
        # if user has an object and password matches               
        if user and user.get_password(password):
            flash(f"{user.first_name}, you are successfully logged in!", "success")

            # after logged in store session information globally
            session["user_id"] = user.user_id
            session["username"] = user.first_name

            return redirect("/index")
        else:
            flash("Sorry, ID/Password combination incorrect.", "danger")

    return render_template("login.html", title="Login", form=form, login=True)
#endregion

#region Route /logout
@app.route("/logout")
def logout():
    session['user_id'] = False
    session.pop('username', None)
    return redirect(url_for('index'))
#endregion

#region Route /courses
@app.route("/courses")
@app.route("/courses/<term>") # parameter can be passed on teh URL directly
def courses(term=None): # defines the variable name and default value for the param on url    
    if term is None:
        term = "Spring 2022"

    # get all data from DB
    # classes = Course.objects.all()

    # get sorted data from DB (- or + is optional assending or descending)
    # classes = Course.objects.order_by("-title")
    classes = Course.objects.order_by("courseID")
    return render_template("courses.html", courseData=classes, courses=True, term=term) # passes each variable to html separately
#endregion

#region Route /register
@app.route("/register", methods=["POST", "GET"])
def register():
    if session.get("username"):
        return redirect(url_for("index"))

    form = RegisterForm()
    if form.validate_on_submit():
        # count objects on databse to generate a new user_id
        user_id     = User.objects.count()
        user_id      += 1

        # get data submitted from the form
        email       = form.email.data
        password    = form.password.data
        first_name  = form.first_name.data
        last_name   = form.last_name.data

        # validation is made on the class in forms.py

        # create object with new user
        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        # hash password
        user.set_password(password)
        # save to database
        user.save()

        flash("You are successfully registered", "success")
        return redirect(url_for('index'))

    return render_template("register.html", form=form, title="Register new login", register=True)
#endregion

#region Route /enrollment
# if only GET, no methods param  is needed.
# but if post is needed both get and post needs to be specified
@app.route("/enrollment", methods=["GET", "POST"])
def enrollment():
    # receiving data from the courses.html form (through enrollment function) 
    # with GET
    # $ id = request.args.get('courseID')
    # $ title = request.args.get('title')
    # $ term = request.args.get('term')

    # with POST
    # $ id = request.form.get('courseID')
    # $ title = request.form.get('title')
    # $ term = request.form.get('term')

    # if not logged in, redirect to login page.
    if not session.get('username'):
        flash("Please sign in to manage enrollments.", "warning")
        return redirect(url_for('login'))


    courseID = request.form.get('courseID')
    courseTitle = request.form.get('title')
    # get user id from session
    user_id = session.get('user_id')

    # if user comes from teh enrollment page, it just shows and does not have courseID passed here.
    # if user comes from classes page and clicks enroll, the courseID is presend and processed below
    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Ops.! You are already registered in this course {courseTitle}", "danger")
            return redirect(url_for("courses"))
        else:
            # create object and .Save() to save it.
            # or assign object to a var and save() it.
            Enrollment(user_id=user_id, courseID=courseID).save()            
            flash(f"You are enrolled in {courseTitle}", "success")

    # coding agregation query (join user with course on enrollment table)
    classes = list( User.objects.aggregate(*[
            {
                '$lookup': {
                    'from': 'enrollment', 
                    'localField': 'user_id', 
                    'foreignField': 'user_id', 
                    'as': 'r1'
                }
            }, {
                '$unwind': {
                    'path': '$r1', 
                    'includeArrayIndex': 'r1_id', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course', 
                    'localField': 'r1.courseID', 
                    'foreignField': 'courseID', 
                    'as': 'r2'
                }
            }, {
                '$unwind': {
                    'path': '$r2', 
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': user_id
                }
            }, {
                '$sort': {
                    'courseID': 1
                }
            }
        ]))

    term = request.form.get('term')
    return render_template("enrollment.html", enrollment=True, classes=classes, title="Enrollment")
#endregion

#region Route /testApi
# create test api that returns all data or only one depending on the index
@app.route("/testApi/")
@app.route("/testApi/<idx>")
def testApi(idx=None):
    courseData = [{"courseID":"1111","title":"PHP 111","description":"Intro to PHP","credits":"3","term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":"4","term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":"3","term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":"3","term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":"4","term":"Fall"}]
    if idx ==None:
        jdata = courseData
    else:
        jdata = courseData[int(idx)]
    
    return Response(json.dumps(jdata), mimetype="application/json")
#endregion

#region Route /testuser
@app.route("/testUser")
def user():
    # TEST FUNCTION. NOT USED ON SITE
    # one way to insert data into mongodb (with save())
    # User(user_id=3, first_name="Eduard", last_name="Buhali", 
    #     email="ebuhali@uta.com", password="abc1234").save()
    # User(user_id=4, first_name="Laysa", last_name="Buhali", 
    #     email="lbuhali@uta.com", password="pass1234").save()

    # GETS ALL USERS AND RETURNS TO THE PAGE
    users = User.objects.all()
    return render_template("user.html", users=users)
#endregion


#region API

# for API, decorate with engApi created in __ini__.py intead of app decorator
# name is different to not conflict with app.
@api.route('/api/users')
class GetAndPost(Resource):
    # get all users
    def get(self):
        return jsonify(User.objects.all())
    
    # post user 
    def post(self):
        # flask passes the jason data through the api.payload
        data = api.payload        
        user = User(user_id=data['user_id'], email=data['email'],
                first_name=data['first_name'], last_name=data['last_name'])
        user.set_password(data['password'])
        user.save()
        return jsonify(User.objects(user_id=data['user_id']))

@api.route('/api/user/<idx>')
class GetUpdateDelete(Resource):
    # get one user
    def get(self, idx):
        return jsonify(User.objects(user_id = idx)) 

    # change one user
    def put(self, idx):
        data = api.payload
        # updates the data for the object where (user_id=idx)
        # then **data unpacks the data
        User.objects(user_id=idx).update(**data)
        return jsonify(User.objects(user_id=idx))

    # delete user
    def delete(self, idx):
        User.objects(user_id=idx).delete()
        return jsonify("User is deleted")

#endregion