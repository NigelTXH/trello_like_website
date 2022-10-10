import sqlite3
"""
For all functions, you can print it to see the error
Example:
    print(db.update_card("user_id","4",1))
"""

def parse(string):
    return '"' + str(string) + '"'

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

    Universal update
    This command helps you build a query to execute a specific update if needed
    You will need information on what the table is called, what the column is called, etc,. This information
    can be found in docs

    Example:
        I want to update the email of the user whose username is "Nathan" to new@gmail.com
            update("user","user_email","new@gmail.com","user_username","Nathan")
    """

    def update(self , db , field , value , row , row_cond) :
        try :
            print("Update " + db + " set " + field + " = '" + str(value) + "' where " + row + " = " + str(row_cond))
            self.cursor.execute(
                "Update " + parse(db) + " set " + field + " = '" + str(value) + "' where " + row + " = " + parse(
                    row_cond))
        except Exception as e :
            return e

    """

    Universal select
    This command helps you build a query to execute a specific select if needed
    You will need information on what the table is called, what the column is called, etc,. This information
    can be found in docs

    Example:
        I want to update the email of the user whose username is "Nathan" to new@gmail.com
            update("user","user_email","new@gmail.com","user_username","Nathan")
    """

    def select(self , db) :
        try :
            self.cursor.execute(
                "Select * from " + db)
            return self.cursor.fetchall( )
        except Exception as e :
            return e

    """
    Removes all records from all tables
    """
    def clean_db(self):
        sql = "Delete from card_time;Delete from card;Delete from Sprint;Delete from User;DELETE from sqlite_sequence"
        self.cursor.executescript(sql)

    """
    #######################################################################################################################
    User
    #######################################################################################################################
    """

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
    Fetches all users 
    Returns:
        A list of tuples where each tuple is a user
    """
    def all_users(self) :
        try :
            self.cursor.execute(
                "SELECT * from user")
            return self.cursor.fetchall()
        except Exception as e :
            return e

    """
    Delete a user based on id
    """
    def delete_user(self, id) :
        try :
            self.cursor.execute(
                "Delete from User where user_id = " + parse(id))
        except Exception as e :
            return e

    """
    Fetches password of a user with email
    Returns:
        A string 
    """
    def fetch_password(self , user_email) :
        try :
            self.cursor.execute("SELECT user_password from user where user_email = " + parse(user_email))
            return self.cursor.fetchall( )[0][0]
        except Exception as e :
            return e

    """
        checks if user email is valid
        Returns:
        A tuple with information of a user
    """
    def check_email(self , user_email) :
        try :
            self.cursor.execute(
                "SELECT * from user where user_email = " + parse(user_email))
            return self.cursor.fetchall( ) != []
        except Exception as e :
            return e

    """
    #######################################################################################################################
    Workspace
    #######################################################################################################################
    """

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
    #######################################################################################################################
    Task
    #######################################################################################################################
    """

    """
    Creates new task card
    The only compulsory field is card_name, rest defaults to Null if left blank
    Currently doesn't allow insertion of list_id, user_id, sprint_id with the creation of card
    """
    def create_card(self,card_name,card_tag=None,card_priority=None,card_storypoint=None,card_description=None,card_status=None,card_type=None,list_id=None,user_name=None,sprint_id=None):
        try:
            self.cursor.execute("insert into card (card_name,card_tag,card_priority,card_storypoint,card_description,card_status,card_type,list_id,user_username,sprint_id) VALUES (?,?,?,?,?,?,?,?,?,?)",(card_name,card_tag,card_priority,card_storypoint,card_description,card_status,card_type,list_id,user_name,sprint_id))
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
            if value != None:
                self.cursor.execute(
                    "Update card set "+field+ " = "+ parse(value) +" where card_id =" + str(card_id))
            else:
                self.cursor.execute(
                    "Update card set "+field+ " = NULL  where card_id =" + str(card_id))
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


    """
    Fetches all information of a card
    Returns:
        A tuple with information of a card
    """
    def select_card(self, card_id) :
        try :
            self.cursor.execute(
                "SELECT * from CARD where card_id = "+ str(card_id))
            return self.cursor.fetchall()[0]
        except Exception as e :
            return e

    """
    #######################################################################################################################
    Sprint
    #######################################################################################################################
    """

    """
        Creates a sprint
    """
    def create_sprint(self,sprint_name,sprint_status=None,sprint_start=None,sprint_end=None):
        try:
            self.cursor.execute("insert into Sprint (sprint_name,sprint_status,sprint_start,sprint_end) VALUES (?,?,?,?)",(sprint_name,sprint_status,sprint_start,sprint_end))
        except Exception as e :
            return e

    """
    Updates a sprint
    Example: 
    """
    def update_sprint(self ,field, value, sprint_id) :
        try :
            self.cursor.execute(
                "Update sprint set "+field+ " = '"+ str(value) +"' where sprint_id =" + str(sprint_id))
        except Exception as e :
            return e

    """
    Display all sprints
    Example: 
    """
    def all_sprint(self) :
        try :
            self.cursor.execute(
                "Select * from sprint")
            return self.cursor.fetchall()
        except Exception as e :
            return e

    """
    Delete sprint
    Example: 
    """
    def delete_sprint(self,sprint_id) :
        try :
            self.cursor.execute(
                "Delete from sprint where sprint_id = "+str(sprint_id))
        except Exception as e :
            return e


    """
    Print all tasks associated with a sprint
    Returns list of tuples [(),(),()]

    Example:
        I want to get all tasks associated with sprint 1
            sprint_tasks(1)
    """

    def sprint_tasks(self , sprint_id) :
        try :
            self.cursor.execute(
                "select * from card inner join sprint ON sprint.sprint_id = card.sprint_id where sprint.sprint_id = "+ str(sprint_id))
            return self.cursor.fetchall()
        except Exception as e :
            return e

    """
    #######################################################################################################################
    Time Tracking
    #######################################################################################################################
    """

    """
    Fetches all time values for a specific card
    """
    def card_times(self, card_id):
        try :
            self.cursor.execute(
                "SELECT * from card_time where card_id = "+ str(card_id))
            return self.cursor.fetchall()
        except Exception as e :
            return e

    """
    Update values in card_time
    """
    def update_card_times(self, card_time_id,field,value):
        try :
            self.cursor.execute(
                "Update card_time set "+field+ " = '"+ str(value) +"' where card_time_id =" + str(card_time_id))
        except Exception as e :
            return e

    """
    Does stop function for a task, adds a new record for said stop time
    Add True boolean to the end of the argument to execute complete
    
   Example:
        I click complete for task with card_id 1
            task_stop(1,"xyztime","xyzhours",True)
    """
    def card_stop(self, card_id, card_time_stop=None,card_time_elapsed=None,complete = False):
        try :
            self.cursor.execute(
                "insert into card_time (card_id,card_time_stop,card_time_elapsed) VALUES (?,?,?)",(card_id,card_time_stop,card_time_elapsed))
            if complete:
                self.cursor.execute("Update card set card_status = 'done' where card_id =" + str(card_id))
        except Exception as e :
            return e

# db = Database()
# db.clean_db()


