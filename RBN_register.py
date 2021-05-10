import tkinter as tk
from tkinter import messagebox
from datetime import date,datetime
from tkinter import filedialog
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import base64
import mysql.connector as mysql
from mysql.connector import MySQLConnection, Error


class Account_window:

    def __init__(self,master,pr_window,uname,passwd,mode):
        try:
            self.mydb = mysql.connect(host='hostname.com', port=3306, username = 'username',password = 'password',database = 'databaseName',use_pure = True) #replace with your own database details
        except:
            tk.messagebox.showerror("Error!!!","Check your internet connection")

        self.master=master
        self.master.geometry("800x750+10+50")    
        self.master.resizable(width=False,height=False)
        self.master.config(bg="#13051e")

        #--------------main variables--------------
        self.mode = mode
        self.uname = uname
        self.passwd = passwd
        self.available = 'false'
        self.previous_window = pr_window
        self.next_window = ''

        #--------------secondary variables--------------
        self.im = tk.PhotoImage()
        self.photo_directory = tk.StringVar()
        self.branch_name = tk.StringVar()
        self.entry={
            "Name":tk.StringVar(),
            "Phone Number":tk.StringVar(),
            "Address":tk.StringVar(),
            "E-Mail":tk.StringVar(),
            "Aadhar Number":tk.StringVar(),
            "Username":tk.StringVar(),
            "Password":tk.StringVar(),
        }

        # Decisions
        if self.mode == 'Register':
            self.master.title('Register New Account')

            for i in self.entry:
                self.entry[i].set("")
            
            try:
                mycur = self.mydb.cursor()
                mycur.execute('SELECT brname FROM branches')
                choices_raw = mycur.fetchall()
                mycur.close()
            except:
                mycur.close()
                tk.messagebox.showerror("Error!!!","Something is wrong")

            # Dropdown with options
            choices = []
            for row in choices_raw:
                choices.append(str(row[0]))
            self.branch_name.set('Choose') # set the default option

            branchName_Menu = tk.OptionMenu(self.master, self.branch_name, *choices)
            branchName_Menu.place(x=170,y=570)
            branchName_Menu.config(height = 0,width = 10)
            branchName_label=tk.Label(self.master, font=('arial',15,'bold'),text="Branch Name",fg='white',bg="#13051e")
            branchName_label.place(x=23,y=570)
            
            # add account button
            sql_calls_button = tk.Button(self.master,font=('arial',16,"bold"), text = 'Register Account', width = 18,relief="raised",command = self.sql_calls)
            sql_calls_button.place(x=275,y=660)


        if self.mode != 'Details':
            # create entry box
            entry_y_axis=240
            for i in self.entry:
                cur_entry=tk.Entry(self.master,textvariable=self.entry[i],bg="white",fg="black",font=('arial',15,"bold"))
                if i == 'Username' and self.mode == 'Update':
                    cur_entry.config(state = tk.DISABLED)
                cur_entry.place(x=545,y=entry_y_axis)
                entry_y_axis+=60
                
            # browse button
            browseImg_btn=tk.Button(self.master,font=('arial',10,"bold"), text = 'Browse', width = 18,relief="raised",command = self.browsefunc)
            browseImg_btn.place(x=85,y=495)

        if self.mode == 'Update':
            self.master.title('Update Account')
            self.update_get()
            x = 0
            for i in self.entry:
                self.entry[i].set(str(self.user_details[x]))
                x = x + 1
            
            # Update account button
            sql_calls_button = tk.Button(self.master,font=('arial',16,"bold"), text = 'Update Account', width = 18,relief="raised",command = self.sql_calls)
            sql_calls_button.place(x=275,y=660)


        if self.mode == 'Details':
            self.master.title('Account Details')
            self.sql_calls()
            y_axis=240
            for i in range(8):
                cur_label=tk.Label(self.master,text = str(self.user_details[i]),fg = 'black',bg="white",width = 18,font=('arial',15,"bold"))
                cur_label.place(x=545,y=y_axis)
                y_axis+=60

        # Image variables
        logo_img=tk.PhotoImage(file="Raw/regis.png")
        default_photo=tk.PhotoImage(file="Raw/Photo.png")
    
        # LOGO
        logo_label=tk.Label(self.master ,image=logo_img,bg="#13051e")
        logo_label.place(x=0,y=0)

        # BANK NAME
        lbl_info=tk.Label(self.master,font=('Arial',30,'bold'),text="RESERVE BANK OF NOIDA",fg='#e73334',bg="#13051e")
        lbl_info.place(x=250,y=100)
    
        # create label
        label=["Name","Phone Number","Address ","E-Mail","Aadhar Number","Username","Password",""]
        if self.mode == 'Details':
            label[6] = "Account Balace"
            label[7] = "Account Number"
        y_axis=240
        for i in range(len(label)):
            if label[i] != "":
                cur_label=tk.Label(self.master,font=('arial',15,"bold"),text=label[i],fg="white",bg="#13051e")
                cur_label.place(x=355,y=y_axis)
                y_axis+=60

        # photo label
        userPhoto_label=tk.Label(self.master,font=('arial',15,"bold"),text="Photo",bg="#13051e",fg="white")
        userPhoto_label.place(x=130,y=240)

        self.Photo_label=tk.Label(self.master,bg="white",image = default_photo,width=150,height=200)
        self.Photo_label.place(x=85,y=280)


        #---------------------------------------------branch details----------------------------------------------
        if self.mode != 'Register':
            try:
                mycursor = self.mydb.cursor()
                sql_script = 'SELECT branches.brname,branches.brcode,branches.ifsc FROM branches,users WHERE branches.brcode = users.branchcode AND users.userid = %s'
                sql_script1 = 'SELECT photo FROM users WHERE userid = %s'
                mycursor.execute(sql_script,(self.uname,))
                branch_detail = mycursor.fetchone()
                mycursor.execute(sql_script1,(self.uname,))
                user_photo_raw = mycursor.fetchone()
                self.write_file(user_photo_raw[0],'cache/temp.png')
                user_photo = Image.open('cache/temp.png')
                user_photo = ImageTk.PhotoImage(user_photo)
                self.Photo_label.config(image = user_photo)
                self.Photo_label.image_names = user_photo
                mycursor.close()
            except:
                mycursor.close()
                tk.messagebox.showerror("Error!!!","Something is wrong")


            ifsc_code = branch_detail[2]
            branch_code = branch_detail[1]
            br_name = branch_detail[0]

            # branch name
            branchName_label=tk.Label(self.master, font=('arial',10),text="Branch Name ",fg='white',bg="#13051e")
            branchName_label.place(x=23,y=540)
            branchName_show=tk.Label(self.master,text = br_name,fg='black',bg="white",font=('arial',8,'bold'),width = 20)
            branchName_show.place(x=150,y=540)

            # branch code
            branchCode_label=tk.Label(self.master, font=('arial',10),text="Branch Code ",fg='white',bg="#13051e")
            branchCode_label.place(x=23,y=570)
            branchCode_show=tk.Label(self.master,text = branch_code,fg='black',bg="white",font=('arial',8,'bold'),width = 20)
            branchCode_show.place(x=150,y=570)

            # IFCS Code
            ifscCode_label=tk.Label(self.master, font=('arial',10),text="IFSC Code ",fg='white',bg="#13051e")
            ifscCode_label.place(x=23,y=600)
            ifscCode_show=tk.Label(self.master,text = ifsc_code,fg='black',bg="white",font=('arial',8,'bold'),width = 20)
            ifscCode_show.place(x=150,y=600)

        #Login Screen Button / Back button
        back_btn = tk.Button(self.master,font=('arial',10,"bold"), text = '<< Back', width = 10,relief="raised",command=self.back)
        back_btn.place(x=100,y=673)

        #----------------------------------status bar---------------------------------------#

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

    # Browse function
    def browsefunc(self):
        self.photo_directory = tk.filedialog.askopenfilename(title = "Choose Image",filetypes = (("jpeg or png files","*.jpg *.png"),("all files","*.*")))
        self.im = Image.open(self.photo_directory)
        self.im = ImageTk.PhotoImage(self.im)
        self.Photo_label.config(image = self.im)
        self.Photo_label.image_names = self.im

    # Convert binary data to proper format and write it on cache/
    def write_file(self,data,filename):
        with open(filename, "wb") as file:
            file.write(data)
        file.close()
    
    # Convert digital data to binary format
    def convertToBinaryData(self,filename):
        with open(filename, "rb") as file:
            binaryData = (file.read())
            return binaryData
    
    # back function
    def back(self):
        self.next_window = self.previous_window
        self.master.destroy()

    # add account function
    def sql_calls(self):
        if self.mode == 'Register':
            self.user_available()
            if self.available == 'false':
                tk.messagebox.showerror("Error!!!","Username unavailable")
        try:
            if self.mode == 'Register' and self.available == 'true':
                mycursor = self.mydb.cursor()
                sql_script = 'INSERT INTO users VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
                mycursor.execute('SELECT brcode FROM branches WHERE brname = %s',(self.branch_name.get(),))
                brcode = str(mycursor.fetchone()[0])
                t = 'temp'
                mycursor.execute("SELECT accntno FROM users WHERE userid = %s",(t,))
                lastaccntno = mycursor.fetchone()
                accntno = str(int(lastaccntno[0])+1)
                userPicture = self.convertToBinaryData(self.photo_directory)
                user = self.entry['Username'].get(),self.entry['Password'].get(),self.entry['Name'].get(),userPicture,accntno,self.entry['Address'].get(),self.entry['E-Mail'].get(),brcode,'0.00',self.entry['Aadhar Number'].get(),self.entry['Phone Number'].get()
                mycursor.execute(sql_script,user)
                mycursor.execute("UPDATE users SET accntno = %s WHERE userid = %s",(accntno,t,))
                self.mydb.commit()
                tk.messagebox.showinfo("Success!!!","Account created")
                mycursor.close()
                self.mydb.close()
                self.back()

            if self.mode == 'Details':
                mycursor = self.mydb.cursor()
                sql_script = 'SELECT uname,phoneno,addr,email,aadhar,userid,accntbal,accntno FROM users WHERE userid = %s'
                mycursor.execute(sql_script,(self.uname,))
                self.user_details = mycursor.fetchone()
                mycursor.close()

            if self.mode == 'Update':
                mycursor = self.mydb.cursor()
                sql_script = 'UPDATE users SET passwd = %s, uname = %s, photo = %s, addr = %s, email = %s, phoneno = %s WHERE userid = %s'
                try:
                    userPicture = self.convertToBinaryData(self.photo_directory)
                except:
                    userPicture = self.convertToBinaryData('cache/temp.png')
                user = self.entry['Password'].get(),self.entry['Name'].get(),userPicture,self.entry['Address'].get(),self.entry['E-Mail'].get(),self.entry['Phone Number'].get(),self.uname
                mycursor.execute(sql_script,user)
                self.mydb.commit()
                tk.messagebox.showinfo("Success!!!","Account updated")
                mycursor.close()
                self.mydb.close()
                self.back()
        except:
            mycursor.close()
            self.mydb.rollback()
            tk.messagebox.showerror("Error!!!","Something is wrong")

    # Update details
    def update_get(self):
        try:
            mycursor = self.mydb.cursor()
            sql_script = 'SELECT uname,phoneno,addr,email,aadhar,userid,passwd FROM users WHERE userid = %s'
            mycursor.execute(sql_script,(self.uname,))
            self.user_details = mycursor.fetchone()
            mycursor.close()
        except:
            mycursor.close()
            tk.messagebox.showerror("Error!!!","Something is wrong")

    # username availability
    def user_available(self):
        try:
            cursor = self.mydb.cursor()
            sql_script = "SELECT userid FROM users WHERE userid = %s"
            username = self.entry['Username'].get()
            cursor.execute(sql_script,(username,))
            userid = cursor.fetchone()
            cursor.close()
            if userid is None:
                self.available = 'true'
            else:
                self.available = 'false'
        except:
            cursor.close()
            tk.messagebox.showerror("Error!!!","Something is wrong")


    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.commit()
            self.mydb.close()
