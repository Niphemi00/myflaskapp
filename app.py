from flask import Flask, render_template, request, redirect
# import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
subscribers = []
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
db = SQLAlchemy(app)

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
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

    # message = f"Welcome {first_name}...we are glad that you've joined the ni-bastience family"
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.starttls()
    # server.login(email, "08162615664josh")
    # server.sendmail("sharnbates@gmail.com", email, message)


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
        newFriend = Friends(name=friend_name)
        try:
            db.session.add(newFriend)
            db.session.commit()
            return redirect('/friends')
        except:
            return 'failed to add'
    else:
        newFriend = Friends.query.order_by(Friends.date_created)
        return render_template('friends.html', newFriend=newFriend)


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    friend_to_update = Friends.query.get_or_404(id)
    if request.method == 'POST':
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/friends')
        except:
            return 'error updating friend details'
    else:
        return render_template('update.html', friend_to_update=friend_to_update)


@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Friends.query.get_or_404(id)
    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/friends')
    except:
        return 'not deleted'


if __name__ == "__main__":
    app.run(debug=True)