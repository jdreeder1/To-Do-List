from flask import Flask, render_template, session, redirect, url_for, g
from flask import request, jsonify
import simplejson as json
import sys #for printing in console
import math
#Using PostgreSQL
import psycopg2
import project2_model
import project2_admin_model

app = Flask(__name__)
app.secret_key = 'jumpingjacks'
username = ''
admin = ''
user = project2_model.check_users()
administrator = project2_model.check_admin()

#need post route to create a new user/signup (If the email address already exists then the signup should fail)
#need post route to login
#need route for dasboard after succesful login that displays prev todo lists, and the option to create new and edit existing lists
#need route to delete a list
#need separate routes for terms-of-use, privacy, and about

@app.route('/', methods = ['GET', 'POST'])
def home():
    if request.method == 'GET':
        if 'username' in session:
            g.user = session['username']
            return render_template('project2_dashboard.html')
        else:
            return render_template('project2_home.html')
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['email']
        password = request.form['password']

        seed = project2_model.signup(fname, lname, username, password)
        if(seed):
        #POST FORM DATA TO DATABASE - IF USERNAME/EMAIL EXISTS, RETURN ERROR MSG
            message = 'Account successfully created! Welcome, {fname}!'.format(fname = fname)
            session['username'] = username
            return render_template('project2_dashboard.html', message = message, username = username)
        else:
            return render_template('project2_home.html', message = 'Error! User already exists!')

@app.route('/dashboard', methods = ['GET'])
def dashboard():
    if 'username' in session:
        return render_template('project2_dashboard.html')
    else:
        return render_template('project2_login.html', message = 'Please login to access dashboard!')

@app.route('/admin', methods = ['GET'])
def admin():
    if request.method == 'GET':
        if 'admin' in session:
            g.administrator = session['admin']
            return render_template('project2_admin_dashboard.html')
        else:
            return render_template('project2_admin.html')

#A: Total user signups
 #  B: Total signups in the last 24 hours
  # C: Total lists created
   #D: Lists created in the last 24 hours

@app.route('/admin_login', methods = ['POST'])
def admin_login():
    session.pop('admin', None) #if someone else already logged in when post request to this route, kick them out
    areyouuser = request.form['email']
    pwd = project2_model.check_admin_pw(areyouuser)
    if(pwd is None):
        return render_template('project2_admin.html', message = 'Invalid login information!')
    elif request.form['password'] == pwd:
        session['admin'] = request.form['email']
        count_users = project2_admin_model.count_all_users()
        recent_users = project2_admin_model.find_recent_users()
        count_lists = project2_admin_model.count_all_lists()
        recent_lists = project2_admin_model.find_recent_lists()

        return render_template('project2_admin_dashboard.html', message = 'Welcome, admin!', count_users = count_users, recent_users = recent_users, count_lists = count_lists, recent_lists = recent_lists) #refers to function above that's associated with dashboard
    else:
        return render_template('project2_admin.html', message = 'Invalid login information!')

@app.route('/admin/users', methods=['GET'])
def user_metrics():
    if 'admin' in session:
        all_users = project2_admin_model.find_all_users(1)
        num_pgs = math.ceil(project2_admin_model.count_all_users() / 50)

        return render_template('project2_admin_metrics.html', all_users = all_users, num_pgs = num_pgs)
    else:
        return render_template('project2_admin.html', message = 'Please login to access dashboard!')

@app.route('/admin/users/info/', methods=['GET'])
def user_info():
    if 'admin' in session:
        page = request.args.get('page')
        print("{page}".format(page = page), file=sys.stdout)
        all_users = project2_admin_model.find_all_users(page)
        num_pgs = math.ceil(project2_admin_model.count_all_users() / 50)

        return render_template('project2_admin_metrics.html', all_users = all_users, num_pgs = num_pgs)
    else:
        return render_template('project2_admin.html', message = 'Please login to access dashboard!')    

@app.route('/find_recent', methods=['POST'])
def find_users():
    if 'admin' in session:
        users = []
        recent_users = project2_admin_model.find_all_users()
        for i in range(len(recent_users)):
            users.append(recent_users[i])
        #GET CHOSEN LIST FROM DATABASE AND SEND TO CLIENT
        return render_template('project2_admin_dashboard.html', users = users)

