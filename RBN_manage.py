import tkinter as tk
from tkinter import messagebox
from datetime import date,datetime
import RBN_login as lg
import RBN_home as hm
import RBN_register as reg
import RBN_deposit as dp
import RBN_withdraw as wd
import RBN_transfer as trans


class manage:

    def __init__(self):
        self.username = ''
        self.password = ''

    def Login(self):
        app = lg.Login_window(tk.Tk())
        self.username = app.uname
        self.password = app.passwd
        if app.next_window == 'Home':
            self.Home()
        if app.next_window == 'Register':
            self.Register('Login','Register')
        del app

    def Register(self,prw,mode):
        app = reg.Account_window(tk.Tk(),prw,self.username,self.password,mode)
        if app.next_window == 'Login':
            self.Login()
        if app.next_window == 'Home':
            self.Home()
        del app

    def Home(self):
        app = hm.main_window(tk.Tk(),self.username,self.password)
        if app.next_window == 'Register':
            self.Register('Home',app.registermode)
        if app.next_window == 'Deposit':
            self.Deposit()
        if app.next_window=='Withdraw':
            self.Withdraw()
        if app.next_window=='Transfer':
            self.Transfer('Home')
        if app.next_window=='Login':
            self.Login()
        del app

    def Deposit(self):
        app = dp.Deposit_window(tk.Tk(),self.username,self.password)
        if app.next_window == 'Home':
            self.Home()
        if app.next_window=='Transfer':
            self.Transfer('Deposit')
        del app

    def Withdraw(self):
        app=wd.WithdrawMOney_window(tk.Tk(),self.username,self.password)
        if app.next_window == 'Home':
            self.Home()
        del app

    def Transfer(self,prw):
        app=trans.Transfer_window(tk.Tk(),prw,self.username,self.password)
        if app.next_window == 'Home':
            self.Home()
        if app.next_window == 'Deposit':
            self.Deposit()
        del app

def main():
    m=manage()
    m.Login()

if __name__ == '__main__':
    main()