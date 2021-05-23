from flask import Flask, render_template, session, redirect, url_for, g
from flask import request, jsonify
import simplejson as json
#Using PostgreSQL
import psycopg2
import project1_model

app = Flask(__name__)
app.secret_key = 'jumpingjacks'
username = ''
user = project1_model.check_users()

#need post route to create a new user/signup (If the email address already exists then the signup should fail)
#need post route to login
#need route for dasboard after succesful login that displays prev todo lists, and the option to create new and edit existing lists
#need route to delete a list
#need separate routes for terms-of-use, privacy, and about

#FIX CREATE ACCOUNT LOGIN!! SHOULDN'T NEED TO LOGIN RIGHT AFTER CREATING ACCOUNT BEFORE ACCESSING THE DASHBOARD!!
@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'GET':
        if 'username' in session:
            g.user = session['username']
            return render_template('project1_dashboard.html')
        else:
            return render_template('project1_home.html')
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['email']
        password = request.form['password']

        seed = project1_model.signup(fname, lname, username, password)
        if(seed):
        #POST FORM DATA TO DATABASE - IF USERNAME/EMAIL EXISTS, RETURN ERROR MSG
            message = 'Account successfully created! Welcome, {fname}!'.format(fname = fname)
            session['username'] = username
            return render_template('project1_dashboard.html', message = message, username = username)
        else:
            return render_template('project1_home.html', message = 'Error! User already exists!')

@app.route('/dashboard', methods = ['GET'])
def dashboard():
    if 'username' in session:
        return render_template('project1_dashboard.html')
    else:
        return render_template('project1_login.html', message = 'Please login to access dashboard!')

@app.route('/login', methods = ['GET'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            g.user = session['username']
            return render_template('project1_dashboard.html.html')
        else:
            return render_template('project1_login.html')

@app.route('/signin', methods = ['POST'])
def login_func():
    session.pop('username', None) #if someone else already logged in when post request to this route, kick them out
    areyouuser = request.form['email']
    pwd = project1_model.check_pw(areyouuser)
    if(pwd is None):
        return render_template('project1_login.html', message = 'Invalid login information!')
    elif request.form['password'] == pwd:
        session['username'] = request.form['email']
        return render_template('project1_dashboard.html') #refers to function above that's associated with dashboard
    else:
        return render_template('project1_login.html', message = 'Invalid login information!')
    #return render_template('index.html')

@app.route('/get_lists', methods = ['POST'])
def get_lists():
     #chosen_list = request.form['chosen_list']
     list_names = []
     tasks = project1_model.read_lists(session['username'])
     for i in range(len(tasks)):
         list_names.append(tasks[i][2])
     #GET CHOSEN LIST FROM DATABASE AND SEND TO CLIENT
     return render_template('project1_dashboard.html', lists = list_names)

@app.route('/pick_list', methods= ['POST'])
def pick_list():
    list_choice = request.form['list_choice']
    tasks = project1_model.find_list(list_choice)
    #parsed = json.loads(tasks)
    #for i in range(len(tasks)):
     #   list_names.append(tasks[i])
    #GET CHOSEN LIST FROM DATABASE AND SEND TO CLIENT
    return render_template('project1_dashboard.html', tasks = tasks)

@app.route('/create_list', methods = ['GET'])
def create_list_tab():
    if request.method == 'GET':
        if 'username' in session:
            return render_template('project1_create_list.html')
        else:
            return render_template('project1_login.html', message = 'Please login to access dashboard!')

@app.route('/new_list', methods = ['POST'])
def new_list():
    #POST TO DATABASE, LIST NAME SHOULD BE PKEY AND ERROR SHOULD BE THROWN IF LIST NAME ALREADY IN DATABASE
    #username = request.form['username']
    list_name = request.form['list_name']
    task = json.dumps({"task": request.form.getlist('task[]')}) #request.form.getlist('task[]')
    seed = project1_model.seed_list(session['username'], list_name, task)
    message = 'New list submitted successfully!'
    return render_template('project1_create_list.html', message = message, username = session['username'])

@app.route('/update_list', methods = ['POST'])
def update_list():
    list_name = request.form['list_name']
    #task = request.form.getlist('task[]')
    j_son = json.dumps({"task": request.form.getlist('task[]')})
    update = project1_model.update_list(session['username'], list_name, j_son)
    message = '{update} list successfully updated!'.format(update = update)

    return render_template('project1_dashboard.html', message = message)

@app.route('/delete_list', methods = ['POST'])
def delete_list():
    list_name = request.form['list_name']
    deleted_count = project1_model.delete_list(session['username'], list_name)
    message = '{count} list successfully deleted!'.format(count = deleted_count)
    return render_template('project1_dashboard.html', message = message)

@app.route('/about', methods = ['GET'])
def about():
    return render_template('project1_about.html')

@app.route('/privacy', methods = ['GET'])
def privacy():
    return render_template('project1_privacy.html')

@app.route('/terms', methods = ['GET'])
def terms():
    return render_template('project1_terms.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port = 5000, debug = True)