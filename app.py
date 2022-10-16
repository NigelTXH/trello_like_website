from flask import Flask, render_template, url_for, request, redirect
from flask_mail import Mail, Message
import db
import datetime
import tkinter as Tkinter
import gc
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
    sprints = appDb.all_sprint()
    if request.method == "POST":
        card_name = request.form.get("taskname")    
        card_tag = request.form.get("tasktag")   
        card_priority = request.form.get("taskpriority")
        card_storypoint = request.form.get("taskstorypoint")
        card_description = request.form.get("taskdescription") 
        card_type = request.form.get("tasktype")
        if  request.form.get("taskassignee") == "":
            card_assignee = None
        else:
             card_assignee = request.form.get("taskassignee")
        try:
            appDb.create_card(card_name, card_tag, card_priority, card_storypoint, card_description, "To do", card_type, None, card_assignee)
            return redirect("/")
        except:
            return "There was an issue addind your task!"
    else:
        tasks = appDb.all_cards()
        return render_template("index.html", tasks=tasks, users=users, sprints=sprints)
    
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
        return render_template('kanban.html', tasks=tasks, id=id, sprint_name=sprint_name, sprints=sprints)

@app.route('/membersboard',methods=['POST','GET'])
def membersboard():
    users = appDb.all_users()
    tasks = appDb.all_cards()
    return render_template("membersboard.html",users=users, tasks=tasks)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    try:
        appDb.delete_user(id)
        return redirect('/membersboard')
    except:
        return 'There was a problem deleting that user'

@app.route('/team_stats',methods=['POST','GET'])
def team_stats():
    users = []
    hours_of_users = [0]
    
    cards = appDb.all_cards()
    for card in cards:
        if (card[11] not in users) and (card[11] != None):
            users.append(card[11])
    
    hours_of_users *= len(users)
    
    for card in cards:
        for user in users:
            if card[11] == user and int(card[14]) != 0:
                hours_of_users[users.index(user)] += int(card[14]) - 662400
    
    return render_template("team_stats.html", labels=users,values=hours_of_users)

@app.route('/timer/<int:id>/<int:sprint>')
def timer(id, sprint):
    if int(appDb.card_timer(id)) == 0:
        counter = int(appDb.card_timer(id)) + 662400
    else:
        counter = int(appDb.card_timer(id))
    running = False
    card = appDb.select_card(id)
    def counter_label(label):
        def count():
            if running:
                nonlocal counter

                # To manage the initial delay.
                if counter==662400:		
                    display="Starting..."
                else:
                    tt = datetime.datetime.fromtimestamp(counter)
                    string = tt.strftime("%H:%M:%S")
                    display=string

                label['text']=display # Or label.config(text=display)

                # label.after(arg1, arg2) delays by
                # first argument given in milliseconds
                # and then calls the function given as second argument.
                # Generally like here we need to call the
                # function in which it is present repeatedly.
                # Delays by 1000ms=1 seconds and call count again.
                label.after(1000, count)
                counter += 1

        # Triggering the start of the counter.
        count()	

    # start function of the stopwatch
    def Start(label):
        nonlocal running
        running=True
        counter_label(label)
        start['state']='disabled'
        stop['state']='normal'
        reset['state']='normal'
        complete['state'] = 'normal'
        appDb.update_card("card_status", "Doing", id)

    # Stop function of the stopwatch
    def Stop():
        nonlocal running
        nonlocal counter
        start['state']='normal'
        stop['state']='disabled'
        reset['state']='normal'
        running = False
        appDb.update_card_timer(id, counter-1)

    # Reset function of the stopwatch
    def Reset(label):
        nonlocal counter
        counter=662400
    
        # If rest is pressed after pressing stop.
        if running==False:	
            reset['state']='disabled'
            label['text']='Welcome!'

        # If reset is pressed while the stopwatch is running.
        else:			
            label['text']='Starting...'
            
    def Complete(label):
        nonlocal running
        nonlocal counter
        start['state']='disabled'
        stop['state']='disabled'
        reset['state']='disabled'
        running = False
        appDb.update_card_timer(id, counter-1)
        date = str(datetime.date.today())
        appDb.update_card_elapsed(id, date)
        appDb.update_card("card_status", "Done", id)


    root = Tkinter.Tk()
    root.title(f"{card[1]}")

    # Fixing the window size.
    root.minsize(width=250, height=70)
    label = Tkinter.Label(root, text=f"{card[1]}", fg="black", font="Verdana 30 bold")
    label.pack()
    f = Tkinter.Frame(root)
    start = Tkinter.Button(f, text='Start', width=6, command=lambda:Start(label))
    stop = Tkinter.Button(f, text='Stop',width=6,state='disabled', command=Stop)
    reset = Tkinter.Button(f, text='Reset',width=6, state='disabled', command=lambda:Reset(label))
    complete = Tkinter.Button(f, text='Complete',width=7, state='disabled', command=lambda:Complete(label))
    f.pack(anchor = 'center',pady=5)
    start.pack(side="left")
    stop.pack(side ="left")
    reset.pack(side="left")
    complete.pack(side="left")
    root.mainloop()
    gc.collect()
    return redirect(f"/kanban/{sprint}")
@app.route("/graph/<int:id>")
def graph(id):
    counter = 0
    counter2 = 0
    get_cards = appDb.all_cards()
    for cards in get_cards:
        if int(cards[12]) == id:
            counter += 1
            counter2 += int(cards[4])

    get_sprint = appDb.all_sprint()
    for sprint in get_sprint:
        if sprint[0] == id:
            sprint_start = datetime.datetime.strptime(sprint[2], "%Y-%m-%d")
            sprint_end = datetime.datetime.strptime(sprint[3], "%Y-%m-%d")
            break

    diff = sprint_end - sprint_start

    data1 = [(cards[9],counter2) for cards in get_cards if int(cards[12]) == id]
    data2 = []


    for i in range(len(data1)):
        completed_story_point = 0
        for cards in get_cards:
            if (cards[6] == "Done") and (cards[12] == id) and (datetime.datetime.strptime(cards[9], "%Y-%m-%d") < sprint_start):
                completed_story_point += int(cards[4])
        add = (str(sprint_start.date()), data1[i][1] - completed_story_point)
        sprint_start+=(diff/(counter-1))
        completed_story_point = 0
        data2.append(add)

    labels = [row[0] for row in data2]
    values = [row[1] for row in data2]

    v = (str(sprint_end.date()))
    return render_template("graph.html", labels=labels, values=values, counter2 = counter2, v = v)

if __name__ == "__main__":
    app.run(debug=True)
    #appDb.clean_db()
