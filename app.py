from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'

DATA_FILE = 'data.json'
ADMIN_EMAIL = 'bhs@mf-gym.dk'
ADMIN_PASSWORD = 'BHSeks25'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('upload'))
        else:
            return redirect(url_for('access'))
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not session.get('admin'):
        return redirect(url_for('login'))
    data = load_data()
    if request.method == 'POST':
        code = request.form['code']
        link = request.form['link']
        data[code] = link
        save_data(data)
        flash('Link uploaded successfully!')
    return render_template('upload.html', data=data)

@app.route('/delete/<code>')
def delete(code):
    if not session.get('admin'):
        return redirect(url_for('login'))
    data = load_data()
    if code in data:
        del data[code]
        save_data(data)
    return redirect(url_for('upload'))

@app.route('/access', methods=['GET', 'POST'])
def access():
    link = None
    if request.method == 'POST':
        email = request.form['email']
        code = request.form['code']
        if email == ADMIN_EMAIL:
            data = load_data()
            link = data.get(code)
            if not link:
                flash('No file found for this code.')
    return render_template('download.html', link=link)

if __name__ == '__main__':
    app.run(debug=True)
