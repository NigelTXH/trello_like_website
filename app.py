from flask import Flask, render_template, url_for, request, redirect
import db
appDb = db.Database()
app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def product_backlog():
    users = appDb.all_users()
    if request.method == "POST":
        card_name = request.form.get("taskname")    
        card_tag = request.form.get("tasktag")   
        card_priority = request.form.get("taskpriority")
        card_storypoint = request.form.get("taskstorypoint")
        card_description = request.form.get("taskdescription") 
        card_status = request.form.get("taskstatus")
        card_type = request.form.get("tasktype")
        if  request.form.get("taskassignee") == "":
            card_assignee = None
        else:
             card_assignee = request.form.get("taskassignee")
        try:
            appDb.create_card(card_name, card_tag, card_priority, card_storypoint, card_description, card_status, card_type, None, card_assignee)
            return redirect("/")
        except:
            return "There was an issue addind your task!"
    else:
        tasks = appDb.all_cards()
        return render_template("index.html", tasks=tasks, users=users)

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

@app.route('/delete/<int:id>')
def delete(id):
    try:
        appDb.delete_card(id)
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

if __name__ == "__main__":
    app.run(debug=True)