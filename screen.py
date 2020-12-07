from selenium import webdriver
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from insta_search_unf import InstaSearchUnf

class Screen:
    def __init__(self):
        window = Tk()
        window.geometry("500x350")
        window.resizable(0, 0)
        window.title("Instagram's Bot")

        label = Label(window, text="FILL WITH YOUR INSTAGRAM'S ACCOUNT CREDENTIALS")
        label.place(x=250, y=30, anchor="center")
        label = Label(window, text="Username")
        label.place(x=150, y=70, anchor="center")
        label = Label(window, text="Password")
        label.place(x=150, y=120, anchor="center")
        
        label = Label(window, text="FILL WITH THE @ OF THE ACCOUNT YOU WANT TO CHECK\n")
        label.place(x=250, y=170, anchor="center")
        label = Label(window, text="Username")
        label.place(x=150, y=220, anchor="center")
        
        label = Label(window, text="Select your browser")
        label.place(x=150, y=270, anchor="center")
        browser_list= ["Microsoft Edge","Opera","Google Chrome","Mozilla Firefox"]
        cbx_browser = ttk.Combobox(window, values=browser_list, state="readonly", width=25)
        cbx_browser.place(x=295, y=270, anchor="center")

        user_login_text = StringVar()
        entry_user_login = Entry(window, textvariable=user_login_text, width=30)
        entry_user_login.place(x=275, y=70, anchor="center")
        pw_text = StringVar()
        entry_pw = Entry(window, textvariable=pw_text, show="*", width=30)
        entry_pw.place(x=275, y=120, anchor="center")
        user_searched_text = StringVar()
        entry_user_searched = Entry(window, textvariable=user_searched_text, width=30)
        entry_user_searched.place(x=275, y=220, anchor="center")
        
        
        myButton = Button(window, text="Check", width=25, command= lambda: self.on_button_press(user_login_text, pw_text, user_searched_text, cbx_browser))
        myButton.place(x=250, y=320, anchor="center")
        
        window.mainloop()

    def on_button_press(self, username, password, username_searched, cbx_browser):
        user_login = username.get()
        pw = password.get()
        user_searched = username_searched.get()
        cbx_bw = cbx_browser.get()
        InstaSearchUnf(user_login, pw, user_searched, cbx_bw)
        