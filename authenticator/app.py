import os
import json
from flask import Flask, render_template, redirect, url_for, request, session, send_from_directory
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set the static folder to the directory containing your static files
app.static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets'))

# Path to user data JSON file
USER_DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'user_data.json'))

def load_credentials_from_json():
    # Load user data from JSON file
    if os.path.exists(USER_DATA_PATH):
        with open(USER_DATA_PATH, 'r') as f:
            return json.load(f)
    else:
        # Return an empty dictionary if file doesn't exist
        return {}

def save_credentials_to_json(credentials):
    # Save credentials to JSON file
    with open(USER_DATA_PATH, 'w') as f:
        json.dump(credentials, f)

def validate_credentials(username, password):
    # Load user data
    user_data = load_credentials_from_json()

    # Check if username exists and password matches
    if username in user_data:
        if user_data[username]["password"] == password:
            return True

    return False

@app.route('/')
def index():
    # Cek apakah user sudah login, jika belum redirect ke halaman login
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
    if session.get('logged_in'):
        return render_template('welcome.html')
    else:
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

# Tambahkan rute untuk mengambil gambar dari folder 'assets'
@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
