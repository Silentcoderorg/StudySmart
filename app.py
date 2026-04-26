from flask import Flask, render_template, request, redirect, flash, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__, template_folder='templates')
app.secret_key = '1234'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///study.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------- MODELS --------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    progress_logs = db.relationship('ProgressLog', backref='log_author', lazy=True)


class ProgressLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    status = db.Column(db.String(20), default='In Progress')
    priority = db.Column(db.String(20), default='Medium')

    start_date = db.Column(db.Date)
    due_date = db.Column(db.Date)

    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# -------------------- ROUTES --------------------
from datetime import datetime  

@app.route('/add_log', methods=['POST'])
def add_log():
    if 'user_id' not in session:
        return redirect(url_for('login'))

   
    title = request.form['title']
    description = request.form.get('description')
    status = request.form.get('status')
    priority = request.form.get('priority')

    start_date_raw = request.form.get('start_date')
    due_date_raw = request.form.get('due_date')

   
    start_date = datetime.strptime(start_date_raw, '%Y-%m-%d').date() if start_date_raw else None
    due_date = datetime.strptime(due_date_raw, '%Y-%m-%d').date() if due_date_raw else None

    new_log = ProgressLog(
        title=title,
        description=description,
        status=status,
        priority=priority,
        start_date=start_date,
        due_date=due_date,
        user_id=session['user_id']
    )

    db.session.add(new_log)
    db.session.commit()

    return redirect(url_for('progress_log'))

@app.route('/delete_log/<int:id>')
def delete_log(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    log = ProgressLog.query.get_or_404(id)

    if log.user_id != session['user_id']:
        abort(403)

    db.session.delete(log)
    db.session.commit()

    return redirect(url_for('progress_log'))


@app.route('/')
def home():
    return render_template('index.html')


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('progress_log'))

        flash("Invalid login details", "error")

    return render_template('login.html')


# SIGNUP
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "error")
            return redirect(url_for('signup'))

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

from datetime import date

@app.route('/progress_log')
def progress_log():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    logs = ProgressLog.query.filter_by(user_id=user_id).all()

    total_count = len(logs)
    completed_count = len([log for log in logs if log.status == 'Completed'])

    return render_template(
        "progress_log.html",
        logs=logs,
        total_count=total_count,
        completed_count=completed_count,
        today=date.today()
    )



@app.route('/complete_log/<int:id>')
def complete_log(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    log = ProgressLog.query.get_or_404(id)

    if log.user_id != session['user_id']:
        abort(403)

    log.status = 'Completed'
    db.session.commit()

    flash("Task completed!", "success")
    return redirect(url_for('progress_log'))


# -------------------- RUN --------------------

if __name__ == "__main__":
   with app.app_context():
        print

        db.drop_all()   
        db.create_all()  

        print

app.run(debug=True)

        
        
