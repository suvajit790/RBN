import tkinter as tk
from tkinter import messagebox as msg
from datetime import date,datetime
import mysql.connector as mysql


class main_window:

    def __init__(self,master,uname,passwd):
        try:
            self.mydb = mysql.connect(host='hostname.com', port=3306, username = 'username',password = 'password',database = 'databaseName',use_pure = True) #replace with your own database details
        except:
            tk.messagebox.showerror("Error!!!","Check your internet connection")
        self.master = master
        self.master.title("RBN")
        self.master.geometry("800x750+10+50")
        self.master.resizable(width=False,height=False)
        self.master.config(bg="#13051e")
        #=========================Icons======================
        new_account_img=tk.PhotoImage(file="Raw/new_ant.png")
        deposit_money_img=tk.PhotoImage(file="Raw/deposit.png")
        withdrwal_img=tk.PhotoImage(file="Raw/withdraw.png")
        bank_logo_img=tk.PhotoImage(file="Raw/logo.png")
        close_btn_img=tk.PhotoImage(file="Raw/close.png")
        logout_btn_img=tk.PhotoImage(file="Raw/logout.png")
        #---------------------------end---------------------

        #--------------variables--------------
        self.registermode = ''
        self.uname = uname
        self.passwd = passwd
        self.next_window = ''

        #============================Menu==================
        #menu list

        main_menu=tk.Menu(self.master)
        self.master.configure(menu=main_menu)
        home_menu=tk.Menu(main_menu,tearoff=False)
        accounts_menu=tk.Menu(main_menu,tearoff=False)
        cash_menu=tk.Menu(main_menu,tearoff=False)
        main_menu.add_cascade(label="Home",menu=home_menu)
        main_menu.add_cascade(label="Accounts",menu=accounts_menu)
        main_menu.add_cascade(label="Cash",menu=cash_menu)

        #------------------------end---------------------

        #-----------------------------Menu Commands--------------------------------#
        #home menu
        home_menu.add_command(label="Logout",command = self.logout)
        home_menu.add_command(label="Close",command = self.close)
        #acount menu
        accounts_menu.add_command(label="Add Account",command = self.Reg)
        accounts_menu.add_command(label="Update Account",command = self.Update)
        accounts_menu.add_command(label="Delete Account",command = self.Delete)
        accounts_menu.add_command(label="Account Detail",command=self.Details)


        #cash menu
        cash_menu.add_command(label="Withdraw Money",command = self.Withdraw)
        cash_menu.add_command(label="Deposit Money",command = self.Dep)
        cash_menu.add_command(label="Transfer Money",command = self.Transfer)
        main_menu.add_command(label="About",command = self.About)

        #---------------------------------- Bank name ----------------------------------#
        lbl_info=tk.Label(self.master,font=('Sans',42,'bold'),text="RESERVE BANK OF NOIDA",fg='#e73334',bg="#13051e")
        lbl_info.place(x=24,y=10)
        #----------------end----------------------
        #=================LOGO===================
        logo_label=tk.Label(self.master,image=bank_logo_img,bg="#13051e")
        logo_label.place(x=65,y=100)


        #=========================================Bank Detail =================================================
        try:
            mycur = self.mydb.cursor()
            sql_script = 'SELECT branches.brname,branches.brcode,branches.ifsc FROM branches,users WHERE branches.brcode = users.branchcode AND users.userid = %s'
            mycur.execute(sql_script,(self.uname,))
            branch_detail = mycur.fetchall()
            mycur.close()
        except:
            mycur.close()
            tk.messagebox.showerror("Error!!!","Something is wrong")
        ifsc_code = branch_detail[0][2]
        branch_code = branch_detail[0][1]
        branch_name = branch_detail[0][0]

        #branch Name
        branchName_label=tk.Label(self.master, font=('arial',20),text="Branch Name : ",fg='white',bg="#13051e")
        branchName_label.place(x=105,y=360)
        branchName_show=tk.Label(self.master,text=branch_name,fg='black',bg="white",font=('arial',10,'bold'),width = 15)
        branchName_show.place(x=300,y=372)


        #branch code
        branchCode_label=tk.Label(self.master, font=('arial',20),text="Branch Code : ",fg='white',bg="#13051e")
        branchCode_label.place(x=105,y=410)
        branchCode_show=tk.Label(self.master,text=branch_code,fg='black',bg="white",font=('arial',10,'bold'),width = 15)
        branchCode_show.place(x=300,y=422)

        #IFCS Code
        ifscCode_label=tk.Label(self.master, font=('arial',20),text="IFSC Code : ",fg='white',bg="#13051e")
        ifscCode_label.place(x=105,y=460)
        ifscCode_show=tk.Label(self.master,text=ifsc_code,fg='black',bg="white",font=('arial',10,'bold'),width = 15)
        ifscCode_show.place(x=300,y=472)

        #============================Upadte Bank Deatil Button=====================================
        updateDetail_btn=tk.Button(self.master,font=('Verdana',17,'bold'),text="UPDATE",fg='black',activebackground="#907db5",bg="#907db5",command=self.Update)
        updateDetail_btn.place(x=190,y=560)

        #Close button
        close_btn = tk.Button(self.master,font=('arial',10,"bold"), text = 'close', width = 100,height = 20,relief="raised",anchor='c',bd=1,image=close_btn_img,compound=tk.LEFT,command=self.close)
        close_btn.place(x=30,y=627)

        #Logout button
        logout_btn = tk.Button(self.master,font=('arial',10,"bold"), text = 'Logout', width = 100,height = 20,bd=1,relief="raised",image=logout_btn_img,compound=tk.LEFT,command=self.logout)
        logout_btn.place(x=380,y=627)

        #---------------------------------- List Of option avaliable ----------------------------------
        new_Act_btn=tk.Button(self.master,font=('Verdana',10,'bold'),text="ACCOUNT DETAIL",width=200,fg='black',activebackground="#907db5",bg="#907db5",bd=1,anchor='c',image=new_account_img,compound=tk.TOP,command=self.Details)
        new_Act_btn.place(x=550,y=130)


        deposit_money_btn=tk.Button(self.master,font=('Verdana',10,'bold'),text="DEPOSIT MONEY",width=200,activebackground="#907db5",fg='black',bg="#907db5",bd=1,anchor='c',image=deposit_money_img,compound=tk.TOP,command=self.Dep)
        deposit_money_btn.place(x=550,y=315)


        withdrwal_btn=tk.Button(self.master,font=('Verdana',10,'bold'),text="WITHDRAW AMOUNT",width=200,activebackground="#907db5",fg='black',bg="#907db5",bd=1,anchor='c',image=withdrwal_img,compound=tk.TOP,command=self.Withdraw)
        withdrwal_btn.place(x=550,y=500)
        #------------------end-----------------------------

        #=========================verticle line ====================
        verticle_lb=tk.Label(self.master,height=259,font=('arial',1),bg="#907db5",relief="raised")
        verticle_lb.place(x=520,y=130)

        #=========================Horizontal line ====================
        horizontal_lb=tk.Label(self.master,width=450,borderwidth=1,bg="#907db5",font=('arial',1),relief="raised")
        horizontal_lb.place(x=30,y=320)

        #-----------------------------------status bar-----------------------------------#

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

    def Reg(self):
            self.next_window = 'Register'
            self.registermode = 'Register'
            self.master.destroy()

    def Details(self):
            self.next_window = 'Register'
            self.registermode = 'Details'
            self.master.destroy()

    def Update(self):
            self.next_window = 'Register'
            self.registermode = 'Update'
            self.master.destroy()

    def Dep(self):
            self.next_window = 'Deposit'
            self.master.destroy() 

    def Withdraw(self):
            self.next_window = 'Withdraw'
            self.master.destroy()  
    
    def Transfer(self):
        self.next_window = "Transfer"
        self.master.destroy()
    
    def logout(self):
        self.next_window = 'Login'
        self.master.destroy()
        
    def close(self):
        self.master.destroy()

    def Delete(self):
        try:
            mycursor = self.mydb.cursor()
            sql_script = 'DELETE FROM users WHERE userid = %s'
            mycursor.execute(sql_script,(self.uname,))
            mycursor.close()
            self.mydb.commit()
            self.next_window = 'Login'
            self.master.destroy()
        except:
            mycursor.close()
            self.mydb.rollback()
            tk.messagebox.showerror('Error!!!','Something went wrong')
        

    def About(self):
        tk.messagebox.showinfo('Developers','This project is made by\n1: SURESH KUMAR (BCA,Chaudhary Charan Singh University)\n2: SUVAJIT PATRA (BSC,VIDYASAGAR University)')

    def __del__(self):
        if self.mydb.is_connected():
            self.mydb.commit()
            self.mydb.close()
