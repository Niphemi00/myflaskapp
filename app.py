from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    title="Index Page"
    return render_template('base.html', title=title)


@app.route('/about')
def about():
    title= "About Page"
    names = ['Liam', 'ThankGod', 'Noel', 'Joshua']
    return render_template('about.html', names=names, title=title)


if __name__ == "__main__":
    app.run(debug=True)