from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import os
from datetime import datetime

app = Flask(__name__)
# CHANGE this to a secure secret in production (or load from env var)
app.secret_key = 'change_this_to_a_random_secret'

DATA_FILE = 'messages.csv'


def ensure_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'name', 'email', 'subject', 'message'])


@app.route('/')
def index():
    return render_template('index.html', datetime=datetime)
    # return render_template('index.html', current_year=datetime.utcnow().year)



@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name', '').strip()
    email = request.form.get('email', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not email or not message:
        flash('Please fill in name, email and message.')
        return redirect(url_for('index') + '#contact')

    ensure_data_file()
    with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.utcnow().isoformat(), name, email, subject, message])
        

    return render_template('thanks.html', name=name, datetime=datetime)


if __name__ == '__main__':
    ensure_data_file()
    # Debug True is fine while developing; turn off for production
    app.run(debug=True)