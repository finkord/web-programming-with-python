from flask import Flask, render_template
from . import app

@app.route('/')
def resume():
    return render_template('resume.html', title="Resume")

@app.route('/contacts')
def contacts():
    return render_template('contacts.html', title="Contacts")