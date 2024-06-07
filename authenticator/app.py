from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory
from flask_session import Session
import subprocess
import webbrowser
import time
import os
import sqlite3

from sympy import true

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

streamlit_process = None

# Set the static folder to the directory containing your static files
app.static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))

# Path to database file
DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'inventaris.db'))

def validate_credentials(username, password):
    # Connect to the database
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        # Execute SQL query to retrieve user data
        cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
        # Fetch the result
        user = cursor.fetchone()
        # If user exists and password matches, return True
        if user:
            return True
    return False

@app.route('/')
def index():
    # Check if user is logged in, if not, redirect to login page
    if not session.get("logged_in"):
        session["logged_in"] = False
        return redirect(url_for('login'))
    return redirect(url_for('welcome'))

@app.route('/login')
def login(alert="Login to continue", alert_type="alert-primary"):
    if request.args.get('failed'):
        alert = "Try again! Validation failed :("
        alert_type = "alert-danger"
    elif request.args.get('invalid'):
        alert = "You must login to continue :("
        alert_type = "alert-warning"

    if session['logged_in']:
        return redirect(url_for('welcome'))
    return render_template('login.html', alert=alert, alert_type=alert_type)

@app.route('/welcome')
def welcome():
    global streamlit_process
    if session.get("logged_in"):
        if streamlit_process is None or streamlit_process.poll() is not None:
            # Run subprocess for Streamlit
            streamlit_process = subprocess.Popen(["streamlit", "run", "../app/Beranda_🏠_.py"], shell=True)
            # Allow time for Streamlit to start
            time.sleep(2)
            # Open Streamlit URL in browser
            return render_template('welcome.html')
    return redirect(url_for('login', invalid="true"))


@app.route('/validate', methods=['POST'])
def validate():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if session['logged_in'] or validate_credentials(username, password):
        session['logged_in'] = True
        return redirect(url_for('welcome'))
    else:
        return redirect(url_for('login', failed='true'))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

# Add route to serve images from the 'assets' folder
@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug= true, host='0.0.0.0', port=5000)
