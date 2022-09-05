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
        # if request.form.get("email") != "email@email.com" or request.form.get("password") != "password":
        if appDb.login_user(request.form.get("email"), request.form.get("password")) is None :
            error = "Invalid credentials"
        else:
            return redirect("/")
    return render_template('login.html', error=error)

@app.route("/signup")
def signup_page():
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)