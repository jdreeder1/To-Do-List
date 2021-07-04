from flask import Flask, render_template, request, session, redirect, url_for, g
import model

#G is the global variable for Flask

app = Flask(__name__)
app.secret_key = 'jumpingjacks'
username = ''
user = model.check_users()

@app.route('/', methods = ['GET', 'POST'])
def home():
    if 'username' in session:
        g.user = session['username']
        return render_template('about.html')
    else:
        return render_template('homepage.html')

    #if request.method == 'GET':
     #   return render_template('index.html')
    #else:
     #   username = request.form['username']
      #  password = request.form['password']
       # db_password = model.check_pw(username)
#
 #       if password == db_password:
  #          message = model.show_color(username)
   #         return render_template('about.html', message = message)
    #    else:
     #       return render_template('index.html', message = 'Invalid login!')"""

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('username', None) #if someone else already logged in when post request to this route, kick them out
        areyouuser = request.form['username']
        pwd = model.check_pw(areyouuser)
        if request.form['password'] == pwd:
            session['username'] = request.form['username']
            return redirect(url_for('about')) #refers to home function above that's associated with homepage
        else:
            return render_template('index.html', message = 'Invalid login information!')
    return render_template('index.html')

@app.route('/about', methods = ['GET'])
def about():
    return render_template('about.html', pic = '../static/images/avatar2.png')

@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        username = request.form['username']
        password = request.form['password']
        color = request.form['color']
        message = model.signup(username, password, color)

        return render_template('signup.html', message = message)

@app.route('/get_session')
def get_session():
    if 'username' in session:
        return session['username']
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 7000, debug = True)