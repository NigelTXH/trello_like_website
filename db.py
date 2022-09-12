import sqlite3
"""
For all functions, you can print it to see the error
Example:
    print(db.update_card("user_id","4",1))
"""

def parse(string):
    return '"' + string + '"'

class Database:
    """
    Connects to the database
    """
    def __init__(self) -> None:
        conn = sqlite3.connect('webapp.db', isolation_level=None, check_same_thread = False)
        cursor = conn.cursor()
        self.conn = conn
        self.cursor = cursor
        self.cursor.execute("PRAGMA foreign_keys = ON")


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
    Currently doesn't allow insertion of list_id, user_id, sprint_id with the creation of card
    """
    def create_card(self,card_name,card_tag=None,card_priority=None,card_storypoint=None,card_description=None,card_status=None,card_type=None):
        try:
            self.cursor.execute("insert into card (card_name,card_tag,card_priority,card_storypoint,card_description,card_status,card_type) VALUES (?,?,?,?,?,?,?)",(card_name,card_tag,card_priority,card_storypoint,card_description,card_status,card_type))
        except Exception as e:
            return e

    """
    Updates
    Currently not so code friendly
    Example: 
    appdb.update_card("card_name", "updated_name1",1)
        Change card_name = updated_name1 for card with ID of 1
    """
    def update_card(self ,field, value, card_id) :
        try :
            self.cursor.execute(
                "Update card set "+field+ " = '"+ str(value) +"' where card_id =" + str(card_id))
        except Exception as e :
            return e

    """
    Deletes a card
    Currently only allows deletion based on card_id
    Example: 
    appdb.delete_card(1)
        Delete card with ID of 1
    """
    def delete_card(self , card_id) :
        try :
            self.cursor.execute(
                "Delete from card where card_id = "+ str(card_id))
        except Exception as e :
            return e

    """
    Fetches all cards
    Returns:
        A list of tuples where each tuple is a card
    """
    def all_cards(self ) :
        try :
            self.cursor.execute(
                "SELECT * from CARD")
            return self.cursor.fetchall()
        except Exception as e :
            return e

    """
    Fetches all cards linked to a user
    Returns:
        A list of tuples where each tuple is a card
    """
    def all_usercards(self, user_id) :
        try :
            self.cursor.execute(
                "SELECT * from CARD where user_id = "+ str(user_id))
            return self.cursor.fetchall()
        except Exception as e :
            return e




# db = Database()
# db.clean_db()
