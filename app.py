from flask import Flask, render_template, url_for, request, redirect
from flask_mail import Mail, Message
import db
import datetime
appDb = db.Database()
app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mytestfunct@gmail.com'
app.config['MAIL_PASSWORD'] = 'fyokeubxxuekydyn'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'mytestfunct@gmail.com'
mail = Mail(app)

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
    
@app.route("/sprint-board", methods=['POST', 'GET'])
def sprint_board():
    error = None
    users = appDb.all_users()
    task_sprint = appDb.all_sprint()
    if request.method == "POST":
        card_name = request.form.get("taskname")    
        card_start_date = request.form.get("start_date")
        card_end_date = request.form.get("end_date")
        card_start_date_split = card_start_date.split("-")
        card_end_date_split = card_end_date.split("-")
        
        card_start_year = int(card_start_date_split[0])
        card_start_month = int(card_start_date_split[1])
        card_start_day = int(card_start_date_split[2])
        
        card_end_year = int(card_end_date_split[0])
        card_end_month = int(card_end_date_split[1])
        card_end_day = int(card_end_date_split[2])
        
        if card_start_year > card_end_year:
            error = "Start year more than end year"
        elif card_start_month > card_end_month and card_start_year == card_end_year:
            error = "Start month more than end month"
        elif card_start_day > card_end_day and card_start_month == card_end_month:
            error = "Start day more than end day"
        else: 
            try:
                appDb.create_sprint(card_name, sprint_start=card_start_date, sprint_end=card_end_date)
                return redirect("/sprint-board")
            except:
                return "There was an issue addind your task!"
    else:
        task_sprint = appDb.all_sprint()
    length = len(task_sprint)
    list_of_days = []
    for sprint in task_sprint:
        
        # get the start date and make it a date time object
        card_start = sprint[2].split("-")
        card_start_year = int(card_start[0])
        card_start_month = int(card_start[1])
        card_start_day = int(card_start[2])
        card_start = datetime.datetime(card_start_year, card_start_month, card_start_day)
        
        # get the end date and make it a date time object
        card_end = sprint[3].split("-")
        card_end_year = int(card_end[0])
        card_end_month = int(card_end[1])
        card_end_day = int(card_end[2])
        card_end = datetime.datetime(card_end_year, card_end_month, card_end_day)
        
        # check and return the corresponding number of days
        today = datetime.date.today()
        today_with_time = datetime.datetime(year=today.year, month=today.month, day=today.day)
        if card_start > today_with_time:
            list_of_days.append("Not started")
        else:
            days_left = (card_end - today_with_time).days
            if days_left <= 0:
                list_of_days.append("Done")
            else:
                list_of_days.append(f"Days Remaining: {days_left}")
    return render_template("sprint-board.html",task_sprint=task_sprint,users=users, error = error, list_of_days=list_of_days, length=length)

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
    
@app.route('/delete_sprint/<int:id>')
def delete_sprint(id):
    try:
        print(id)
        appDb.delete_sprint(id)
        return redirect('/sprint-board')
    except:
        return 'There was a problem deleting that task'
    
@app.route('/remove/<int:id>/<int:sprint_id>')
def remove(id, sprint_id):
    try:
        appDb.update_card("sprint_id", None , id)
        return redirect(f"/kanban/{sprint_id}")
    except:
        return 'There was a problem removing that task'

@app.route("/forgotpassword", methods=['GET', 'POST'])
def forgot_password():
    error = None
    if request.method == 'POST':
        if not appDb.check_email(request.form.get("email")):
            error = "Invalid email"
        else:
            msg = Message('Scrum King Password', sender = 'mytestfunct@gmail.com', recipients = [request.form.get("email")])
            msg.body = "Your password is: "+appDb.fetch_password(request.form.get("email"))+""        
            mail.send(msg)
            return redirect("/login")
    return render_template('forgotpassword.html', error=error)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_task(id):
    users = appDb.all_users()
    details = appDb.select_card(id)
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
            appDb.update_card("card_name", card_name, id)
            appDb.update_card("card_tag", card_tag, id)
            appDb.update_card("card_type", card_type, id)
            appDb.update_card("card_priority", card_priority, id)
            appDb.update_card("card_storypoint", card_storypoint, id)
            appDb.update_card("card_description", card_description, id)
            appDb.update_card("card_status", card_status, id)
            appDb.update_card("user_username", card_assignee, id)
            return redirect("/")
        except:
            return "There was an issue adding your task!"
    else:
        return render_template("update.html", details=details, users=users)

@app.route('/kanban/<int:id>', methods=['GET', 'POST'])
def kanban(id):
    sprints = appDb.all_sprint()
    for sprint in sprints:
        if sprint[0] == id:
            sprint_name = sprint[1]
    tasks = appDb.all_cards()
    if request.method == "POST":
        task_id = request.form.get("add_task")
        appDb.update_card("sprint_id", id, task_id)
        return redirect(f"/kanban/{id}")
    else:
        return render_template('kanban.html', tasks=tasks, id=id, sprint_name=sprint_name)

@app.route('/membersboard',methods=['POST','GET'])
def membersboard():
    users = appDb.all_users()
    return render_template("membersboard.html",users=users)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    try:
        appDb.delete_user(id)
        return redirect('/membersboard')
    except:
        return 'There was a problem deleting that user'



if __name__ == "__main__":
    app.run(debug=True)
    #appDb.clean_db()
