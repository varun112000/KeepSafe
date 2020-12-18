from Application import app
from flask import render_template, request, url_for, flash, redirect,session
from Application import User, WebPassword
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId


@app.route('/')
@app.route('/home')
def index():  
    if session.get('name'):
        return render_template('index.html',websites=list(WebPassword.find({'name':session.get('name'),'email':session.get('email')})))
    else:
        return redirect('/login')

@app.route('/home/add', methods = ['GET', 'POST'])
def add_password():
    if request.method == "GET":
        if session.get('name'):
            return render_template('addPassword.html')
        else:
            return redirect('/login')
    elif request.method == "POST":
        if WebPassword.find_one({"name":session.get('name'), 'email':session.get('email'), 'website':request.form['website'], 'websitePassword':request.form['websitePassword']}): 
            return render_template('index.html',websites=list(WebPassword.find({'name':session.get('name'),'email':session.get('email')})))
        else:
            WebPassword.insert_one({"name":session.get('name'), 'email':session.get('email'), 'website':request.form['website'], 'websitePassword':request.form['websitePassword']})
            return render_template('index.html',websites=list(WebPassword.find({'name':session.get('name'),'email':session.get('email')})))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if session.get('name'):
        flash("Already Logged In", "info")
        return redirect('/')

    if request.method == "POST":
        if User.find_one({'email':request.form['email']}):
            if check_password_hash(User.find_one({'email':request.form['email']})['password'], request.form['password']):
                flash("Logged In","success")
                session['name'] = User.find_one({'email':request.form['email']})['name']
                session['email'] = User.find_one({'email':request.form['email']})['email']
                return redirect("/")
            else:
                flash("Incorrect Password", "danger")
                return redirect("/login")
        else:
            flash("Email Not Found, Register Here", "danger")
            return redirect("/register")

    return render_template('login.html')

@app.route('/about_us')
def aboutus():
    return render_template('about_us.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if session.get('name'):
        flash("Already Registered", "info")
        return redirect('/')

    if request.method == "POST":
        if User.find_one({'email':request.form['email']}):
            flash("Email Already Exist's","danger")
            return redirect("/register")

        else:    
            password = generate_password_hash(request.form['password'])
            User.insert_one({'name':request.form['name'], 'phone_number':request.form['phonenumber'],'email':request.form['email'], 'password':password})
            flash("You are Successfully Registered","success")
            return redirect("/login")

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('name',None)
    session.pop('email',None)
    flash("Successfully logged out",'success')
    return redirect('/')

@app.route('/home/edit/<string:idx>' ,methods = ['GET', 'POST'])
def edit(idx=None):
    if request.method=="POST":
        WebPassword.find_one_and_update({'_id':ObjectId(idx)},{"$set":{'website':request.form['website'], 'websitePassword':request.form['websitePassword']}})
        return redirect('/')
    else:
        data = list(WebPassword.find({'_id':ObjectId(idx)}))[0]
        web = dict()
        web['id'] = idx
        web['website'] = data['website']
        web['webPassword'] = data['websitePassword']
        print(web) 
        return render_template('edit.html', web=web)


@app.route('/home/delete/<string:idx>')
def delete(idx=None):
    result = WebPassword.delete_one({'_id':ObjectId(idx)})
    print(result.deleted_count)
    return redirect('/')
    