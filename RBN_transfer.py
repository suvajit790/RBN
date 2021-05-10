import tkinter as tk
from tkinter import messagebox as msg
from datetime import date,datetime
from PIL import Image,ImageTk
import mysql.connector as mysql


class Transfer_window:

    def __init__(self, master,pr_window,uname,passwd):
        try:
            self.mydb = mysql.connect(host='hostname.com', port=3306, username = 'username',password = 'password',database = 'databaseName',use_pure = True) #replace with your own database details
        except:
            tk.messagebox.showerror("Error!!!","Check your internet connection")
        self.master = master
        self.master.geometry("800x750+10+50")
        self.master.title('Transfer Money')
        self.master.resizable(width=False,height=False)
        self.master.config(bg="#13051e")

        self.bank_logo_img=tk.PhotoImage(file="Raw/deposit_scr.png")
        default_photo=tk.PhotoImage(file="Raw/Photo.png")

        #--------------variables--------------
        self.uname = uname
        self.passwd = passwd
        self.previous_window = pr_window
        self.next_window = ''

        # LOGO
        self.logo_label=tk.Label(self.master ,image=self.bank_logo_img,bg="#13051e")
        self.logo_label.place(x=320,y=0)

        # Photo label
        self.Photo_label=tk.Label(self.master,bg="white",image = default_photo,width=150,height=200)
        self.Photo_label.place(x=105,y=220)

        # Retrieve Photo and user details
        try:
            mycursor = self.mydb.cursor()
            sql_script = 'SELECT uname,phoneno,accntno,accntbal FROM users WHERE userid = %s'
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
        self.rec_accntno = tk.StringVar()
        self.transfer_amount = tk.StringVar()
        self.rec_accntbal = tk.StringVar()

        # name
        userName_label=tk.Label(self.master, font=('arial',15),text="Name",fg='white',bg="#13051e")
        userName_label.place(x=23,y=450)
        userName_value=tk.Label(self.master,text = user_name,fg='black',font=('arial',12,'bold'),width = 20)
        userName_value.place(x=150,y=450)

        # account Number
        accNo_label=tk.Label(self.master, font=('arial',15),text="Account No",fg='white',bg="#13051e")
        accNo_label.place(x=23,y=495)
        accNo_value=tk.Label(self.master,text = accnt_no,fg='black',font=('arial',12,'bold'),width = 20)
        accNo_value.place(x=150,y=495)

        # phone Number
        phNo_label=tk.Label(self.master, font=('arial',15),text="Phone No",fg='white',bg="#13051e")
        phNo_label.place(x=23,y=540)
        phNo_value=tk.Label(self.master,text = user_phone,fg='black',font=('arial',12,'bold'),width = 20)
        phNo_value.place(x=150,y=540)

        # account Balnce
        accbal_label=tk.Label(self.master, font=('arial',15),text="Account Bal.",fg='white',bg="#13051e")
        accbal_label.place(x=23,y=585)
        accbal_value=tk.Label(self.master,text = self.accnt_bal,fg='black',font=('arial',12,'bold'),width = 20)
        accbal_value.place(x=150,y=585)

        # VERTICLE LINE
        verticle_lb=tk.Label(self.master,height=30,bg="#907db5",relief="raised")
        verticle_lb.place(x=405,y=215)

        # To Whom Transfer
        receiverAcc_label=tk.Label(self.master, font=('arial',15),text="Enter Receiver's\nAccount number",fg='white',bg="#13051e")
        receiverAcc_label.place(x=560,y=200)
        receiverAcc_entry=tk.Entry(self.master,textvariable = self.rec_accntno,width=15,font=('arial',20))
        receiverAcc_entry.place(x=520,y=260)

        # check button
        checkbtn=tk.Button(self.master,font=('arial',10),text="Check",fg='white',bg="#907db5",command = self.Check_user)
        checkbtn.place(x=606,y=300)

        # Receiver's Photo
        self.Rec_Photo_label=tk.Label(self.master,bg="white",image = default_photo,width=150,height=200)
        self.Rec_Photo_label.place(x=555,y=340)

        # Receiver's name
        recName_label=tk.Label(self.master, font=('arial',16),text="Name",fg='white',bg="#13051e")
        recName_label.place(x=460,y=570)
        self.recName_value=tk.Label(self.master,text = '',fg='black',font=('arial',12,'bold'),width = 20)
        self.recName_value.place(x=543,y=570)

        # amount to be tansfered
        self.receiverAmount_entry=tk.Entry(self.master,textvariable = self.transfer_amount,width=15,font=('arial',20),justify='center')
        self.receiverAmount_entry.place(x=520,y=620)
        receiverAmount_label=tk.Label(self.master, font=('arial',15),text="Amount To be Transfered",fg='white',bg="#13051e")
        receiverAmount_label.place(x=520,y=660)


        # Tansfer Button
        deposit_btn=tk.Button(self.master,font=('arial',17,'bold'),text="Transfer",fg='white',bg="#907db5",command = self.Transfer)
        deposit_btn.place(x=130,y=645)

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

    # Back button function
    def back(self):
        self.next_window = self.previous_window
        self.master.destroy()

    # Convert binary data to proper format and write it on cache/
    def write_file(self,data,filename):
        with open(filename, "wb") as file:
            file.write(data)
        file.close()

    # Check_user function
    def Check_user(self):
        try:
            cursor = self.mydb.cursor()
            sql_query = 'SELECT photo,uname,accntbal FROM users WHERE accntno = %s'
            cursor.execute(sql_query,(self.rec_accntno.get(),))
            user_detail = cursor.fetchall()
            cursor.close()
            self.write_file(user_detail[0][0],'cache/temp_rec.png')
            self.rec_name = user_detail[0][1]
            self.rec_accntbal = str(user_detail[0][2])
            self.recName_value.config(text = self.rec_name)
            user_photo = Image.open('cache/temp_rec.png')
            user_photo_im = ImageTk.PhotoImage(user_photo)
            self.Rec_Photo_label.config(image = user_photo_im)
            self.Rec_Photo_label.image_names = user_photo_im
        except:
            cursor.close()
            tk.messagebox.showerror("Error!!!","Something is wrong")

    # Transfer function
    def Transfer(self):
        try:
            newcursor = self.mydb.cursor()
            sql_script = 'UPDATE users SET accntbal = %s WHERE userid = %s'
            sql_script1 = 'UPDATE users SET accntbal = %s WHERE accntno = %s AND uname = %s'
            updated_user_bal = float(self.accnt_bal) - float(self.transfer_amount.get())
            updated_rec_bal = float(self.rec_accntbal) + float(self.transfer_amount.get())
            data = updated_user_bal,self.uname
            rec_data = updated_rec_bal,self.rec_accntno.get(),self.rec_name
            print(rec_data)
            newcursor.execute(sql_script,data)
            newcursor.execute(sql_script1,rec_data)
            newcursor.close()
            self.mydb.commit()
            tk.messagebox.showinfo("Success!!!","Balance updated")
            self.mydb.close()
            self.back()
        except:
            self.mydb.rollback()
            tk.messagebox.showerror('Sorry!!!','Something went wrong')


    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.commit()
            self.mydb.close()
        
