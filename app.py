from flask import Flask, render_template, request

app = Flask(__name__)
subscribers = []
@app.route('/')
def index():
    return render_template('base.html')


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
    if not first_name or not last_name or not email:
        error_message = 'Every field needs to be filled properly'
        subscribers.append(f'{first_name} {last_name}, {email}')
        return render_template('failsafe.html', error=error_message,first_name=first_name,
                               last_name=last_name, email=email )
    else:
        subscribers.append(f'{first_name} {last_name}, {email}')
        return render_template('form.html',subscribers=subscribers)


if __name__ == "__main__":
    app.run(debug=True)