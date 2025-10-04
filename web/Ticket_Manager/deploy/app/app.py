from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "adsolIASDhna873124FSG__SFG__ADS_F__ASDR234324dsrfPKLMMCNasddERTasSSSSSWVT"

flag_dict = {"flag":"nnctf{no_c0rras_t4nt0_am1g0!}"}


# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketmanager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


class TextEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


def get_text(entry_id, user_id):
    entry = TextEntry.query.filter_by(id=entry_id, user_id=user_id).first()
    db.session.refresh(entry)
    return entry

# Create database tables
with app.app_context():
    db.create_all()


# Login page
@app.route('/', methods=['GET'])
def login():
    return render_template('auth.html')


# Combined login/register page
@app.route('/auth', methods=['POST'])
def auth():
    action = request.form.get('action')
    username = request.form.get('username')
    password = request.form.get('password')

    if action == 'register':
        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "error")
        else:
            new_user = User(username=username, password_hash=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! You can now log in.", "success")
    elif action == 'login':
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['username'] = username
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", "error")

    return render_template('auth.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        flash("You need to login first!", "error")
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'upload':
            text = request.form.get('text')
            if text:
                entry = TextEntry(content=text, user_id=user_id)
                db.session.add(entry)
                db.session.commit()
                flash("Text uploaded!", "success")

        elif action.startswith('delete_'):
            entry_id = int(action.split('_')[1])
            entry = TextEntry.query.filter_by(id=entry_id, user_id=user_id).first()
            if entry:
                db.session.delete(entry)
                db.session.commit()
                flash("Text deleted!", "success")

        elif action.startswith('modify_'):
            entry_id = int(action.split('_')[1])
            new_content = request.form.get(f'new_text_{entry_id}')
            entry = TextEntry.query.filter_by(id=entry_id, user_id=user_id).first()
            if entry and new_content:
                entry.content = new_content
                db.session.commit()
                flash("Text modified!", "success")

    texts = TextEntry.query.filter_by(user_id=user_id).all()
    return render_template('home.html', texts=texts, username=session['username'])


@app.route('/flag', methods=['GET'])
def flag():
    if 'username' not in session:
        flash("You need to login first!", "error")
        return redirect(url_for('login'))

    user_id = session['user_id']
    entry_id = int(request.args.get("id"))
    entry = get_text(entry_id, user_id)
    if entry:
        if "flag" not in entry.content:
            return flag_dict.get(get_text(entry_id, user_id).content, "Key not found")
        else:
            return "You are not allowed to retrieve the flag"
    else:
        return "Invalid entry"


# Logout
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    flash("Logged out!", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=False)