@app.route('/delete_user', methods=['POST'])
def delete_user():
    if 'admin' in session:
        email = request.form['email']
        delete_user = project2_admin_model.delete_user(email)
        #delete_user_lists = project2_admin_model.delete_user_lists(email)
        message = '{delete_user} user deleted.'.format(delete_user = delete_user)
        return render_template('project2_admin_metrics.html', message = message, refresh = True)   
    else:
        return render_template('project2_admin.html', message = 'Please login to access dashboard!')     

@app.route('/login', methods = ['GET'])
def login():
    if request.method == 'GET':
        if 'username' in session:
            g.user = session['username']
            return render_template('project2_dashboard.html')
        else:
            return render_template('project2_login.html')

@app.route('/signin', methods = ['POST'])
def login_func():
    session.pop('username', None) #if someone else already logged in when post request to this route, kick them out
    areyouuser = request.form['email']
    pwd = project2_model.check_pw(areyouuser)
    if(pwd is None):
        return render_template('project2_login.html', message = 'Invalid login information!')
    elif request.form['password'] == pwd:
        session['username'] = request.form['email']
        return render_template('project2_dashboard.html') #refers to function above that's associated with dashboard
    else:
        return render_template('project2_login.html', message = 'Invalid login information!')
    #return render_template('index.html')

@app.route('/get_lists', methods = ['POST'])
def get_lists():
     #chosen_list = request.form['chosen_list']
     list_names = []
     tasks = project2_model.read_lists(session['username'])
     for i in range(len(tasks)):
         list_names.append(tasks[i][2])
     #GET CHOSEN LIST FROM DATABASE AND SEND TO CLIENT
     return render_template('project2_dashboard.html', lists = list_names)

@app.route('/pick_list', methods= ['POST'])
def pick_list():
    list_choice = request.form['list_choice']
    tasks = project2_model.find_list(list_choice)
    #parsed = json.loads(tasks)
    #for i in range(len(tasks)):
     #   list_names.append(tasks[i])
    #GET CHOSEN LIST FROM DATABASE AND SEND TO CLIENT
    return render_template('project2_dashboard.html', tasks = tasks)

@app.route('/create_list', methods = ['GET'])
def create_list_tab():
    if request.method == 'GET':
        if 'username' in session:
            return render_template('project2_create_list.html')
        else:
            return render_template('project2_login.html', message = 'Please login to access dashboard!')

@app.route('/new_list', methods = ['POST'])
def new_list():
    #POST TO DATABASE, LIST NAME SHOULD BE PKEY AND ERROR SHOULD BE THROWN IF LIST NAME ALREADY IN DATABASE
    #username = request.form['username']
    list_name = request.form['list_name']
    task = json.dumps({"task": request.form.getlist('task[]')}) #request.form.getlist('task[]')
    seed = project2_model.seed_list(session['username'], list_name, task)
    message = 'New list submitted successfully!'
    return render_template('project2_create_list.html', message = message, username = session['username'])

@app.route('/update_list', methods = ['POST'])
def update_list():
    list_name = request.form['list_name']
    #task = request.form.getlist('task[]')
    j_son = json.dumps({"task": request.form.getlist('task[]')})
    update = project2_model.update_list(session['username'], list_name, j_son)
    message = '{update} list successfully updated!'.format(update = update)

    return render_template('project2_dashboard.html', message = message)

@app.route('/delete_list', methods = ['POST'])
def delete_list():
    list_name = request.form['list_name']
    deleted_count = project2_model.delete_list(session['username'], list_name)
    message = '{count} list successfully deleted!'.format(count = deleted_count)
    return render_template('project2_dashboard.html', message = message)

@app.route('/about', methods = ['GET'])
def about():
    return render_template('project2_about.html')

@app.route('/privacy', methods = ['GET'])
def privacy():
    return render_template('project2_privacy.html')

@app.route('/terms', methods = ['GET'])
def terms():
    return render_template('project2_terms.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000, debug = True)