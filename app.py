from flask import Flask, render_template, request, redirect, url_for
import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
subscribers = []
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
db = SQLAlchemy(app)

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())


    def __repr__(self):
        return f'{self.id}: {self.name} is {self.age} years old'


@app.route('/')
def index():
    first_name = request.form.get('first_name')
    return render_template('base.html', first_name=first_name)


@app.route('/about')
def about():
    names = ['Liam', 'ThankGod', 'Noel', 'Joshua']
    return render_template('about.html', names=names)


@app.route('/subscribe')
def subscribe():
    return render_template('subscribe.html')

@app.route('/form', methods=['POST'])
def forms():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    message = f"Welcome {first_name}...we are glad that you've joined the ni-bastience family"
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("input your email", "input your password")
    server.sendmail("sharnbates@gmail.com", email, message)


    if not first_name or not last_name or not email:
        error_message = 'Warning!!!...Every field needs to be filled properly'
        subscribers.append(f'{first_name} {last_name}, {email}')
        return render_template('subscribe.html', error=error_message,first_name=first_name,
                               last_name=last_name, email=email )
    else:
        subscribers.append(f'{first_name} {last_name}, {email}')
        return render_template('form.html', first_name=first_name,subscribers=subscribers)


@app.route('/friends', methods=['POST', 'GET'])
def friends():
    if request.method == 'POST':
        friend_name = request.form['name']
        gender = request.form['gender']
        new_friends = Friends(name=friend_name, gender=gender)
        try:
            db.session.add(new_friends)
            db.session.commit()
            return redirect('/friends')
        except:
            return 'There was an error'
    else:
        friends = Friends.query.order_by(Friends.date_created)
        return render_template('friends.html', friends=friends)

if __name__ == "__main__":
    app.run(debug=True)