from flask import Flask, render_template, redirect, url_for, request, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Simulated data storage
announcements = [
    {"id": 1, "content": "Company picnic this Saturday!"},
    {"id": 2, "content": "Reminder: Q3 reports are due next week."},
]

# Simulated user accounts
users = {
    "employee": {"username": "employee", "password": "employee123", "role": "employee"},
    "customer": {"username": "customer", "password": "customer123", "role": "customer"},
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.get(username)
        if user and user['password'] == password:
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('home'))

@app.route('/announcements')
def view_announcements():
    return render_template('announcements.html', announcements=announcements)

@app.route('/calendar')
def view_calendar():
    return render_template('calendar.html')

@app.route('/references')
def view_references():
    return render_template('references.html')

if __name__ == '__main__':
    app.run(debug=True)
