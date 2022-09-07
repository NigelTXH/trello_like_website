import sqlite3


def parse(string):
    return '"' + string + '"'

class Database:
    """
    Connects to the database
    """
    def __init__(self) -> None:
        conn = sqlite3.connect('webapp.db', isolation_level=None, check_same_thread = False)
        cursor = conn.cursor()
        self.cursor = cursor
        self.conn = conn

    """
    Removes all records from all tables
    """
    def clean_db(self):
        sql = "DELETE from List; DELETE from card; DELETE from Sprint; DELETE from UserTimer;DELETE from sqlite_sequence;DELETE from UserWorkspace;DELETE from User;DELETE from Workspace;DELETE from sqlite_sequence"
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

        try:
            self.cursor.execute("insert into User (user_username,user_password,user_email) VALUES (?,?,?)",(username,password,email))
        except Exception as e:
            print(e)
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
    def login_user(self,email,password):
        try:
            email = parse(email)
            password = parse(password)
            sql = 'SELECT * FROM USER where (user_email = '+email+'and user_password = '+ password +')'
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        if self.cursor.fetchall():
            return self.cursor.fetchall()
        else:
            return None

    """
    Creates new workspace if workspace name is unique 
    """
    def create_workspace(self,work_name):
        work_name = parse(work_name)
        try:
            sql = "insert into Workspace ('work_name') VALUES (" + work_name +')'
            self.cursor.execute(sql)
        except Exception as e:
            return e

    """
    Creates new task card
    The only compulsory field is card_name, rest defaults to Null if left blank
    
    """
    def create_card(self,card_name,card_tag=None,card_priority=None,card_storypoint=None,card_description=None,card_status=None):
        try:
            self.cursor.execute("insert into card (card_name,card_tag,card_priority,card_storypoint,card_description,card_status) VALUES (?,?,?,?,?,?)",(card_name,card_tag,card_priority,card_storypoint,card_description,card_status))
        except Exception as e:
            return e






# db = Database()
# db.clean_db()