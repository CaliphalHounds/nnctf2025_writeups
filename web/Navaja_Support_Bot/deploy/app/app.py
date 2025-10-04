from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from urllib.parse import urlparse
from datetime import datetime

from user_sim import UserSimulator

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
FLAG = os.environ.get("FLAG")


# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketmanager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)


class SupportMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

# Create database tables
with app.app_context():
    db.create_all()

    # Create Admin user if it doesn't exist
    admin_user = User.query.filter_by(username="admin").first()
    if not admin_user:
        admin_user = User(
            username="admin",
            password_hash=generate_password_hash(os.environ.get("ADMIN_PASS"))
        )
        db.session.add(admin_user)
        db.session.commit()

    # Create a message with flag if it doesn't exist
    flag_msg = SupportMessage.query.filter_by(user_id=admin_user.id).first()
    if not flag_msg:
        flag_msg = SupportMessage(user_id=admin_user.id, message=FLAG)
        db.session.add(flag_msg)
        db.session.commit()


userSim = UserSimulator()

@app.after_request
def set_csp(response):
    csp = (
        "default-src 'self'; "
        "script-src 'self' cdn.jsdelivr.net; "
        "img-src 'self' ;"
        "style-src 'self' 'unsafe-inline'; "
        "style-src-elem 'self' 'unsafe-inline'; "
        "style-src-attr 'self' 'unsafe-inline';"
    )
    response.headers['Content-Security-Policy'] = csp
    return response


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
            return redirect(url_for('support'))
        else:
            flash("Invalid username or password", "error")

    return render_template('auth.html')


@app.route('/support', methods=['GET'])
def support():
    if 'username' not in session:
        flash("You need to login first!", "error")
        return redirect(url_for('login'))

    id = request.args.get("id")
    if id and session["username"] == "admin" and User.query.filter_by(id=id).first():
        return render_template('support.html', username=User.query.filter_by(id=id).first().username)

    return render_template('support.html', username=session["username"])


@app.route('/messages', methods=['GET'])
def get_messages():
    if 'username' not in session:
        return {"error": "Access denied"}, 403

    if request.args.get("id") and session["username"] == "admin":
        messages = SupportMessage.query.filter_by(user_id=request.args.get("id")).all()
    else:
        messages = SupportMessage.query.filter_by(user_id=session["user_id"]).all()
    return {
        "messages": [
            {"id": m.id, "message": m.message} for m in messages
        ]
    }

# Admin Visit
@app.route('/visit', methods=['POST'])
def visit():
    if 'username' not in session or "user_id" not in session:
        return {"error": "Access denied"}, 403


    userSim.init()
    userSim.visit_url(session["user_id"])

    return "Visiting..."



@app.route("/create_msg", methods=["POST"])
def create_msg():
    if 'user_id' not in session:
        return jsonify({"error": "You must be logged in"}), 403

    data = request.get_json()
    message_text = data.get("message", "").strip()

    if not message_text:
        return jsonify({"error": "Message cannot be empty"}), 400

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Invalid user"}), 400




    new_msg = SupportMessage(message=message_text, user_id=user.id)
    db.session.add(new_msg)
    db.session.commit()

    return jsonify({
        "id": new_msg.id,
        "message": new_msg.message,
        "user": user.username,
        "timestamp": new_msg.timestamp.isoformat()
    })


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    next = request.args.get("next")
    if next:
        def is_absolute_url(url):
            parsed = urlparse(url)
            return bool(parsed.scheme) and bool(parsed.netloc)

        if is_absolute_url(next):
            return redirect(next)

    session.pop('username', None)
    session.pop('user_id', None)
    flash("Logged out!", "info")

    return redirect(url_for('login'))




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=False)
