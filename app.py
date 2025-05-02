from flask import Flask, render_template,  request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret:key-12'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =db.Column(db.String(100), nullable=False)
    email =db.Column(db.String(120), unique=True, nullable=False)
    password= db.Column(db.String(120), nullable=False)



@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method =='POST':
        email = request.form['email']
        password =request.form['password']
        # Fake check (replace with real DB check if needed)
        if email and password:  # Assuming success
            session['username'] = email.split('@')[0]
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials", 401
        
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username=request.form['username']
        email=request.form['email']
        password=request.form['password']
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return 'User already exists!'

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
