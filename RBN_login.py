import tkinter as tk
from datetime import date,datetime
import mysql.connector as mysql


class Login_window:

    def __init__(self, master):
        try:
            self.mydb = mysql.connect(host='hostname.com', port=3306, username = 'username',password = 'password',database = 'databaseName',use_pure = True) #replace with your own database details
        except:
            tk.messagebox.showerror("Error!!!","Check your internet connection")
        self.master = master
        self.master.title("Login")
        self.master.geometry("800x750+10+50")
        self.master.resizable(width=False,height=False)
        self.master.config(bg="#13051e")
        main_menu=tk.Menu(self.master)
        self.master.configure(menu=main_menu)
        main_menu.add_command(label="About",command = self.About)

        bank_logo_img=tk.PhotoImage(file="Raw/login_logo.png")
        #logo
        logo_label=tk.Label(self.master ,image = bank_logo_img,bg="#13051e")
        logo_label.place(x=150,y=0)

        #--------------variables--------------
        self.uname = ''
        self.passwd = ''
        self.next_window = ''

        #usernamelabel and entry box
        self.username=tk.StringVar()
        self.password=tk.StringVar()
        username_lbl=tk.Label(self.master,font=('arial',20,"bold"),text="Username",relief="sunken")
        username_lbl.place(x=160,y=410)
        self.username_entry=tk.Entry(self.master,font=('arial',20),textvariable=self.username)
        self.username_entry.place(x=320,y=410)
        self.username_entry.focus()

        #passowrd label and entry box
        password_lbl=tk.Label(self.master,font=('arial',20,"bold"),text="Passowrd",relief="sunken")
        password_lbl.place(x=160,y=460)
        password_entry=tk.Entry(self.master,show="*",font=('arial',20,"bold"),textvariable=self.password)
        password_entry.place(x=320,y=460)

        #-----------Clicking Enter will do login button press--------------- 
        self.master.bind('<Return>', self.login_system)

        #login Button
        button1 = tk.Button(self.master,font=('arial',20,"bold"), text = 'Login', width = 25, command = self.login_system,relief="raised")
        button1.place(x=175,y=530)
        
        #Register Account Button
        button1 = tk.Button(self.master,font=('arial',20,"bold"), text = 'Register New Account', width = 25,relief="raised",command=self.Register_acc)
        button1.place(x=175,y=600)

        #--------------------------------status bar--------------------------------#

        horStatus_lb=tk.Label(self.master,width=600,height=200,bg="black",font=('arial',5),relief="solid")
        horStatus_lb.place(x=1,y=720)
        date_lbl=tk.Label(self.master,text='',bg="black",fg="white")
        date_lbl.place(x=1,y=723)
        time_lbl=tk.Label(self.master,text='',bg="black",fg="white")
        time_lbl.place(x=750,y=723)


        def tick():
            today = datetime.today()
            now = datetime.now()
            # get the current local time from the PC
            local_time = now.strftime('%H:%M:%S')
            local_date = today.strftime("%B %d, %Y")
            date_lbl.config(text = local_date)
            time_lbl.config(text = local_time)
            # calls itself every 200 milliseconds
            # to update the time display as needed
            time_lbl.after(200, tick)
        #----------------TIME end-----------------
        tick()
        #------------------------------status_bar_end-----------------------

        self.master.mainloop()

    # Login button functin
    def login_system(self,event = None):
        self.uname=self.username.get()
        self.passwd=self.password.get()
        try:
            mycur = self.mydb.cursor()
            sql_script = "SELECT userid FROM users WHERE userid = %s and passwd = %s"
            mycur.execute(sql_script,(self.uname,self.passwd,))
            userid = mycur.fetchone()
            mycur.close()
            if userid is not None:
                self.next_window = 'Home'
                self.master.destroy()
            else:
                tk.messagebox.showerror("Error!!!","Wrong Username or Password")
                self.username.set("")
                self.password.set("")
                self.username_entry.focus()
        except:
            mycur.close()
            tk.messagebox.showerror("Error!!!","Something is wrong")

    def About(self):
        tk.messagebox.showinfo('Developers',"This is just a project don't give any personal information here\nThis project is made by\n1: SURESH KUMAR (BCA,Chaudhary Charan Singh University)\n2: SUVAJIT PATRA (BSC,VIDYASAGAR University)")

    # Register
    def Register_acc(self):
        self.mydb.close()
        tk.messagebox.showwarning("Warning!","Remember!!! \nThis is just a project made for educational \npurpose.You are advised not to give any \nsensitive personal details")
        self.next_window = 'Register'
        self.master.destroy()     
