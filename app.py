from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def resume():
    return render_template('resume.html', title="Resume")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Contacts")

if __name__ == '__main__':
    app.run(debug=True)