import tkinter as tk
from tkinter import messagebox as msg
from datetime import date,datetime
from PIL import Image,ImageTk
import mysql.connector as mysql


class WithdrawMOney_window:

    def __init__(self, master,uname,passwd):
        try:
            self.mydb = mysql.connect(host='hostname.com', port=3306, username = 'username',password = 'password',database = 'databaseName',use_pure = True) #replace with your own database details
        except:
            tk.messagebox.showerror("Error!!!","Check your internet connection")
        self.master = master
        self.master.title("Withdraw Money")
        self.master.geometry("800x750+10+50")
        self.master.resizable(width=False,height=False)
        self.master.config(bg="#13051e")

        self.bank_logo_img=tk.PhotoImage(file="Raw/withdraw_logo.png")  #logo
        default_photo=tk.PhotoImage(file="Raw/Photo.png")

        #--------------variables--------------
        self.uname = uname
        self.passwd = passwd
        self.next_window = ''


        self.logo_label=tk.Label(self.master ,image=self.bank_logo_img,bg="#13051e")
        self.logo_label.place(x=250,y=0)

        # photo label
        userPhoto_label=tk.Label(self.master,font=('arial',15,"bold"),text="Photo",bg="#13051e",fg="white")
        userPhoto_label.place(x=130,y=295)

        self.Photo_label=tk.Label(self.master,bg="white",image = default_photo,width=150,height=200)
        self.Photo_label.place(x=85,y=335)

        # Retrieve Photo and user details
        try:
            mycursor = self.mydb.cursor()
            sql_script = 'SELECT uname,phoneno,accntno,accntbal FROM users WHERE users.userid = %s'
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

        user_name = user_detail[0]
        user_phone = user_detail[1]
        accnt_no = user_detail[2]
        self.accnt_bal = user_detail[3]
        self.wd_amount = tk.StringVar()

        # name
        userName_label=tk.Label(self.master, font=('arial',15),text="Name",fg='white',bg="#13051e")
        userName_label.place(x=20,y=575)
        userName_value=tk.Label(self.master,text = user_name,fg='black',font=('arial',12,'bold'),width = 20)
        userName_value.place(x=150,y=575)

        # account Number
        accNo_label=tk.Label(self.master, font=('arial',15),text="Account No",fg='white',bg="#13051e")
        accNo_label.place(x=20,y=615)
        accNo_value=tk.Label(self.master,text = accnt_no,fg='black',font=('arial',12,'bold'),width = 20)
        accNo_value.place(x=150,y=615)

        # phone Number
        phNo_label=tk.Label(self.master, font=('arial',15),text="Phone No",fg='white',bg="#13051e")
        phNo_label.place(x=20,y=655)
        phNo_value=tk.Label(self.master,text = user_phone,fg='black',font=('arial',12,'bold'),width = 20)
        phNo_value.place(x=150,y=655) 

        # VERTICLE LINE
        verticle_lb=tk.Label(self.master,height=24,bg="#907db5",relief="raised")
        verticle_lb.place(x=390,y=330)
        
        # available amount
        availableBlnc_label=tk.Label(self.master,font=('arial',15),text="Available Balance",fg='white',bg="#13051e")
        availableBlnc_label.place(x=440,y=400)
        availableBlnc_value=tk.Label(self.master,text = self.accnt_bal,fg='black',font=('arial',12,'bold'),width = 15)
        availableBlnc_value.place(x=610,y=400)

        # Withdraw ammount
        withdrawAmnt_label=tk.Label(self.master, font=('arial',20),text="Withdraw Amount",fg='white',bg="#13051e")
        withdrawAmnt_label.place(x=490,y=490)
        withdrawAmnt_entry=tk.Entry(self.master,text = self.wd_amount,fg='black',font=('arial',16,'bold'),width = 22,justify='center')
        withdrawAmnt_entry.place(x=470,y=540)

        # withdraw Button
        deposit_btn=tk.Button(self.master,font=('arial',17,'bold'),text="Withdraw",fg='white',bg="#907db5",command = self.Withdraw)
        deposit_btn.place(x=540,y=625)

        # Back button
        back_btn = tk.Button(self.master,font=('arial',10,"bold"), text = '<< Back', width = 10,relief="raised",command=self.back)
        back_btn.place(x=20,y=20)

        #-------------------------------------------------status bar-------------------------------------------------#

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

    # back Button function
    def back(self):
        self.next_window = 'Home'
        self.master.destroy()

    # Convert binary data to proper format and write it on cache/
    def write_file(self,data,filename):
        with open(filename, "wb") as file:
            file.write(data)
        file.close()

    # Withdraw function
    def Withdraw(self):
        self.next_window = 'home'
        try:
            mycursor = self.mydb.cursor()
            sql_script = 'UPDATE users SET accntbal = %s WHERE userid = %s'
            updated_bal = float(self.accnt_bal) - float(self.wd_amount.get())
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

        
