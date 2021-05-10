import tkinter as tk
from tkinter import messagebox as msg
from datetime import date,datetime
from PIL import Image,ImageTk
import mysql.connector as mysql


class Deposit_window:

    def __init__(self, master,uname,passwd):
        try:
            self.mydb = mysql.connect(host='hostname.com', port=3306, username = 'username',password = 'password',database = 'databaseName',use_pure = True) #replace with your own database details
        except:
            tk.messagebox.showerror("Error!!!","Check your internet connection")
        self.master = master
        self.master.title("Deposit Money")
        self.master.geometry("800x750+10+50")
        self.master.resizable(width=False,height=False)
        self.master.config(bg="#13051e")

        self.bank_logo_img=tk.PhotoImage(file="Raw/deposit_scr.png")  #logo


        #--------------variables--------------
        self.uname = uname
        self.passwd = passwd
        self.next_window = ''
        
        default_photo=tk.PhotoImage(file="Raw/Photo.png")

        # LOGO
        self.logo_label=tk.Label(self.master ,image=self.bank_logo_img,bg="#13051e")
        self.logo_label.place(x=320,y=0)

        # photo label
        userPhoto_label=tk.Label(self.master,font=('arial',15,"bold"),text="Photo",bg="#13051e",fg="white")
        userPhoto_label.place(x=130,y=240)

        self.Photo_label=tk.Label(self.master,bg="white",image = default_photo,width=150,height=200)
        self.Photo_label.place(x=86,y=280)

        # Retrieve Photo and user details
        try:
            mycursor = self.mydb.cursor()
            sql_script = 'SELECT branches.brname,users.uname,users.phoneno,users.accntno,users.accntbal FROM branches,users WHERE branches.brcode = users.branchcode AND users.userid = %s'
            sql_script1 = 'SELECT photo FROM users WHERE userid = %s'
            mycursor.execute(sql_script,(self.uname,))
            user_detail = mycursor.fetchone()
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

        br_name = user_detail[0]
        user_name = user_detail[1]
        user_phone = user_detail[2]
        accnt_no = user_detail[3]
        self.accnt_bal = user_detail[4]
        self.dp_amount = tk.StringVar()

        # Name
        Name_label=tk.Label(self.master, font=('arial',10),text="Name",fg='white',bg="#13051e")
        Name_label.place(x=23,y=540)
        Name_show=tk.Label(self.master,text = user_name,fg='black',bg="white",font=('arial',8,'bold'),width = 20)
        Name_show.place(x=150,y=540)

        # ph no
        Phone_label=tk.Label(self.master, font=('arial',10),text="Phone Number",fg='white',bg="#13051e")
        Phone_label.place(x=23,y=570)
        Phone_show=tk.Label(self.master,text = user_phone,fg='black',bg="white",font=('arial',8,'bold'),width = 20)
        Phone_show.place(x=150,y=570)

        # branch name
        ifscCode_label=tk.Label(self.master, font=('arial',10),text="Branch Name",fg='white',bg="#13051e")
        ifscCode_label.place(x=23,y=600)
        ifscCode_show=tk.Label(self.master,text = br_name,fg='black',bg="white",font=('arial',8,'bold'),width = 20)
        ifscCode_show.place(x=150,y=600)

        # VERTICLE LINE
        verticle_lb=tk.Label(self.master,height=29,bg="#907db5",relief="raised")
        verticle_lb.place(x=360,y=246)

        # Transaction label
        depositAmnt_label=tk.Label(self.master,font=('arial',15,"bold"),text="Transaction",bg="#907db5",fg="white")
        depositAmnt_label.place(x=530,y=250)    

        # Account Number
        branchName_label=tk.Label(self.master, font=('arial',15),text="Account Number",fg='white',bg="#13051e")
        branchName_label.place(x=405,y=340)
        branchName_show=tk.Label(self.master,text = accnt_no,fg='black',bg="white",font=('arial',12,'bold'),width = 20)
        branchName_show.place(x=565,y=340)

        # Account Balance
        branchName_label=tk.Label(self.master, font=('arial',15),text="Account Balance",fg='white',bg="#13051e")
        branchName_label.place(x=405,y=400)
        branchName_show=tk.Label(self.master,text = self.accnt_bal,fg='black',bg="white",font=('arial',12,'bold'),width = 20)
        branchName_show.place(x=565,y=400)

        # Amount to Deposit
        branchName_label=tk.Label(self.master, font=('arial',15),text="Enter Amount",fg='white',bg="#13051e")
        branchName_label.place(x=405,y=500)
        branchName_entry=tk.Entry(self.master,textvariable = self.dp_amount,fg='black',bg="white",font=('arial',16,'bold'),width = 17,justify='center')
        branchName_entry.place(x=565,y=500)

        # Deposit Button
        deposit_btn=tk.Button(self.master,font=('arial',20,'bold'),text="Deposit Money",fg='white',bg="#907db5",command=self.Deposit)
        deposit_btn.place(x=486,y=630)

        # Transfer money button
        deposit_btn=tk.Button(self.master,font=('arial',15,'bold'),text="Transfer Money",fg='white',bg="#907db5",command=self.Transfer)
        deposit_btn.place(x=95,y=650)

        # Back button
        back_btn = tk.Button(self.master,font=('arial',10,"bold"), text = '<< Back', width = 10,relief="raised",command=self.back)
        back_btn.place(x=20,y=20)

        #---------------------------------------------- status bar ----------------------------------------------#

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

    # Back function
    def back(self):
        self.next_window = 'Home'
        self.master.destroy()

    # Convert binary data to proper format and write it on cache/
    def write_file(self,data,filename):
        with open(filename, "wb") as file:
            file.write(data)
        file.close()

    # transfer window
    def Transfer(self):
        self.next_window = "Transfer"
        self.master.destroy()

    # Deposit button function
    def Deposit(self):
        try:
            mycursor = self.mydb.cursor()
            sql_script = 'UPDATE users SET accntbal = %s WHERE userid = %s'
            updated_bal = float(self.dp_amount.get()) + float(self.accnt_bal)
            data = updated_bal,self.uname
            mycursor.execute(sql_script,data)
            self.mydb.commit()
            tk.messagebox.showinfo("Success!!!","Balance updated")
            mycursor.close()
            self.mydb.close()
            self.back()
        except:
            self.mydb.rollback()
            mycursor.close()
            tk.messagebox.showerror('Sorry!!!','Something went wrong')

    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.commit()
            self.mydb.close()
