from tkinter import *

from app.operation.table_view import Table_View
from app.operation.access_control import Access_Control

import app.operation.login as login
import app.operation.connect_db as connect_db
import app.operation.connected_dbs as connected_dbs
import app.operation.database_view as db_view

# Header Font Style
HEADER_STYLE = ('Arial', 14, 'bold')

# Sub-header Font Style
SUB_HEADER_STYLE = ('Arial', 12, 'bold')

# Data Font Style
DATA_STYLE = ('Arial', 11, 'normal')

# Data Header Font Style
DATA_HEADER_STYLE = ('Arial', 11, 'bold')

## Main app class
#
class App(Tk):

    ## Generates the main window,
    # the current page var and the page switching function
    def __init__(self):
        # Inherits from Tk - making an instance of App (self) the main window - root
        Tk.__init__(self)

        self.current_page = None

        LOGIN_GUI = Login_GUI(self)
        self.show_frame(LOGIN_GUI)

    ## Displays the passed page by hiding the 
    # current page first and packing the new page
    # if not logged in and the passed page is not the login page 
    # then the user is redirected to the login page
    def show_frame(self, new_page):
        
        if self.current_page:
            self.current_page.grid_forget()

        if not login.logged_in and str(new_page) != ".!login_gui":
            LOGIN_GUI = Login_GUI(self)
            new_page = LOGIN_GUI

        self.current_page = new_page

        new_page.grid(row=0, column=0)

    ## Refreshes the given frame by destroying its elements and
    # executes the provided function with any arguments given
    def refresh_frame(self, frame, function, args):

        for widget in frame.winfo_children():
            widget.destroy()

        function(*args) if args is not None else function()

