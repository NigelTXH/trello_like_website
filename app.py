import re
from flask import Flask, render_template, url_for, request, redirect
import db
appDb = db.Database()
app = Flask(__name__)

@app.route("/")
def test_page():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if appDb.login_user(request.form.get("email"), request.form.get("password")) is None :
            error = "Invalid credentials"
        else:
            return redirect("/")
    return render_template('login.html', error=error)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        if appDb.create_user(request.form.get("name"), request.form.get("password"), request.form.get("email")) == "Duplicate username or password":
            error = "Duplicate username or password"
        else:
            return redirect("/login")
    return render_template('signup.html', error=error)

@app.route('/create/', methods = ['GET', 'POST'])
def create():
    if request.method == "GET":
        # not sure where to render this page on since i couldnt find html template that contain create 
        return render_template('createpage.html')
    if request.method == "POST":
        card_name = request.form['card_name']
        card_tag = request.form['card_tag']
        card_priority = request.form['card_priority']
        card_storypoint = request.form['card_storypoint']
        card_description = request.form['card_description']
        card_status = request.form['card_status']
        card_type = request.form['card_type']
        list_id = request.form['list_id']
        user_id = request.form['user_id']
        sprint_id = request.form['sprint_id']
        card_start = request.form['card_start']
        card_stop = request.form['card_stop']
        card_elapsed = request.form['card_elapsed']

        
        appDb.create_card(card_name, card_tag, card_priority, card_storypoint, card_description, card_status, card_type, list_id, user_id, sprint_id, card_start, card_stop, card_elapsed)
        return redirect('/')

@app.route("/delete/<int:id>")
def delete(id):
    error = None

    try:
        appDb.delete_card(id)
        return redirect('/')
    
    except:
        error = "There was a problem deleting that task"
    return render_template('index.html', error = error) 

if __name__ == "__main__":
    app.run(debug=True)