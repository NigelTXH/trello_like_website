import sqlite3


def parse(string):
    return '"' + string + '"'

class Database:
    """
    Connects to the database
    """
    def __init__(self) -> None:
        conn = sqlite3.connect('webapp.db', isolation_level=None)
        cursor = conn.cursor()
        self.cursor = cursor
        self.conn = conn

    """
    Removes all records from all tables
    """
    def clean_db(self):
        sql = "DELETE from List; DELETE from card; DELETE from Sprint; DELETE from UserTimer;DELETE from sqlite_sequence;DELETE from UserWorkspace;DELETE from User;DELETE from Workspace"
        self.cursor.executescript(sql)

    """
    Registers a user into the database
    Input:  String              username
            String              password
            (Optional) String     email   
    Output: None
    Example: 
    appdb.register("user1", "ps1")
    appdb.register("user2", "ps2","user@gmail.com")
    """
    def create_user(self,username,password,email=None):
        username = parse(username)
        password = parse(password)
        try:
            if email == None:
                sql = "insert into User ('user_username','user_password') VALUES (" + username + ',' + password +')'
            else:
                email = parse(email)
                sql = "insert into User ('user_username','user_password','user_email') VALUES ("+username+','+password+','+email+')'
            self.cursor.execute(sql)
        except Exception as e:
            return "Duplicate username or password"

    """
    Checks if user is present in database
    Input:  String              username
            String              password
    Output: Boolean
    Example: 
    appdb.register("user1", "ps1")
    appdb.register("user2", "ps2","user@gmail.com")
    """
    def login_user(self,username,password):
        try:
            username = parse(username)
            password = parse(password)
            sql = 'SELECT * FROM USER where (user_username = '+username+'and user_password = '+ password +')'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        if self.cursor.fetchall():
            return True
        else:
            return "Username or password does not match"

    """
    Creates new workspace if workspace name is unique 
    """
    def create_workspace(self,work_name):
        work_name = parse(work_name)
        try:
            sql = "insert into Workspace ('work_name') VALUES (" + work_name +')'
            self.cursor.execute(sql)
        except Exception as e:
            return "Choose a different workspace name"