## Generates the login page
#
class Login_GUI(Frame):

    def __init__(self, main_window):
        # Inherits from Frame - creating a frame embedded within the main window
        Frame.__init__(self, main_window)
        self.configure(bg="white")

        self.main_window = main_window

        # Main Box
        main_frame = Frame(self, highlightbackground="grey", highlightthickness=1, bg="white")
        main_frame.grid(row=0, column=0, padx=300, pady=20)

        # Welcome Texts
        welcome_text = Label(main_frame, text="-Welcome to CipherBytesDB-", font=('Arial', 25, 'bold'), bg="white", fg="blue")
        welcome_text.grid(row=0, column=1, padx=70, pady=10)

        exp_text_1 = Label(main_frame, text="A reliable and comprehensive encryption tool for MySQL", font=('Arial', 15, 'bold'), bg="white", fg="blue")
        exp_text_1.grid(row=1, column=1, padx=70)

        # The Line
        canvas = Canvas(main_frame, bg="white", highlightthickness=0, width=300, height=2)
        line = canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        canvas.grid(row=2, column=1, sticky="ew", padx=15, pady=20) # fill=BOTH

        # Login Box
        login_frame = Frame(main_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        login_frame.grid(row=3, column=1, padx=20, pady=(5, 20))

        # Login Variables
        username = StringVar()
        password = StringVar()
        error_msg = StringVar()

        # Login Input - Usename
        username_label = Label(login_frame, text='Username', font=DATA_HEADER_STYLE, bg="white")
        username_label.grid(row=0, column=0, pady=(10,5))

        username_entry = Entry(login_frame, textvariable=username, font=DATA_STYLE)
        username_entry.grid(row=1, column=0, padx=100)

        # Login Input - Password
        password_label = Label(login_frame, text='Password', font=DATA_HEADER_STYLE, bg="white")
        password_label.grid(row=2, column=0, pady=5)

        password_entry = Entry(login_frame, textvariable=password, font=DATA_STYLE, show='*')
        password_entry.grid(row=3, column=0)

        # Error Message
        error_text = Label(login_frame, textvariable=error_msg, font=DATA_STYLE, bg="white", fg="red", anchor="w")
        error_text.grid(row=4, column=0)

        # Login Button
        login_button = Button(login_frame, text='Login', command=lambda: login.login(username, password, error_msg, self.show_home_page, self.show_conn_db_page))
        login_button.grid(row=5, column=0)

    ## Displays Connect_Database_1_GUI frame
    #
    def show_conn_db_page(self):
        CONN_DB_GUI_1 = Connect_Database_1_GUI(self.main_window)
        self.main_window.show_frame(CONN_DB_GUI_1)

    ## Displays Home_GUI frame
    #
    def show_home_page(self):
        HOME_GUI = Home_GUI(self.main_window)
        self.main_window.show_frame(HOME_GUI)

## Generates the first step of connecting a new database
#
class Connect_Database_1_GUI(Frame):

    def __init__(self, main_window):
        # Inherits from Frame - creating a frame embedded within the main window
        Frame.__init__(self, main_window)
        self.configure(bg="white")

        self.main_window = main_window

        # Main Box
        main_frame = Frame(self, highlightbackground="grey", highlightthickness=1, bg="white")
        main_frame.grid(row=0, column=0, padx=350, pady=20)

        # Text
        text = Label(main_frame, text="Connect your database to start securing your data", font=HEADER_STYLE, bg="white", fg="black")
        text.grid(row=0, column=1, padx=70, pady=10)

        # Input Box
        input_frame = Frame(main_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        input_frame.grid(row=1, column=1, padx=20, pady=(5, 20))

        # Input Variables
        host = StringVar()
        db_name = StringVar()
        db_nick = StringVar()
        username = StringVar()
        password = StringVar()
        error_msg = StringVar()

        # Input - Host
        host_label = Label(input_frame, text='Host Address', font=DATA_HEADER_STYLE, bg="white")
        host_label.grid(row=0, column=0, pady=(10,5))

        host_entry = Entry(input_frame, textvariable=host, font=DATA_STYLE)
        host_entry.grid(row=1, column=0, padx=100)

        # Input - Database Name
        db_name_label = Label(input_frame, text='Database Name', font=DATA_HEADER_STYLE, bg="white")
        db_name_label.grid(row=2, column=0, pady=(10,5))

        db_name_entry = Entry(input_frame, textvariable=db_name, font=DATA_STYLE)
        db_name_entry.grid(row=3, column=0, padx=100)

        # Input - Database Nickname
        db_nick_label = Label(input_frame, text='Database Nickname', font=DATA_HEADER_STYLE, bg="white")
        db_nick_label.grid(row=4, column=0, pady=(10,5))

        db_nick_entry = Entry(input_frame, textvariable=db_nick, font=DATA_STYLE)
        db_nick_entry.grid(row=5, column=0, padx=100)

        # Input - Username
        username_label = Label(input_frame, text='Username', font=DATA_HEADER_STYLE, bg="white")
        username_label.grid(row=6, column=0, pady=(10,5))

        username_entry = Entry(input_frame, textvariable=username, font=DATA_STYLE)
        username_entry.grid(row=7, column=0, padx=100)

        # Input - Password
        password_label = Label(input_frame, text='Password', font=DATA_HEADER_STYLE, bg="white")
        password_label.grid(row=8, column=0, pady=(10,5))

        password_entry = Entry(input_frame, textvariable=password, font=DATA_STYLE, show='*')
        password_entry.grid(row=9, column=0)

        # Key Rotation Interval
        key_rotation_label = Label(input_frame, text="Key Rotation Interval", font=DATA_HEADER_STYLE, bg="white")
        key_rotation_label.grid(row=10, column=0, pady=(10,5))
        
        interval_list = ['Yearly', 'Monthly', 'Weekly', 'Daily']
        
        key_rotation_interval = StringVar()
        key_rotation_interval.set(interval_list[1])

        key_rotation_dropdown = OptionMenu(input_frame, key_rotation_interval, *interval_list)
        key_rotation_dropdown.config(width=15, font=DATA_STYLE, bg="white", highlightthickness=0)
        key_rotation_dropdown.grid(row=11, column=0)

        # Error Message
        error_text = Label(input_frame, textvariable=error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text.grid(row=12, column=0, pady=5)

        # The Line
        canvas = Canvas(input_frame, bg="white", highlightthickness=0, width=300, height=2)
        line = canvas.create_line(0, 1, 600, 1, width=1, fill="grey")
        canvas.grid(row=13, column=0, sticky="ew", padx=15)

        # Cancel Button
        cancel_button = Button(input_frame, text='Cancel', command=self.cancel_button_pressed)
        cancel_button.grid(row=14, column=0, padx=(0, 100))

        # Connect Button
        connect_button = Button(input_frame, text='Connect', command=lambda: connect_db.first_step(host, db_name, db_nick, username, password, key_rotation_interval, error_msg, self.show_conn_db_2_page))
        connect_button.grid(row=14, column=0, padx=(100,0), pady=10)

    ## Displays either Home_GUI or Login_GUI
    #
    def cancel_button_pressed(self):
        HOME_GUI = Home_GUI(self.main_window)
        LOGIN_GUI = Login_GUI(self.main_window)
        self.main_window.show_frame(HOME_GUI) if login.logged_in else self.main_window.show_frame(LOGIN_GUI)

    ## Displays Connect_Database_2_GUI frame
    #
    def show_conn_db_2_page(self, error_msg):
        CONN_DB_GUI_2 = Connect_Database_2_GUI(self.main_window, error_msg)
        self.main_window.show_frame(CONN_DB_GUI_2)

## Generates the second step of connecting a new database
#
class Connect_Database_2_GUI(Frame):

    def __init__(self, main_window, error_msg):
        # Inherits from Frame - creating a frame embedded within the main window
        Frame.__init__(self, main_window)
        self.configure(bg="white")

        self.main_window = main_window
        self.error_msg = error_msg

        # Main Box
        main_frame = Frame(self, highlightbackground="grey", highlightthickness=1, bg="white")
        main_frame.grid(row=0, column=0, padx=160, pady=20)

        # Main Header
        db = connect_db.database_name
        main_header = Label(main_frame, text=f"Users of {db} Database", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        main_header.grid(row=0, column=0, padx=15, pady=10, sticky="sw")

        # Scroll Canvas
        sb_canvas = Canvas(main_frame, width = 950, height = 660, bg="white", highlightbackground="grey")
        sb_canvas.grid(row=1, column=0)

        # Scroll Bar
        scrollbar = Scrollbar(main_frame, orient="vertical", bg="white", command=sb_canvas.yview)
        scrollbar.grid(row=1, column=1, sticky="nsew") # fill=Y

        # Configure Scroll Canvas
        sb_canvas.configure(yscrollcommand=scrollbar.set)
        sb_canvas.bind(
            "<Configure>",
            lambda e: sb_canvas.configure(
                scrollregion=sb_canvas.bbox("all")
            )
        )

        # Scrollable Frame
        self.scrollable_frame = Frame(sb_canvas, bg="white", pady=10)

        # Place Scrollable Frame inside canvas's window
        sb_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Generate Data
        self.generate_data()

        # Error Message
        error_text = Label(main_frame, textvariable=self.error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text.grid(row=3, column=0, pady=(15,0), padx=10, sticky="nw")

        # Complete Button
        complete_button = Button(main_frame, text='Complete', command=lambda: self.complete_button_pressed())
        complete_button.grid(row=3, column=0, pady=(10,10), sticky="se")

    ## Generates the dynamic user data bit
    #
    def generate_data(self):
        # Header 1
        header1 = Label(self.scrollable_frame, text="Username", font=SUB_HEADER_STYLE, bg="white", fg="black")
        header1.grid(row=1, column=1, padx=150)

        # Header 2
        header2 = Label(self.scrollable_frame, text="User Privilage", font=SUB_HEADER_STYLE, bg="white", fg="black")
        header2.grid(row=1, column=2, padx=(130,20))

        # Data
        ## Remove Button
        ## Username Label
        ## Role Label
        for index, (key, value) in enumerate(connect_db.database_users.items()):
            Button(self.scrollable_frame, text="x", bg="blue", fg="white", command=lambda k=key: self.remove_button_pressed(k)).grid(row=index+2, column=0, padx=(30,10))
            
            Label(self.scrollable_frame, text=key, bg="white").grid(row=index+2, column=1)
            
            Label(self.scrollable_frame, text=value, bg="white").grid(row=index+2, column=2, padx=(95,0))

    ## Calls remove_user function and
    # refresh the page
    def remove_button_pressed(self, username):
        connect_db.remove_user(username, self.error_msg)        
        self.main_window.refresh_frame(self.scrollable_frame, self.generate_data, None)

    ## Adds the users to the database
    # and switches to home page
    def complete_button_pressed(self):
        users_added = connect_db.add_users(self.error_msg)

        if users_added:
            HOME_GUI = Home_GUI(self.main_window)
            self.main_window.show_frame(HOME_GUI)

## Generates the home page
#
class Home_GUI(Frame):

    def __init__(self, main_window):
        # Inherits from Frame - creating a frame embedded within the main window
        Frame.__init__(self, main_window)
        self.configure(bg="white")

        self.main_window = main_window

        # Calls the Connected Databases GUI
        CONN_DBS = Connected_Databases_GUI(self.main_window, self)

## Generates the connected databases box
#
class Connected_Databases_GUI():
    
    ## Unlike the previous GUI classes - this is not a child of tkinter.Frame
    # it extends the Home_GUI's frame
    def __init__(self, main_window, parent_frame):
        self.main_window = main_window
        self.parent_frame = parent_frame

        self.generate_connected_dbs()

    ## Generates the main box
    #
    def generate_connected_dbs(self):
        # Connected DBs Box
        conn_db_frame = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        conn_db_frame.grid(row=0, column=0, padx=20, pady=20)

        # Conn DB Header
        main_header = Label(conn_db_frame, text="Connected Databases", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        main_header.grid(row=0, column=0, padx=(15,100), pady=10, sticky="w")

        # New DB Connection Button
        conn_db_button = Button(conn_db_frame, text="+", command=self.show_conn_db_page)
        conn_db_button.grid(row=0, column=0, padx=(310,0), pady=10)

        # Scroll Canvas
        sb_canvas = Canvas(conn_db_frame, width = 350, height = 620, bg="white", highlightbackground="grey")
        sb_canvas.grid(row=1, column=0)

        # Scroll Bar
        scrollbar = Scrollbar(conn_db_frame, width=15, orient="vertical", bg="white", command=sb_canvas.yview)
        scrollbar.grid(row=1, column=1, sticky="nsew") # fill=Y

        # Configure Scroll Canvas
        sb_canvas.configure(yscrollcommand=scrollbar.set)
        sb_canvas.bind(
            "<Configure>",
            lambda e: sb_canvas.configure(
                scrollregion=sb_canvas.bbox("all")
            )
        )

        # Scrollable Frame
        self.scrollable_frame = Frame(sb_canvas, bg="white", pady=10)

        # Place Scrollable Frame inside canvas's window
        sb_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.conn_dbs_error_msg = StringVar()

        # Generate Data
        self.generate_conn_dbs_data()

        # Error Message
        error_text_1 = Label(conn_db_frame, textvariable=self.conn_dbs_error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text_1.grid(row=2, column=0, pady=(10,0), padx=15, sticky="w")

        # Logout Button
        logout_button = Button(conn_db_frame, text ="Logout", command=self.logout)
        logout_button.grid(row=3, column=0, padx=15, pady=(10, 10), sticky="w")

    ## Displays Connect_Database_1_GUI frame
    #
    def show_conn_db_page(self):
        CONN_DB_GUI_1 = Connect_Database_1_GUI(self.main_window)
        self.main_window.show_frame(CONN_DB_GUI_1)

    ## Logout function:
    # + Sets logged_in to False
    # + Displays Login_GUI frame
    def logout(self):
        login.logged_in = False
        LOGIN_GUI = Login_GUI(self.main_window)
        self.main_window.show_frame(LOGIN_GUI)

    ## Calls the database view function
    #
    def database_pressed(self, host, db_name, db_nick, username, key_rotation_interval):
        DB_VIEW = Database_View_GUI(self.main_window, self.parent_frame, [host, db_name, db_nick, username, key_rotation_interval])
        DB_VIEW.generate_database_view()

    ## Generates dynamic connected databases data
    #
    def generate_conn_dbs_data(self):
        connected_dbs.get_connections(self.conn_dbs_error_msg)

        # Empty Message
        empty_msg = Label(self.scrollable_frame, text="No database has been connected.\nClick on the above plus button to connect\nyour database and start securing your data.", font=DATA_HEADER_STYLE, bg="white", fg="black", anchor="w")

        num_conn_dbs = len(connected_dbs.connected_dbs)

        if num_conn_dbs == 0:
            empty_msg.grid(row=2, column=0, pady=(10,0), padx=15, sticky="w")
        else:
            # Data
            ## Database Button
            ## Edit Button
            ## Delete Button
            for index, (key, value) in enumerate(connected_dbs.connected_dbs.items()):
                host = key.split(":")[0]
                db_name = key.split(":")[1]
                username = value[0]
                db_nick = value[1]
                key_rotation_interval = value[2]

                main = db_nick if db_nick != "" else key

                Button(self.scrollable_frame, text=main, bg="#ffffff", fg="black", font=DATA_HEADER_STYLE, highlightthickness=0, command=lambda h=host, dbn=db_name, dbni=db_nick, un=username, kri=key_rotation_interval: self.database_pressed(h, dbn, dbni, un, kri)).grid(row=index+2, column=0, sticky="w", padx=(15,100), pady=(0, 0))

                Button(self.scrollable_frame, text="Edit", bg="blue", fg="white", command=lambda h=host, dbn=db_name, dbni=db_nick, un=username, kri=key_rotation_interval: self.security_check(h, dbn, dbni, un, kri)).grid(row=index+2, column=1, padx=(0,5), pady=(0, 0))

                Button(self.scrollable_frame, text="x", bg="blue", fg="white", command=lambda h=host, dbn=db_name, dbni=db_nick: self.remove_button_pressed(h, dbn, dbni)).grid(row=index+2, column=2, pady=(0, 0))

    ## Calls disconnect database function
    # and refreshes the page
    def remove_button_pressed(self, host, db_name, db_nick):
        db_disconnected = connected_dbs.disconnect_database(host, db_name, db_nick, self.conn_dbs_error_msg)
        
        if db_disconnected:
            self.conn_dbs_error_msg.set("")
            self.main_window.refresh_frame(self.scrollable_frame, self.generate_conn_dbs_data, None)

    ## Generates the edit steps' header
    # 
    def generate_db_header(self, frame, db_name, host):
        # Main Header
        db_header = Label(frame, text=f"{host}:{db_name}", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        db_header.grid(row=0, column=0, sticky="w", padx=15, pady=5)

        # Top Line
        top_canvas = Canvas(frame, bg="white", highlightthickness=0, width=300, height=2)
        top_line = top_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        top_canvas.grid(row=1, column=0, columnspan=1, sticky="ew") # fill=BOTH
    
    ## Gets the current password and validates
    #
    def security_check(self, host, db_name, db_nick, username, key_rotation_interval):
        # Main Box
        self.security_check_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.security_check_box.grid(row=0, column=2, padx=230)

        # Generate the Header and Line
        self.generate_db_header(self.security_check_box, db_name, host) 

        # Explanation Text
        exp_text = Label(self.security_check_box, text="You need to complete the security step to\nedit the connection", font=DATA_STYLE, bg="white", fg="black", anchor="w")
        exp_text.grid(row=2, column=0, padx=15, pady=(5,0))

        # Current Password Label
        curr_password_label = Label(self.security_check_box, text="Current Password", font=DATA_HEADER_STYLE, bg="white", fg="black")
        curr_password_label.grid(row=3, column=0, sticky="w", padx=15, pady=(10,0))

        # Current Password Entry
        current_password = StringVar()

        curr_password_entry = Entry(self.security_check_box, textvariable=current_password, font=DATA_STYLE, width=40, show='*')
        curr_password_entry.grid(row=4, column=0, padx=15, pady=(5,0))

        # Error Message
        error_msg = StringVar()

        error_text = Label(self.security_check_box, textvariable=error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text.grid(row=5, column=0, pady=(5,0), padx=15, sticky="w")

        # Bottom Line
        bottom_canvas = Canvas(self.security_check_box, bg="white", highlightthickness=0, width=300, height=2)
        top_line = bottom_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        bottom_canvas.grid(row=6, column=0, columnspan=1, sticky="ew", pady=(10,0)) # fill=BOTH

        # Cancel Button
        cancel_button = Button(self.security_check_box, text="Cancel", command=self.security_check_box.grid_forget)
        cancel_button.grid(row=7, column=0, pady=10, padx=100, sticky="e")

        # Submit Button
        submit_button = Button(self.security_check_box, text="Submit", bg="blue", fg="white", command=lambda: self.submit_button_pressed(host, db_name, db_nick, username, current_password, key_rotation_interval, error_msg))
        submit_button.grid(row=7, column=0, padx=15, sticky="e")

    ## Calls check password function and
    # displays change password page if correct password
    def submit_button_pressed(self, host, db_name, db_nick, username, password_input, key_rotation_interval, error_msg):
        correct_password = connected_dbs.check_password(host, db_name, db_nick, password_input, error_msg)

        if correct_password:
            error_msg.set("")
            self.generate_db_edit_view(host, db_name, db_nick, username, key_rotation_interval)

    ## Generates the DB edit view
    #
    def generate_db_edit_view(self, host, db_name, db_nick, username, key_rotation_interval):
        self.security_check_box.grid_forget()

        # Main Box
        self.db_edit_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.db_edit_box.grid(row=0, column=2, padx=230)

        # Generate the Header and Line
        self.generate_db_header(self.db_edit_box, db_name, host)

        # Host Label
        host_label = Label(self.db_edit_box, text=host, font=DATA_STYLE, bg="white", fg="black", borderwidth=1, relief="solid", width=40, anchor="w")
        host_label.grid(row=2, column=0, sticky="w", padx=15, pady=(10,0))

        # Database Name Label
        db_name_label = Label(self.db_edit_box, text=db_name, font=DATA_STYLE, bg="white", fg="black", borderwidth=1, relief="solid", width=40, anchor="w")
        db_name_label.grid(row=3, column=0, sticky="w", padx=15, pady=(10,0))

        # Database Nickname Entry
        new_db_nick = StringVar()

        nickname_entry = Entry(self.db_edit_box, textvariable=new_db_nick, font=DATA_STYLE, width=40)
        nickname_entry.grid(row=4, column=0, sticky="w", padx=15, pady=(10,0))
        nickname_entry.delete(0, 'end')

        if db_nick != "":
            nickname_entry.insert(0, db_nick)
        else:
            nickname_entry.insert(0, "Database Nickname")

        # Username Entry
        new_username = StringVar()

        username_entry = Entry(self.db_edit_box, textvariable=new_username, font=DATA_STYLE, width=40)
        username_entry.grid(row=5, column=0, sticky="w", padx=15, pady=(10,0))
        username_entry.delete(0, 'end')
        username_entry.insert(0, username)

        # Change Password Button
        password_button = Button(self.db_edit_box, text ="Change Password", font=('Arial', 11, 'bold', 'underline'), bg="#ffffff", borderwidth=0, fg="blue", command=lambda: self.change_password(host, db_name, db_nick, username, key_rotation_interval))
        password_button.grid(row=6, column=0, sticky="w", padx=15, pady=(10,0))

        # Key Rotation Interval
        key_rotation_label = Label(self.db_edit_box, text="Key Rotation Interval", font=DATA_HEADER_STYLE, bg="white")
        key_rotation_label.grid(row=7, column=0, sticky="w", padx=15, pady=(10,5))
        
        interval_list = ['Yearly', 'Monthly', 'Weekly', 'Daily']
        
        new_key_rotation = StringVar()
        new_key_rotation.set(key_rotation_interval)

        key_rotation_dropdown = OptionMenu(self.db_edit_box, new_key_rotation, *interval_list)
        key_rotation_dropdown.config(width=15, font=DATA_STYLE, bg="white", highlightthickness=0)
        key_rotation_dropdown.grid(row=8, column=0, sticky="w", padx=15)

        # Error Message
        error_msg = StringVar()

        error_text = Label(self.db_edit_box, textvariable=error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text.grid(row=9, column=0, pady=(5,0), padx=15, sticky="w")

        # Bottom Line
        bottom_canvas = Canvas(self.db_edit_box, bg="white", highlightthickness=0, width=300, height=2)
        top_line = bottom_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        bottom_canvas.grid(row=10, column=0, columnspan=1, sticky="ew", pady=(10,0)) # fill=BOTH

        # Cancel Button
        cancel_button = Button(self.db_edit_box, text="Cancel", command=self.db_edit_box.grid_forget)
        cancel_button.grid(row=11, column=0, pady=10, padx=100, sticky="e")

        # Update Button
        update_button = Button(self.db_edit_box, text="Update", bg="blue", fg="white", command=lambda: self.update_db_configs(host, db_name, new_db_nick, new_username, new_key_rotation, error_msg))
        update_button.grid(row=11, column=0, padx=15, sticky="e")

    ## Calls edit database function
    # and hides the box and refreshes the connected dbs
    def update_db_configs(self, host, db_name, db_nick, username, key_rotation_interval, error_msg):
        updated = connected_dbs.edit_connection(host, db_name, db_nick, username, key_rotation_interval, error_msg)

        if updated:
            error_msg.set("")
            self.db_edit_box.grid_forget()
            self.main_window.refresh_frame(self.scrollable_frame, self.generate_conn_dbs_data, None)

    ## Change password:
    # + Hide db edit view
    # + Display change password view
    # + Get new password
    def change_password(self, host, db_name, db_nick, username, key_rotation_interval):
        self.db_edit_box.grid_forget()

        # Main Box
        self.password_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.password_box.grid(row=0, column=2, padx=230)

        # Generate the Header and Line
        self.generate_db_header(self.password_box, db_name, host) 

        # Explanation Text
        exp_text = Label(self.password_box, text="Please enter your new database password below", font=DATA_STYLE, bg="white", fg="black", anchor="w")
        exp_text.grid(row=2, column=0, sticky="w", padx=15, pady=(5,0))

        # New Password Label
        new_password_label = Label(self.password_box, text="New Password", font=DATA_HEADER_STYLE, bg="white", fg="black")
        new_password_label.grid(row=3, column=0, sticky="w", padx=15, pady=(10,0))

        # New Password Entry
        new_password = StringVar()

        new_password_entry = Entry(self.password_box, textvariable=new_password, font=DATA_STYLE, width=40, show='*')
        new_password_entry.grid(row=4, column=0, padx=15, pady=(5,0))

        # New Password Repeat Label
        new_password_repeat_label = Label(self.password_box, text="Repeat New Password", font=DATA_HEADER_STYLE, bg="white", fg="black")
        new_password_repeat_label.grid(row=5, column=0, sticky="w", padx=15, pady=(10,0))

        # New Password Repeat Entry 
        new_password_repeat = StringVar()

        new_password_entry_repeat = Entry(self.password_box, textvariable=new_password_repeat, font=DATA_STYLE, width=40, show='*')
        new_password_entry_repeat.grid(row=6, column=0, padx=15, pady=(5,0))

        # Error Message
        error_msg = StringVar()

        error_text = Label(self.password_box, textvariable=error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text.grid(row=7, column=0, pady=(5,0), padx=15, sticky="w")

        # Bottom Line
        bottom_canvas = Canvas(self.password_box, bg="white", highlightthickness=0, width=300, height=2)
        top_line = bottom_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        bottom_canvas.grid(row=8, column=0, columnspan=1, sticky="ew", pady=(10,0)) # fill=BOTH

        # Cancel Button
        cancel_button = Button(self.password_box, text="Cancel", command=self.cancel_password_change)
        cancel_button.grid(row=9, column=0, pady=10, padx=100, sticky="e")

        # Change Button
        change_button = Button(self.password_box, text="Submit", bg="blue", fg="white", command=lambda: self.change_button_pressed(host, db_name, db_nick, username, new_password, new_password_repeat, key_rotation_interval, error_msg))
        change_button.grid(row=9, column=0, padx=15, sticky="e")

    ## Hides the password change view and
    # displays db edit box
    def cancel_password_change(self):
        self.password_box.grid_forget()
        self.db_edit_box.grid(row=0, column=2, padx=230)

    ## Calls update password and
    # displays success page if successful
    def change_button_pressed(self, host, db_name, db_nick, username, new_password, new_password_repeat, key_rotation_interval, error_msg):
        updated = connected_dbs.update_password(host, db_name, db_nick, username, new_password, new_password_repeat, key_rotation_interval, error_msg)

        if updated:
            error_msg.set("")
            self.generate_success_page(host, db_name)

    ## Hides the password change page and
    # generates the success page
    def generate_success_page(self, host, db_name):
        self.password_box.grid_forget()

        # Main Box
        pc_success_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        pc_success_box.grid(row=0, column=2, padx=230)

        # Generate the Header and Line
        self.generate_db_header(pc_success_box, db_name, host)

        # Image

        # Success Message
        success_msg = Label(pc_success_box, text=f"Database {db_name}'s password has been successfully changed", font=DATA_STYLE, bg="white", fg="black")
        success_msg.grid(row=2, column=0, pady=(10,0))

        # Bottom Line
        bottom_canvas = Canvas(pc_success_box, bg="white", highlightthickness=0, width=300, height=2)
        top_line = bottom_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        bottom_canvas.grid(row=3, column=0, columnspan=1, sticky="ew", pady=(10,0)) # fill=BOTH

        # Complete Button
        complete_button = Button(pc_success_box, text="Complete", bg="blue", fg="white", command=pc_success_box.grid_forget)
        complete_button.grid(row=4, column=0, pady=10, padx=15, sticky="e")

## Generates the database view box
#
class Database_View_GUI():
    
    ## Unlike the previous GUI classes - this is not a child of tkinter.Frame
    # it extends the Home_GUI's frame
    def __init__(self, main_window, parent_frame, db_data_pack):
        self.main_window = main_window
        self.parent_frame = parent_frame

        self.DB_DATA_PACK = db_data_pack
        self.HOST = db_data_pack[0]
        self.DB_NAME = db_data_pack[1]
        self.DB_NICK = db_data_pack[2]
        self.USERNAME = db_data_pack[3]
        self.KEY_ROTATION_INTERVAL = db_data_pack[4]

    ## Generates the database view
    #
    def generate_database_view(self):
        # Database View Box
        self.db_view_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.db_view_box.grid(row=0, column=2, padx=(0,20), pady=20, sticky="n")

        # Main Header
        db_header = Label(self.db_view_box, text=f"{self.HOST}:{self.DB_NAME}", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        db_header.grid(row=0, column=0, sticky="w", padx=(15,500), pady=10)

        # Scroll Canvas
        sb_canvas = Canvas(self.db_view_box, width = 848, height = 705, bg="white", highlightbackground="grey")
        sb_canvas.grid(row=1, column=0, columnspan=3, sticky="w")

        # Scroll Bar
        scrollbar = Scrollbar(self.db_view_box, width=15, orient="vertical", bg="white", command=sb_canvas.yview)
        scrollbar.grid(row=1, column=3, sticky="nsew") # fill=Y

        # Configure Scroll Canvas
        sb_canvas.configure(yscrollcommand=scrollbar.set)
        sb_canvas.bind(
            "<Configure>",
            lambda e: sb_canvas.configure(
                scrollregion=sb_canvas.bbox("all")
            )
        )

        # Scrollable Frame
        scrollable_frame = Frame(sb_canvas, bg="white", pady=10)

        # Place Scrollable Frame inside canvas's window
        sb_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        error_msg = StringVar()

        db_view.gen_db_view(self.HOST, self.DB_NAME, self.DB_NICK, self.USERNAME, error_msg)

        # Table Name Header
        header1 = Label(scrollable_frame, text="Table Name", font=SUB_HEADER_STYLE, bg="white", fg="black")
        header1.grid(row=0, column=0, padx=(15,100))

        # Encrypted Header
        header2 = Label(scrollable_frame, text="Encrypted", font=SUB_HEADER_STYLE, bg="white", fg="black")
        header2.grid(row=0, column=1, padx=(100,100))

        # Encryption Models Header
        header2 = Label(scrollable_frame, text="Encryption Models", font=SUB_HEADER_STYLE, bg="white", fg="black")
        header2.grid(row=0, column=2, padx=(100,30))

        # Error Message
        error_text = Label(scrollable_frame, textvariable=error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text.grid(row=1, column=0, padx=(15,0), pady=(10,0), sticky="w", columnspan=2)

        # Data
        ## Table View Button
        ## Encrypted Label
        ## Encryption Model Label
        for index, (key, value) in enumerate(db_view.db_tables.items()):
            Button(scrollable_frame, text=key, bg="#ffffff", borderwidth=0, fg="black", command=lambda tn=key: self.table_pressed(tn)).grid(row=index+2, column=0, padx=15, pady=(10,0), sticky="w")

            Label(scrollable_frame, text=value[0], bg="white").grid(row=index+2, column=1, padx=(0,15), pady=(10,0))

            enc_models = value[1]
            for i in range(len(enc_models)):
                Label(scrollable_frame, text=enc_models[i], bg="white").grid(row=index+i+2, column=2, padx=(0,15), pady=(10,0))

    ## Hides the database view box and
    # displays the table view
    def table_pressed(self, table_name):
        self.db_view_box.grid_forget()

        TABLE_VIEW = Table_View_GUI(self.main_window, self.parent_frame, self.DB_DATA_PACK, table_name)
        TABLE_VIEW.generate_table_view()

## Generates the table view box
#
class Table_View_GUI():

    ## Unlike the previous GUI classes - this is not a child of tkinter.Frame
    # it extends the Home_GUI's frame
    def __init__(self, main_window, parent_frame, db_data_pack, table_name):
        self.main_window = main_window
        self.parent_frame = parent_frame

        self.DB_DATA_PACK = db_data_pack
        self.TABLE_NAME = table_name

        self.table_view = Table_View(db_data_pack, table_name)

        self.is_tle_visible = True
        self.is_cle_visible = True
        self.is_rle_visible = True
        self.is_cele_visible = True

    ## Generates the table view
    #
    def generate_table_view(self):
        # Table View Box
        self.table_view_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.table_view_box.grid(row=0, column=2, padx=(0,20), pady=20, sticky="n")
        
        # Main Header
        table_header = Label(self.table_view_box, text=f"{self.TABLE_NAME}", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        table_header.grid(row=0, column=0, sticky="w", padx=(15,0), pady=(10,5))

        # Access Control Button
        ac_button = Button(self.table_view_box, text="Access Control", bg="blue", fg="white", command=self.ac_button_pressed)
        ac_button.grid(row=0, column=0, pady=(10,0), padx=(0,0), sticky="e")

        # Table Level Encryption Box Header
        tle_header = Label(self.table_view_box, width=103, text="Table Level Encryption", font=DATA_HEADER_STYLE, bg="grey", fg="black")
        tle_header.grid(row=1, column=0, sticky="w")

        # Table Level Encryption Box - Init
        tle_box = Frame(self.table_view_box, highlightbackground="grey", highlightthickness=1, bg="white")

        # Table Level Encryption Toggle Button
        tle_toggle = Button(self.table_view_box, text="v", bg="grey", borderwidth=0, fg="black", font=DATA_HEADER_STYLE, command=lambda: self.toggle_enc_block(tle_box, self.is_tle_visible, 2))
        tle_toggle.grid(row=1, column=1, sticky="w")

        # Table Level Encryption Box - Grid
        tle_box.grid(row=2, column=0, padx=10, sticky="w", columnspan=2)

        # Table Level Encryption Enable Toggle
        toggle_txt = Label(tle_box, text="Table Level Encryption", font=DATA_HEADER_STYLE, bg="#ffffff", fg="black", anchor="w")
        toggle_txt.grid(row=0, column=0, padx=(15,60), pady=(10,0), sticky="w")

        tle_error_msg = StringVar()

        tle_enabled = self.table_view.is_tle_enabled(tle_error_msg)

        # Enabled - Off and remove
        if tle_enabled:
            tle_enc_toggle = Button(tle_box, text="Turn Off", relief=RAISED, bg="red", fg="white", command=lambda: self.call_remove("0", self.TABLE_NAME, tle_error_msg))
        # Disabled - On and enable
        else:
            tle_enc_toggle = Button(tle_box, text="Turn On", relief=RAISED, bg="green", fg="white", command=lambda: self.call_ac_popup("0", self.TABLE_NAME, tle_error_msg))  

        tle_enc_toggle.grid(row=0, column=1, padx=(0,540), pady=(10,0), sticky="w")

        # Table Level Encryption Error Message
        tle_error_text = Label(tle_box, textvariable=tle_error_msg, font=DATA_STYLE, bg="white", fg="red")
        tle_error_text.grid(row=1, column=0, padx=15, pady=5, sticky="w", columnspan=2)

        # Column Level Encryption Box Header
        cle_header = Label(self.table_view_box, width=103, text="Column Level Encryption", font=DATA_HEADER_STYLE, bg="grey", fg="black")
        cle_header.grid(row=3, column=0, pady=(10,0), sticky="w")

        # Column Level Encryption Box - Init
        cle_box = Frame(self.table_view_box, highlightbackground="grey", highlightthickness=0, bg="white")

        # Column Level Encryption Toggle Button
        cle_toggle = Button(self.table_view_box, text="v", bg="grey", borderwidth=0, fg="black", font=DATA_HEADER_STYLE, command=lambda: self.toggle_enc_block(cle_box, self.is_cle_visible, 4))
        cle_toggle.grid(row=3, column=1, pady=(5,0), sticky="w")

        # Column Level Encryption Box - Grid
        cle_box.grid(row=4, column=0, padx=10, sticky="w", columnspan=2)

        # Scroll Canvas
        cle_sb_canvas = Canvas(cle_box, width = 835, height = 200, bg="white", highlightbackground="grey")
        cle_sb_canvas.grid(row=0, column=0)

        # Scroll Bar
        cle_scrollbar = Scrollbar(cle_box, width=15, orient="vertical", bg="white", command=cle_sb_canvas.yview)
        cle_scrollbar.grid(row=0, column=1, sticky="nsew") # fill=Y

        # Configure Scroll Canvas
        cle_sb_canvas.configure(yscrollcommand=cle_scrollbar.set)
        cle_sb_canvas.bind(
            "<Configure>",
            lambda e: cle_sb_canvas.configure(
                scrollregion=cle_sb_canvas.bbox("all")
            )
        )

        # Scrollable Frame
        cle_scrollable_frame = Frame(cle_sb_canvas, bg="white")

        # Place Scrollable Frame inside canvas's window
        cle_sb_canvas.create_window((0, 0), window=cle_scrollable_frame, anchor="nw")

        # Column Level Encryption Error Message
        cle_error_msg = StringVar()

        cle_error_text = Label(cle_scrollable_frame, textvariable=cle_error_msg, font=DATA_STYLE, bg="white", fg="red")
        cle_error_text.grid(row=0, column=0, padx=(15,0), pady=5, sticky="w", columnspan=2)

        # Column Name Header
        cle_header_1 = Label(cle_scrollable_frame, text=f"Column Name", font=SUB_HEADER_STYLE, bg="white", fg="black", anchor="w")
        cle_header_1.grid(row=1, column=1, sticky="w", padx=(15,100), pady=(0,10))

        # Encrypted Header
        cle_header_2 = Label(cle_scrollable_frame, text=f"Encrypted", font=SUB_HEADER_STYLE, bg="white", fg="black", anchor="w")
        cle_header_2.grid(row=1, column=2, sticky="w", padx=(0,20), pady=(0,10))

        columns = self.table_view.gen_column_view(cle_error_msg)

        # Data
        ## Delete Button if encrypted
        ## Column Name - button if not encrypted else label
        ## Encryption Label
        for index, (key, value) in enumerate(columns.items()):
            if value == 'Y':
                Button(cle_scrollable_frame, text="x", font=DATA_STYLE, bg="blue", fg="white", command=lambda id=key: self.call_remove("1", id, cle_error_msg)).grid(row=index+2, column=0, sticky="w", padx=(15,0))
                Label(cle_scrollable_frame, text=key, font=DATA_STYLE, bg="white", fg="black").grid(row=index+2, column=1, sticky="w", padx=(15,100))
            else:
                Button(cle_scrollable_frame, text=key, font=DATA_STYLE, bg="#ffffff", borderwidth=0, fg="black", command=lambda c=key: self.call_ac_popup("1", c, cle_error_msg)).grid(row=index+2, column=1, sticky="w", padx=(15,100))

            Label(cle_scrollable_frame, text=value, font=DATA_STYLE, bg="white", fg="black").grid(row=index+2, column=2, sticky="w", padx=(0,20))
        
        # Row Level Encryption Box Header
        rle_header = Label(self.table_view_box, width=103, text="Row Level Encryption", font=DATA_HEADER_STYLE, bg="grey", fg="black")
        rle_header.grid(row=5, column=0, pady=(10,0), sticky="w")

        # Row Level Encryption Box - Init
        rle_box = Frame(self.table_view_box, highlightbackground="grey", highlightthickness=0, bg="white")

        # Row Level Encryption Toggle Button
        rle_toggle = Button(self.table_view_box, text="v", bg="grey", borderwidth=0, fg="black", font=DATA_HEADER_STYLE, command=lambda: self.toggle_enc_block(rle_box, self.is_rle_visible, 6))
        rle_toggle.grid(row=5, column=1, pady=(5,0), sticky="w")

        # Row Level Encryption Box - Grid
        rle_box.grid(row=6, column=0, padx=10, sticky="w", columnspan=2)

        # Scroll Canvas
        rle_sb_canvas = Canvas(rle_box, width = 835, height = 200, bg="white", highlightbackground="grey")
        rle_sb_canvas.grid(row=0, column=0)

        # Scroll Bar
        rle_scrollbar = Scrollbar(rle_box, width=15, orient="vertical", bg="white", command=rle_sb_canvas.yview)
        rle_scrollbar.grid(row=0, column=1, sticky="nsew") # fill=Y

        # Configure Scroll Canvas
        rle_sb_canvas.configure(yscrollcommand=rle_scrollbar.set)
        rle_sb_canvas.bind(
            "<Configure>",
            lambda e: rle_sb_canvas.configure(
                scrollregion=rle_sb_canvas.bbox("all")
            )
        )

        # Scrollable Frame
        rle_scrollable_frame = Frame(rle_sb_canvas, bg="white")

        # Place Scrollable Frame inside canvas's window
        rle_sb_canvas.create_window((0, 0), window=rle_scrollable_frame, anchor="nw")

        # Row Level Encryption Error Message
        rle_error_msg = StringVar()

        rle_error_text = Label(rle_scrollable_frame, textvariable=rle_error_msg, font=DATA_STYLE, bg="white", fg="red")
        rle_error_text.grid(row=0, column=0, padx=(15,0), pady=5, sticky="w", columnspan=2)

        # Primary Key Header
        rle_header_1 = Label(rle_scrollable_frame, text=f"Primary Key Value", font=SUB_HEADER_STYLE, bg="white", fg="black", anchor="w")
        rle_header_1.grid(row=1, column=1, sticky="w", padx=(15,100), pady=(0,10))

        # Encrypted Header
        rle_header_2 = Label(rle_scrollable_frame, text=f"Encrypted", font=SUB_HEADER_STYLE, bg="white", fg="black", anchor="w")
        rle_header_2.grid(row=1, column=2, sticky="w", padx=(0,20), pady=(0,10))

        rows = self.table_view.gen_row_view(rle_error_msg)

        # Data
        ## Delete Button if encrypted
        ## Primary Column Row Value - button if not encrypted else label
        ## Encryption Label
        for index, (key, value) in enumerate(rows.items()):
            if value == 'Y':
                Button(rle_scrollable_frame, text="x", font=DATA_STYLE, bg="blue", fg="white", command=lambda id=key: self.call_remove("2", id, rle_error_msg)).grid(row=index+2, column=0, sticky="w", padx=(15,0))
                Label(rle_scrollable_frame, text=key, font=DATA_STYLE, bg="white", fg="black").grid(row=index+2, column=1, sticky="w", padx=(15,100))
            else:
                Button(rle_scrollable_frame, text=key, font=DATA_STYLE, bg="#ffffff", borderwidth=0, fg="black", command=lambda r=key: self.call_ac_popup("2", r, rle_error_msg)).grid(row=index+2, column=1, sticky="w", padx=(15,100))

            Label(rle_scrollable_frame, text=value, font=DATA_STYLE, bg="white", fg="black").grid(row=index+2, column=2, sticky="w", padx=(0,20))

        # Cell Level Encryption Box Header
        cele_header = Label(self.table_view_box, width=103, text="Cell Level Encryption", font=DATA_HEADER_STYLE, bg="grey", fg="black")
        cele_header.grid(row=7, column=0, pady=(10,0), sticky="w")

        # Cell Level Encryption Box - Init
        cele_box = Frame(self.table_view_box, highlightbackground="grey", highlightthickness=0, bg="white")

        # Cell Level Encryption Toggle Button
        cele_toggle = Button(self.table_view_box, text="v", bg="grey", borderwidth=0, fg="black", font=DATA_HEADER_STYLE, command=lambda: self.toggle_enc_block(cele_box, self.is_cele_visible, 8))
        cele_toggle.grid(row=7, column=0, pady=(5,0), sticky="e")

        # Encrypt Cell Button
        cell_enc_button = Button(self.table_view_box, text="+", bg="blue", fg="white", command=self.gen_cele_step_1)
        cell_enc_button.grid(row=7, column=1, pady=(5,0), sticky="w")

        # Cell Level Encryption Box - Grid
        cele_box.grid(row=8, column=0, padx=10, sticky="w", columnspan=2)

        # Scroll Canvas
        cele_sb_canvas = Canvas(cele_box, width = 835, height = 95, bg="white", highlightbackground="grey")
        cele_sb_canvas.grid(row=0, column=0, pady=(0,5))

        # Scroll Bar
        cele_scrollbar = Scrollbar(cele_box, width=15, orient="vertical", bg="white", command=cele_sb_canvas.yview)
        cele_scrollbar.grid(row=0, column=1, sticky="nsew") # fill=Y

        # Configure Scroll Canvas
        cele_sb_canvas.configure(yscrollcommand=cele_scrollbar.set)
        cele_sb_canvas.bind(
            "<Configure>",
            lambda e: cele_sb_canvas.configure(
                scrollregion=cele_sb_canvas.bbox("all")
            )
        )

        # Scrollable Frame
        cele_scrollable_frame = Frame(cele_sb_canvas, bg="white")

        # Place Scrollable Frame inside canvas's window
        cele_sb_canvas.create_window((0, 0), window=cele_scrollable_frame, anchor="nw")

        # Cell Level Encryption Error Message
        cele_error_msg = StringVar()

        cele_error_text = Label(cele_scrollable_frame, textvariable=cele_error_msg, font=DATA_STYLE, bg="white", fg="red")
        cele_error_text.grid(row=0, column=0, padx=(15,0), pady=5, sticky="w", columnspan=2)

        # Cell Level Encryption Empty Message
        empty_msg = Label(cele_scrollable_frame, text="No cells have been encrypted yet. Click on the above plus button to start encrypting.", font=DATA_HEADER_STYLE, bg="white", fg="black", anchor="w")

        # Cell Identifier Header
        cele_header_1 = Label(cele_scrollable_frame, text=f"Cell Identifier", font=SUB_HEADER_STYLE, bg="white", fg="black", anchor="w")
        
        cells = self.table_view.gen_cell_view(cele_error_msg)

        if len(cells) == 0:
            empty_msg.grid(row=1, column=0, sticky="w", padx=(15,0))
        else:
            cele_header_1.grid(row=1, column=1, sticky="w", padx=(5,0), pady=(0,10))

            # Data
            ## Delete Button
            ## Cell Identifier Label
            for i in range(len(cells)):
                Button(cele_scrollable_frame, text="x", font=DATA_STYLE, bg="blue", fg="white", command=lambda id=cells[i]: self.call_remove("3", id, cele_error_msg)).grid(row=i+2, column=0, sticky="w", padx=(15,0))
                Label(cele_scrollable_frame, text=cells[i], font=DATA_STYLE, bg="white", fg="black").grid(row=i+2, column=1, sticky="w", padx=(5,0))

    ## Hides the database view box and
    # displays the access control page
    def ac_button_pressed(self):
        self.table_view_box.grid_forget()

        ACCESS_CONTROL = Access_Control_GUI(self.main_window, self.parent_frame, self.DB_DATA_PACK, self.TABLE_NAME)
        ACCESS_CONTROL.generate_ac_page()

    ## Toggles the given encryption box's visibility
    #
    def toggle_enc_block(self, box, is_visible, row_no):

        if is_visible:
            box.grid_forget()

            # Table Level Encryption
            if row_no == 2:
                self.is_tle_visible = False
            # Column Level Encryption
            elif row_no == 4:
                self.is_cle_visible = False
            # Row Level Encryption
            elif row_no == 6:
                self.is_rle_visible = False
            # Cell Level Encryption
            elif row_no == 8:
                self.is_cele_visible = False
        
        elif (not is_visible):
            box.grid(row=row_no, column=0, padx=10, sticky="w", columnspan=2)

            # Table Level Encryption
            if row_no == 2:
                self.is_tle_visible = True
            # Column Level Encryption
            elif row_no == 4:
                self.is_cle_visible = True
            # Row Level Encryption
            elif row_no == 6:
                self.is_rle_visible = True
            # Cell Level Encryption
            elif row_no == 8:
                self.is_cele_visible = True

    ## Calls the access control popup generation
    # and passes the necessary details for encryption
    def call_ac_popup(self, model, identifier, table_view_error_msg):
        ACCESS_CONTROL = Access_Control_GUI(self.main_window, self.parent_frame, self.DB_DATA_PACK, self.TABLE_NAME)
        ACCESS_CONTROL.generate_ac_popup(model, identifier, table_view_error_msg, self.table_view_box)

    ## Calls remove encryption function and
    # refreshes the page if successful
    def call_remove(self, model, identifier, error_msg):
        enc_removed = self.table_view.remove_encryption(model, identifier, error_msg)

        if enc_removed:
            error_msg.set("")
            self.main_window.refresh_frame(self.table_view_box, self.generate_table_view, None)

    ## Generates the first step CeLE and
    # gets cell inputs
    def gen_cele_step_1(self):
        # Main Box
        self.cell_input_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.cell_input_box.grid(row=0, column=2, padx=230)

        # Main Header
        cele_header = Label(self.cell_input_box, text="Encrypt New Cell(s)", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        cele_header.grid(row=0, column=0, sticky="w", padx=15, pady=(5,0))

        # Top Line
        top_canvas = Canvas(self.cell_input_box, bg="white", highlightthickness=0, width=300, height=2)
        top_line = top_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        top_canvas.grid(row=1, column=0, columnspan=1, sticky="ew", pady=(5,0)) # fill=BOTH

        # Explanation Text
        exp_text = Label(self.cell_input_box, text="Please enter the cell identifier. If there are more than 1,\nplease seperate them using a semicolon (;).", font=DATA_STYLE, bg="white", fg="black", anchor="w")
        exp_text.grid(row=2, column=0, padx=15, pady=(5,0), sticky="w")

        # Cells Input Area
        cells_input = Text(self.cell_input_box, height=5, width=50, font=DATA_STYLE)
        cells_input.grid(row=3, column=0, padx=15, pady=(10,0), sticky="w")
        cells_input.delete('1.0', END)
        cells_input.insert(INSERT, "Example: credit_limit:5;name:10")

        # Error Message
        error_msg = StringVar()

        error_text = Label(self.cell_input_box, textvariable=error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text.grid(row=4, column=0, pady=(5,0), padx=15, sticky="w")

        # Bottom Line
        bottom_canvas = Canvas(self.cell_input_box, bg="white", highlightthickness=0, width=300, height=2)
        bottom_line = bottom_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        bottom_canvas.grid(row=5, column=0, columnspan=1, sticky="ew", pady=(10,0)) # fill=BOTH

        # Cancel Button
        cancel_button = Button(self.cell_input_box, text="Cancel", command=self.cell_input_box.grid_forget)
        cancel_button.grid(row=6, column=0, pady=10, padx=85, sticky="e")

        # Next Button
        next_button = Button(self.cell_input_box, text="Next", bg="blue", fg="white", command=lambda c=cells_input, e=error_msg: self.next_button_pressed(c, e))
        next_button.grid(row=6, column=0, padx=15, sticky="e")

    ## Gets the cells and calls the get cells function
    # If successful, calls the preview function and
    # generates second step UI
    def next_button_pressed(self, cells, error_msg):
        cells = cells.get(1.0, "end-1c")

        cells_finalised = self.table_view.get_cells(cells, error_msg)

        if cells_finalised:
            error_msg.set("")

            preview = self.table_view.generate_cell_preview(error_msg)

            self.gen_cele_step_2(preview) if len(preview) > 0 else None

    ## Generates the second step CeLE and
    # displays the cell preview
    def gen_cele_step_2(self, preview):
        # Main Box
        self.cell_preview_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.cell_preview_box.grid(row=0, column=2, padx=230)

        # Main Header
        cele_header = Label(self.cell_preview_box, text="Encrypt New Cell(s) - Preview", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        cele_header.grid(row=0, column=0, sticky="w", padx=15, pady=(5,0))

        # Top Line
        top_canvas = Canvas(self.cell_preview_box, bg="white", highlightthickness=0, width=300, height=2)
        top_line = top_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        top_canvas.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5,0)) # fill=BOTH

        # Explanation Text
        exp_text = Label(self.cell_preview_box, text="Please check the below preview and confirm these are the cells\nyou would like to encrypt.", font=DATA_STYLE, bg="white", fg="black", anchor="w")
        exp_text.grid(row=2, column=0, padx=15, pady=(5,0), sticky="w")

        # Scroll Canvas
        sb_canvas = Canvas(self.cell_preview_box, bg="white", height=150, highlightthickness=0, highlightbackground="grey")
        sb_canvas.grid(row=3, column=0, pady=(10,0))

        # Scroll Bar
        scrollbar = Scrollbar(self.cell_preview_box, width=15, orient="vertical", bg="white", command=sb_canvas.yview)
        scrollbar.grid(row=3, column=1, sticky="nsew") # fill=Y

        # Configure Scroll Canvas
        sb_canvas.configure(yscrollcommand=scrollbar.set)
        sb_canvas.bind(
            "<Configure>",
            lambda e: sb_canvas.configure(
                scrollregion=sb_canvas.bbox("all")
            )
        )

        # Scrollable Frame
        scrollable_frame = Frame(sb_canvas, bg="white")

        # Place Scrollable Frame inside canvas's window
        sb_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Data Header
        data_header = Label(scrollable_frame, text="Data", font=DATA_HEADER_STYLE, bg="white", fg="black")
        data_header.grid(row=0, column=0, padx=15, pady=(5,0), sticky="w")

        # Data
        ## Data label
        for i in range(len(preview)):
            Label(scrollable_frame, text=preview[i], font=DATA_STYLE, bg="white", fg="black").grid(row=i+1, column=0, padx=15, pady=(5,0), sticky="w")

        # Bottom Line
        bottom_canvas = Canvas(self.cell_preview_box, bg="white", highlightthickness=0, width=300, height=2)
        bottom_line = bottom_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        bottom_canvas.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10,0)) # fill=BOTH

        # Cancel Button
        cancel_button = Button(self.cell_preview_box, text="Cancel", command=self.cell_preview_box.grid_forget)
        cancel_button.grid(row=6, column=0, pady=10, padx=95, sticky="e")

        # Confirm Button
        confirm_button = Button(self.cell_preview_box, text="Confirm", bg="blue", fg="white", command=self.generate_warning_page)
        confirm_button.grid(row=6, column=0, padx=(0,5), sticky="e")

    ## Generates the third step CeLE and
    # displays the warning on constraints
    def generate_warning_page(self):
        self.cell_input_box.grid_forget()
        self.cell_preview_box.grid_forget()

        # Main Box
        self.warning_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.warning_box.grid(row=0, column=2, padx=230)

        # Main Header
        cele_header = Label(self.warning_box, text="Encrypt New Cell(s) - Warning", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        cele_header.grid(row=0, column=0, sticky="w", padx=15, pady=(5,0))

        # Top Line
        top_canvas = Canvas(self.warning_box, bg="white", highlightthickness=0, width=300, height=2)
        top_line = top_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        top_canvas.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5,0)) # fill=BOTH

        # Explanation Text
        exp_text = Label(self.warning_box, text="Please note that any constraints set on the given column\nwill be dropped except for the primary key constraint.\nYou can find the list of constraints below:\n  - Default\n  - Auto increment\n  - Not null\n  - Check\n  - Foreign key\n  - Unique\n\nPlease only proceed if these changes won't affect\nyour application logic.", font=DATA_STYLE, bg="white", fg="black", anchor="w")
        exp_text.grid(row=2, column=0, padx=15, pady=(5,0), sticky="w")

        # Error Message
        error_msg = StringVar()

        error_text = Label(self.warning_box, textvariable=error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text.grid(row=3, column=0, padx=15, pady=(5,0), sticky="w")

        # Bottom Line
        bottom_canvas = Canvas(self.warning_box, bg="white", highlightthickness=0, width=300, height=2)
        bottom_line = bottom_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        bottom_canvas.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10,0)) # fill=BOTH

        # Cancel Button
        cancel_button = Button(self.warning_box, text="Cancel", command=self.warning_box.grid_forget)
        cancel_button.grid(row=5, column=0, pady=10, padx=95, sticky="e")

        # Confirm Button
        confirm_button = Button(self.warning_box, text="Confirm", bg="blue", fg="white", command=lambda e=error_msg:self.confirm_button_pressed(e))
        confirm_button.grid(row=5, column=0, padx=(0,5), sticky="e")

    ## Calls encrypt cells function and generates
    # the success page if successful
    def confirm_button_pressed(self, error_msg):
        cells_encrypted = self.table_view.encrypt_cells(error_msg)

        if cells_encrypted:
            error_msg.set("")
            self.generate_success_page()

    ## Hides the input and preview boxes and
    # generates the success page
    def generate_success_page(self):
        self.warning_box.grid_forget()

        # Main Box
        self.success_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.success_box.grid(row=0, column=2, padx=230)

        # Main Header
        cele_header = Label(self.success_box, text="Encrypt New Cell(s)", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        cele_header.grid(row=0, column=0, sticky="w", padx=15, pady=(5,0))

        # Top Line
        top_canvas = Canvas(self.success_box, bg="white", highlightthickness=0, width=300, height=2)
        top_line = top_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        top_canvas.grid(row=1, column=0, columnspan=1, sticky="ew", pady=(5,0)) # fill=BOTH

        # Image

        # Success Message
        success_msg = Label(self.success_box, text=f"Cells have been successfully encrypted", font=DATA_STYLE, bg="white", fg="black")
        success_msg.grid(row=2, column=0, pady=(10,0))

        # Bottom Line
        bottom_canvas = Canvas(self.success_box, bg="white", highlightthickness=0, width=300, height=2)
        bottom_line = bottom_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        bottom_canvas.grid(row=3, column=0, columnspan=1, sticky="ew", pady=(10,0)) # fill=BOTH

        # Complete Button
        complete_button = Button(self.success_box, text="Complete", bg="blue", fg="white", command=self.success_complete_button_pressed)
        complete_button.grid(row=4, column=0, pady=10, padx=15, sticky="e")
    
    ## Hides the success page and refreshes 
    # the table view
    def success_complete_button_pressed(self):
        self.success_box.grid_forget()
        self.main_window.refresh_frame(self.table_view_box, self.generate_table_view, None)

## Generates the database access control box
#
class Access_Control_GUI(Table_View_GUI):

    ## Unlike the previous GUI classes - this is not a child of tkinter.Frame
    # it extends the Home_GUI's frame
    def __init__(self, main_window, parent_frame, db_data_pack, table_name):
        # Inherits from Table_View_GUI - uses its variables and functions
        super().__init__(main_window, parent_frame, db_data_pack, table_name)

        self.DB_NAME = db_data_pack[1]

        self.users = []

        self.access_control = Access_Control(db_data_pack, table_name)

    ## Generates the main access policy page
    #
    def generate_ac_page(self):
        # Access Control Box
        self.ac_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.ac_box.grid(row=0, column=2, padx=(0,20), pady=20, sticky="n")

        # Main Header
        ac_header = Label(self.ac_box, text=f"{self.DB_NAME}:{self.TABLE_NAME} Access Control", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        ac_header.grid(row=0, column=0, sticky="w", padx=(15,500), pady=10)

        # Add Button
        add_button = Button(self.ac_box, text="+", bg="blue", fg="white", command=self.generate_add_popup)
        add_button.grid(row=0, column=1, pady=10)

        # Scroll Canvas
        sb_canvas = Canvas(self.ac_box, width = 862, height = 705, bg="white", highlightbackground="grey")
        sb_canvas.grid(row=1, column=0, columnspan=2, sticky="w")

        # Scroll Bar
        scrollbar = Scrollbar(self.ac_box, width=15, orient="vertical", bg="white", command=sb_canvas.yview)
        scrollbar.grid(row=1, column=2, sticky="nsew") # fill=Y

        # Configure Scroll Canvas
        sb_canvas.configure(yscrollcommand=scrollbar.set)
        sb_canvas.bind(
            "<Configure>",
            lambda e: sb_canvas.configure(
                scrollregion=sb_canvas.bbox("all")
            )
        )

        # Scrollable Frame
        scrollable_frame = Frame(sb_canvas, bg="white", pady=10)

        # Place Scrollable Frame inside canvas's window
        sb_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Error Message
        error_msg = StringVar()

        error_text = Label(scrollable_frame, textvariable=error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text.grid(row=0, column=0, padx=(15,0), pady=(5,10), sticky="w", columnspan=2)

        # Empty message
        empty_msg = Label(scrollable_frame, text="No access control rule has been set yet. Click on the above plus button to create a new one.", font=DATA_HEADER_STYLE, bg="white", fg="black", anchor="w")

        ac_rules = self.access_control.get_ac_rules(error_msg)

        if len(ac_rules) == 0:
            empty_msg.grid(row=1, column=0, pady=(10,0), padx=15, sticky="w")
        else:
            # User ID Header
            header1 = Label(scrollable_frame, text=f"User ID", font=SUB_HEADER_STYLE, bg="white", fg="black", anchor="w")
            header1.grid(row=1, column=0, padx=(80,50), pady=(0,5))

            # Username Header
            header2 = Label(scrollable_frame, text=f"Username", font=SUB_HEADER_STYLE, bg="white", fg="black", anchor="w")
            header2.grid(row=1, column=1, padx=(30,200), pady=(0,5))

            # Key ID header
            header3 = Label(scrollable_frame, text=f"Key ID", font=SUB_HEADER_STYLE, bg="white", fg="black", anchor="w")
            header3.grid(row=1, column=2, padx=(30,0), pady=(0,5))

            # Data
            ## Delete Button
            ## User ID
            ## Username
            ## Key ID
            for i in range(len(ac_rules)):
                rule = ac_rules[i]

                Button(scrollable_frame, text="x", font=DATA_STYLE, bg="blue", fg="white", command=lambda u=rule[0], k=rule[2]: self.delete_button_pressed(u, k, error_msg)).grid(row=i+2, column=0, sticky="w", padx=(15,0))
                Label(scrollable_frame, text=rule[0], font=DATA_STYLE, bg="white", fg="black").grid(row=i+2, column=0, sticky="w", padx=(80,50))
                Label(scrollable_frame, text=rule[1], font=DATA_STYLE, bg="white", fg="black").grid(row=i+2, column=1, sticky="w", padx=(30,200))
                Label(scrollable_frame, text=rule[2], font=DATA_STYLE, bg="white", fg="black").grid(row=i+2, column=2, sticky="w", padx=(30,0))

    ## Generates the add rule popup on the main
    # access policy page
    def generate_add_popup(self):
        # Main Box
        self.ac_ad_popup_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.ac_ad_popup_box.grid(row=0, column=2, padx=210)

        # Main Header
        ac_ad_header = Label(self.ac_ad_popup_box, text="Add New Access Control Rule", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        ac_ad_header.grid(row=0, column=0, sticky="w", padx=15, pady=(5,0))

        # Top Line
        top_canvas = Canvas(self.ac_ad_popup_box, bg="white", highlightthickness=0, width=300, height=2)
        top_line = top_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        top_canvas.grid(row=1, column=0, columnspan=1, sticky="ew", pady=(5,0)) # fill=BOTH

        # Error Message
        error_msg = StringVar()

        error_text = Label(self.ac_ad_popup_box, textvariable=error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text.grid(row=2, column=0, padx=15, pady=(10,0), sticky="w")

        # Username Header
        username_header = Label(self.ac_ad_popup_box, text="Username", font=DATA_HEADER_STYLE, bg="white", fg="black")
        username_header.grid(row=3, column=0, padx=15, pady=(5,0), sticky="w")

        # Username Entry
        user = StringVar()

        username_entry = Entry(self.ac_ad_popup_box, width=38, textvariable=user, font=DATA_STYLE)
        username_entry.grid(row=4, column=0, padx=15, pady=(10,0), sticky="w")

        # Key ID Header
        key_id_header = Label(self.ac_ad_popup_box, text="Key ID", font=DATA_HEADER_STYLE, bg="white", fg="black")
        key_id_header.grid(row=5, column=0, padx=15, pady=(10,0), sticky="w")

        # Key ID Entry
        key_id = StringVar()

        key_id_entry = Entry(self.ac_ad_popup_box, width=38, textvariable=key_id, font=DATA_STYLE)
        key_id_entry.grid(row=6, column=0, padx=15, pady=(10,0), sticky="w")

        # Bottom Line
        bottom_canvas = Canvas(self.ac_ad_popup_box, bg="white", highlightthickness=0, width=300, height=2)
        bottom_line = bottom_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        bottom_canvas.grid(row=7, column=0, columnspan=1, sticky="ew", pady=(10,0)) # fill=BOTH

        # Cancel Button
        cancel_button = Button(self.ac_ad_popup_box, text="Cancel", command=self.ac_ad_popup_box.grid_forget)
        cancel_button.grid(row=8, column=0, pady=10, padx=85, sticky="e")
        
        # Done Button
        next_button = Button(self.ac_ad_popup_box, text="Done", bg="blue", fg="white", command=lambda r=[(user, key_id)]: self.done_button_pressed(r, error_msg))
        next_button.grid(row=8, column=0, padx=15, sticky="e")

    ## Validates the given rule and adds them to the database.
    # If successful refreshes the access rules page
    def done_button_pressed(self, rules, error_msg):
        rules_valid = self.access_control.validate_rules(rules, error_msg)

        rules_added = self.access_control.add_ac_rule(rules, error_msg) if rules_valid else False

        if rules_added:
            error_msg.set("")
            self.ac_ad_popup_box.grid_forget()
            self.main_window.refresh_frame(self.ac_box, self.generate_ac_page, None)

    ## Deletes the access policy rule and
    # refreshes the page if successful
    def delete_button_pressed(self, user_id, key_id, error_msg):
        rule_deleted = self.access_control.delete_ac_rule(user_id, key_id, error_msg)

        if rule_deleted:
            self.main_window.refresh_frame(self.ac_box, self.generate_ac_page, None)

    ## Generates the access policy popup on encryption
    # operations
    def generate_ac_popup(self, model, identifier, table_view_error_msg, table_view_box):
        # Main Box
        self.ac_popup_box = Frame(self.parent_frame, highlightbackground="grey", highlightthickness=1, bg="white")
        self.ac_popup_box.grid(row=0, column=2, padx=210)

        # Main Header
        ac_header = Label(self.ac_popup_box, text=f"'{identifier}' Access Control", font=HEADER_STYLE, bg="white", fg="black", anchor="w")
        ac_header.grid(row=0, column=0, sticky="w", padx=15, pady=(5,0))

        # Top Line
        top_canvas = Canvas(self.ac_popup_box, bg="white", highlightthickness=0, width=300, height=2)
        top_line = top_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        top_canvas.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(5,0)) # fill=BOTH

        # Explanation Text
        exp_text = Label(self.ac_popup_box, text="Please enter the username of users who can access this data", font=DATA_STYLE, bg="white", fg="black", anchor="w")
        exp_text.grid(row=2, column=0, padx=15, pady=(10,0), sticky="w")

        # Username Entry
        user = StringVar()

        user_entry = Entry(self.ac_popup_box, width=38, textvariable=user, font=DATA_STYLE)
        user_entry.grid(row=3, column=0, padx=15, pady=(10,0), sticky="w")

        # Add Button
        add_button = Button(self.ac_popup_box, text="Add", font=DATA_STYLE, bg="blue", fg="white", command=lambda u=user: self.popup_add_button_pressed(u, model, identifier, table_view_error_msg, table_view_box))
        add_button.grid(row=3, column=0, padx=(340,0), pady=(10,0), sticky="w")

        # Error Message
        error_msg = StringVar()

        error_text = Label(self.ac_popup_box, textvariable=error_msg, font=DATA_STYLE, bg="white", fg="red")
        error_text.grid(row=4, column=0, padx=15, pady=(5,0), sticky="w")

        # Users Header
        users_header = Label(self.ac_popup_box, text="Users", font=DATA_HEADER_STYLE, bg="white", fg="black")
        users_header.grid(row=5, column=0, padx=15, pady=(5,0), sticky="w")

        # Scroll Canvas
        sb_canvas = Canvas(self.ac_popup_box, bg="white", height=150, highlightthickness=0, highlightbackground="grey")
        sb_canvas.grid(row=6, column=0, pady=(10,0))

        # Scroll Bar
        scrollbar = Scrollbar(self.ac_popup_box, width=15, orient="vertical", bg="white", command=sb_canvas.yview)
        scrollbar.grid(row=6, column=1, sticky="nsew") # fill=Y

        # Configure Scroll Canvas
        sb_canvas.configure(yscrollcommand=scrollbar.set)
        sb_canvas.bind(
            "<Configure>",
            lambda e: sb_canvas.configure(
                scrollregion=sb_canvas.bbox("all")
            )
        )

        # Scrollable Frame
        scrollable_frame = Frame(sb_canvas, bg="white")

        # Place Scrollable Frame inside canvas's window
        sb_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Data
        ## Delete Button
        ## User Label
        for i in range(len(self.users)):
            Button(scrollable_frame, text="x", font=DATA_STYLE, bg="blue", fg="white", command=lambda u=self.users[i]: self.popup_delete_button_pressed(u, model, identifier, table_view_error_msg, table_view_box)).grid(row=i, column=0, pady=(5,0), padx=(5,0), sticky="w")
            Label(scrollable_frame, text=self.users[i], font=DATA_STYLE, bg="white", fg="black").grid(row=i, column=1, padx=15, pady=(5,0), sticky="w")

        # Bottom Line
        bottom_canvas = Canvas(self.ac_popup_box, bg="white", highlightthickness=0, width=300, height=2)
        bottom_line = bottom_canvas.create_line(0, 1, 800, 1, width=1, fill="grey")
        bottom_canvas.grid(row=7, column=0, columnspan=2, sticky="ew", pady=(10,0)) # fill=BOTH

        # Cancel Button
        cancel_button = Button(self.ac_popup_box, text="Cancel", command=self.ac_popup_box.grid_forget)
        cancel_button.grid(row=8, column=0, pady=10, padx=85, sticky="e")
        
        # Done Button
        next_button = Button(self.ac_popup_box, text="Done", bg="blue", fg="white", command=lambda: self.popup_done_button_pressed(model, identifier, table_view_error_msg, error_msg, table_view_box))
        next_button.grid(row=8, column=0, padx=15, sticky="e")

    ## Adds the given username to the list if not empty
    # and refreshes the page
    def popup_add_button_pressed(self, username, model, identifier, table_view_error_msg, table_view_box):
        username_input = username.get()

        if username_input != "":
            self.users.append(username_input)

            self.main_window.refresh_frame(self.ac_popup_box, self.generate_ac_popup, [model, identifier, table_view_error_msg, table_view_box])

    ## Removes the username from the list and
    # refreshes the page
    def popup_delete_button_pressed(self, username, model, identifier, table_view_error_msg, table_view_box):
        self.users.remove(username)
        self.main_window.refresh_frame(self.ac_popup_box, self.generate_ac_popup, [model, identifier, table_view_error_msg, table_view_box])

    ## Validates the users and calls the encryption function
    # based on the give model and refreshes the page if successful
    def popup_done_button_pressed(self, model, identifier, table_view_error_msg, error_msg, table_view_box):
        valid_users = self.access_control.validate_users(self.users, error_msg)

        if valid_users:
            self.ac_popup_box.destroy()

            encrypted = False

            if model == "0":
                encrypted = self.table_view.encrypt_table(self.users, table_view_error_msg)
            elif model == "1":
                encrypted = self.table_view.encrypt_column(identifier, self.users, table_view_error_msg)
            elif model == "2":
                encrypted = self.table_view.encrypt_row(identifier, self.users, table_view_error_msg)

            if encrypted:
                table_view_error_msg.set("")
                self.main_window.refresh_frame(table_view_box, self.generate_table_view, None)
